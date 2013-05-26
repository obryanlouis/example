from django.db import models
from django.contrib.auth.models import User

class TitleModel(models.Model):
    '''
    Holds job titles for backboard/me section.
    '''
    user = models.ForeignKey(User, unique=False)
    job_title = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    website = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    location = models.CharField(max_length=100)
    start_date = models.DateField(max_length=20)
    end_date = models.DateField(blank=True)

class AwardModel(models.Model):
    '''
    Holds awards_or_mentions for
    backboard/me section.
    '''
    AWARD_OR_MENTION = (
        ('ME', 'Mention'),        
        ('AW', 'Award'),
        )

    user = models.ForeignKey(User, unique=False)
    award_title = models.CharField(max_length=50)
    link = models.URLField()
    ##associated_doing = ForeignKey(Doing...)
    award_or_mention = models.CharField(max_length=2,
                                        choices=AWARD_OR_MENTION,
                                        default='ME')

class WebsiteModel(models.Model):
    '''
    Holds websites for backboard/me section.
    '''
    user = models.ForeignKey(User, unique=False)
    site_name = models.CharField(max_length=100)
    site_link = models.URLField()
    description = models.CharField(max_length=1000,
                                   blank=True)
    #img = models.ImageField()
    def __unicode__(self):
        return self.site_link

