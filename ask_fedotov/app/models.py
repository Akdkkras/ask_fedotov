from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User


# Managers

class QuestionQuerySet(models.QuerySet):
    def order_by_likes(self):
        return self.annotate(
            likes_count=Count('likes', distinct=True)
        ).order_by('-likes_count')

    def order_by_new(self):
        return self.order_by('-created_at')


class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuestionQuerySet(self.model, using=self._db)

    def order_by_likes(self):
        return self.get_queryset().order_by_likes()

    def order_by_new(self):
        return self.get_queryset().order_by_new()


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
    qs = QuestionManager()


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True, default='value_default')

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
