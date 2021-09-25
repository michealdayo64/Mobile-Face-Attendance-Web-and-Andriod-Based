from django.db import models
from Quiz.models import Aquiz
# Create your models here.

class Questions(models.Model):
    text = models.CharField(max_length = 200)
    quiz = models.ForeignKey(Aquiz, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.text}"

    def get_answers(self):
        return self.answer_set.all()

    class Meta:
        verbose_name_plural = 'Questions'

class Answer(models.Model):
    text = models.CharField(max_length = 200)
    correct = models.BooleanField(default = False)
    question = models.ForeignKey(Questions, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"