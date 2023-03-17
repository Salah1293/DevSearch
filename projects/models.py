from email.policy import default
from turtle import title
from django.db import models
from django.forms import CharField
import uuid
from users.models import profile



class project(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(profile,null=True, blank=True,on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio' , '-vote_total' , 'title']

    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id',flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()





class review(models.Model):
    VOTE_TYPE=(
        ('up','Up vote'),
        ('down','Down vote'),
    )
    owner = models.ForeignKey(profile,on_delete=models.CASCADE,null=True)
    project = models.ForeignKey(project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    class Meta:
        unique_together = [['owner','project']]

    def __str__(self):
        return self.value


class Tag(models.Model):

    name = models.CharField(max_length=200)
    
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    def __str__(self):
        return self.name


