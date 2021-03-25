from django.db import models

class User(models.Model):
    name = models.CharField(max_length = 64)
    email = models.EmailField(unique = True)
    create_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email


class Question(models.Model):
    enunciado = models.TextField()
    alternativas = models.JSONField()
    alternativa_correta = models.IntegerField(choices=[(0,"A"),(1,"B"),(2,"C"),(3,"D")])
    disponivel = models.BooleanField(default=False)

    def __str__(self):
        return self.enunciado

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    points = models.IntegerField()
    answered_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['user', 'question'], name = 'unique_answer')
        ]