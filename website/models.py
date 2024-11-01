from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


class Word(models.Model):
    text = models.CharField(max_length=100)



class MorpionJeu(models.Model):
    plateau = models.CharField(max_length=9, default=' ' * 9)  # 9 espaces pour un plateau 3x3
    tour_actuel = models.CharField(max_length=1, default='X')  # 'X' ou 'O'
    gagnant = models.CharField(max_length=1, blank=True, null=True)  # Gagnant ('X', 'O', ou None)

