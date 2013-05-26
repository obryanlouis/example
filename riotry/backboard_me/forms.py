from django import forms
from backboard_me.models import AwardModel # for AwardModel.choices used in AwardForm

class TitleForm(forms.Form):
    '''
    A form used by views to submit or edit a job title
    on the backboard/me/#titles section.
    '''
    job_title = forms.CharField(label='Job Title or Position')
    organization = forms.CharField(label='Organization')
    website = forms.CharField(label='Link to Website')
    description = forms.CharField(label='Description of your role and accomplishments while working there')
    location = forms.CharField(label='City and State of Workplace')
    start_date = forms.DateField(label='Start Date (example: 07/25/1990)')
    end_date = forms.DateField(label='End Date (example: 07/25/2013)')

class AwardForm(forms.Form):
    '''
    A form used by views to submit or edit an award_or_mention
    on the backboard/me/#awards_or_mentions section.

    
    '''
    award_title = forms.CharField(label='Title of Award, Article, or Publication')
    link = forms.URLField(label='Link')
    ##associated_doing = Choices of User's doings???
    award_or_mention = forms.ChoiceField(label='Was it an award, or did you get featured/mentioned somewhere?',
                                         choices=AwardModel.AWARD_OR_MENTION)    

class WebsiteForm(forms.Form):
    '''
    A form used by views to submit or edit a website
    on the backboard/me/#websites section.
    '''
    site_name = forms.CharField(label='Name of site')
    site_link = forms.URLField(label='Link')
    description = forms.CharField(label="What is this site's relationship to you? (optional)",
                                  required=False)
    #img = forms.ImageField(label='Image for link (optional)', required=False)
