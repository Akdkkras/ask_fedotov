from django.db import models
from django.contrib.auth.models import User


# Managers

class QuestionManager(models.Manager):
    def new(self):
        return self.get_queryset().order_by('-created_at')
    
    def best(self):
        return self.get_queryset().annotate(
            likes_count=models.Count('likes')
        ).order_by('-likes_count', '-created_at')


# Main models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # avatar = models.ImageField(blank=True)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    user = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='questions', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', related_name='questions')
    likes = models.ManyToManyField(Profile, related_name='question_likes', through='QuestionLike')

    objects = models.Manager()
    custom = QuestionManager()



class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    user = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='answers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(Profile, related_name='answer_likes', through='AnswerLike')


# Additional models

class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['question', 'user']


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['answer', 'user']

