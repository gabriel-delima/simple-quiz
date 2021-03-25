from django.shortcuts import render, redirect
from django.http import HttpResponse
from quiz.base.models import Question, User, Answer
from quiz.base.forms import UserForm
from django.utils.timezone import now
from django.db.models.aggregates import Sum


def home(request):
    if request.method == "POST":

        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            form = UserForm(request.POST)
            if form.is_valid():

                user = form.save()
                return redirect('/questions/1')
            else:
                context = {'form':form}
                return render(request, "base/home.html", context)
        else:
            request.session['user_id'] = user.id
            return redirect('/questions/1')

    return render(request, "base/home.html")

MAX_POINTS = 1000
def questions(request, index):
    try:
        user_id = request.session['user_id']
    except KeyError:
        return redirect('/')
    else:
        try:
            question = Question.objects.filter(disponivel = True).order_by('id')[index-1]
            context = {"question_index" : index, "question":question}
        except IndexError:
            return redirect('/ranking')
        if request.method == "POST":
            answer = int(request.POST['answer'])
            if answer == question.alternativa_correta:
                # Save question data
                try:
                    first_answer_time = Answer.objects.filter(question=question).order_by('answered_time')[0].answered_time
                except IndexError:
                    Answer(user_id = user_id, question = question, points=MAX_POINTS).save()
                else:
                    diference = int((now() - first_answer_time).total_seconds())
                    points = max(MAX_POINTS - diference, 10)
                    Answer(user_id = user_id, question = question, points=points).save()
                
                return redirect(f'/questions/{index+1}')

            context['answer'] = answer
        return render(request, "base/game.html", context=context)

def ranking(request):
    try:
        user_id = request.session['user_id']
    except KeyError:
        return redirect('/')
    else:
        user_score = (Answer.objects.filter(user_id = user_id).aggregate(Sum('points')))['points__sum']

        users_with_higher_score = Answer.objects.values('user').annotate(Sum('points')).filter(points__sum__gt = user_score).count()
        
        first_users = list(Answer.objects.values('user', 'user__name').annotate(Sum('points')).order_by('-points__sum')[:5])
        
        context = {
                'user_score':user_score , 
                'user_position':users_with_higher_score+1,
                'first_users': first_users
                }
        return render(request, "base/ranking.html", context=context)


