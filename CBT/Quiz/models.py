from django.db import models
import random
# Create your models here.
DIFF_CHOICES = (
    ('Hard', 'Hard'),
    ('Medium', 'Medium'),
    ('Easy', 'Easy'),
)

class Aquiz(models.Model):
    name = models.CharField(max_length =120)
    topic = models.CharField(max_length = 120)
    number_of_quesstions = models.IntegerField()
    time = models.IntegerField(help_text = 'Duration of time in minutes')
    required_score_to_pass = models.IntegerField(help_text = 'Requ++ired score to pass')
    difficulty = models.CharField(max_length = 6, choices = DIFF_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.topic}"

    def get_questions(self):
        questions = list(self.questions_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_quesstions]


