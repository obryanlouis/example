from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from backboard_me.forms import WebsiteForm, TitleForm, AwardForm
from django.contrib.auth.models import User
from backboard_me.models import WebsiteModel, TitleModel, AwardModel
from django.template import RequestContext

##
##======================TITLES============================
##

def TitleView(request):
    '''
    View for the backboard/me/#jobtitles section.

    Generates user's existing instances,
    and generates a form for submitting
    new instances.
    '''
    titles_list = list(TitleModel.objects.filter(user=request.user)) # user's existing titles
    if request.method == 'POST':
        form = TitleForm(request.POST)
        if form.is_valid():
            new_title = TitleModel.objects.create(user=request.user,
                                                  job_title=form.cleaned_data['job_title'],
                                                  organization=form.cleaned_data['organization'],
                                                  website=form.cleaned_data['website'],
                                                  description=form.cleaned_data['description'],
                                                  location=form.cleaned_data['location'],
                                                  start_date=form.cleaned_data['start_date'],
                                                  end_date=form.cleaned_data['end_date']
                                                  )
            new_title.save()
            return HttpResponseRedirect('/backboard/me/title_test/')
        else:
            #error message, form didn't validate
            pass
    else:
        form = TitleForm() # unbound form
    return render_to_response('me_titles_test.html', {'form': form, 'titles_list': titles_list}, context_instance=RequestContext(request))





def EditTitleView(request, item_id):
    '''
    View to handle the editing of an existing
    title entry in the backboard/me section.
    '''
    item = TitleModel.objects.get(pk=item_id) # item to be edited
    if request.method == 'POST':
        form = TitleForm(request.POST)
        if form.is_valid():
            item.job_title = form.cleaned_data['job_title']
            item.organization = form.cleaned_data['organization']
            item.website = form.cleaned_data['website']
            item.description = form.cleaned_data['description']
            item.location = form.cleaned_data['location']
            item.start_date = form.cleaned_data['start_date']
            item.end_date = form.cleaned_data['end_date']

            item.save()
            return HttpResponseRedirect('/backboard/me/title_test/')
        else:
            #error message, form didn't validate
            pass
    else:
        form = TitleForm(item) # form with existing item's data
    return render_to_response('me_titles_edit_test.html', {'form': form, 'item': item}, context_instance=RequestContext(request))





def DeleteTitleView(request, item_id):
    '''
    View to delete an existing title entry
    in the backboard/me section.
    '''
    TitleModel.objects.get(pk=item_id).delete()
    return HttpResponseRedirect('/backboard/me/title_test/')

##
##======================AWARDS============================
##

def AwardView(request):
    '''
    View for the backboard/me/#awards_and_mentions section.

    Generates user's existing instances,
    and generates a form for submitting
    new instances.
    '''
    awards_list = list(AwardModel.objects.filter(user=request.user)) # user's existing awards_or_mentions

    if request.method == 'POST':
        form = AwardForm(request.POST)
        if form.is_valid():
            new_award = AwardModel.objects.create(user=request.user,
                                                  award_title=form.cleaned_data['award_title'],
                                                  link=form.cleaned_data['link'],
                                                  ##associated_doing=form.cleaned_data['associated_doing']
                                                  award_or_mention=form.cleaned_data['award_or_mention']
                                                  )
            new_award.save()
            return HttpResponseRedirect('/backboard/me/award_test/')
        else:
            #error message, form didn't validate
            pass
    else:
        form = AwardForm() # unbound form
    return render_to_response('me_awards_test.html', {'form': form, 'awards_list': awards_list}, context_instance=RequestContext(request))





def EditAwardView(request, item_id):
    '''
    View to handle the editing of an existing award_or_mention
    entry in the backboard/me section.
    '''
    item = AwardModel.objects.get(pk=item_id) # item to be edited
    if request.method == 'POST':
        form = AwardForm(request.POST)
        if form.is_valid():
            item.award_title = form.cleaned_data['award_title']
            item.link = form.cleaned_data['link']
            item.award_or_mention = form.cleaned_data['award_or_mention']

            item.save()
            return HttpResponseRedirect('/backboard/me/award_test/')
        else:
            #error message, form didn't validate
            pass
    else:
        form = AwardForm(item) # form with existing item's data
    return render_to_response('me_awards_edit_test.html', {'form': form, 'item': item}, context_instance=RequestContext(request))





def DeleteAwardView(request, item_id):
    '''
    View to delete an existing award_or_mention
    entry in the backboard/me section.
    '''
    MeAward.objects.get(pk=item_id).delete()
    return HttpResponseRedirect('/backboard/me/award_test/')

##
##======================WEBSITES============================
##

def WebsiteView(request):
    '''
    View for the backboard/me/#websites section.

    Generates user's existing instances,
    and generates a form for submitting
    new instances.
    '''
    websites_list = list(WebsiteModel.objects.filter(user=request.user)) # user's existing websites
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            new_website = WebsiteModel.objects.create(user=request.user,
                                                      site_name=form.cleaned_data['site_name'],
                                                      site_link=form.cleaned_data['site_link'],
                                                      description=form.cleaned_data['description'],
                                                      #img=form.cleaned_data['img']
                                                      )
            new_website.save()
            return HttpResponseRedirect('/backboard/me/website_test/')
        else:
            #error message, form didn't validate
            pass
    else:
        form = WebsiteForm() # unbound form
    return render_to_response('me_websites_test.html', {'form': form, 'websites_list': websites_list}, context_instance=RequestContext(request))





def EditWebsiteView(request, item_id):
    '''
    View to handle the editing of an existing
    website entry in the backboard/me section.
    '''
    item = WebsiteModel.objects.get(pk=item_id) # item to be edited
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            item.site_name = form.cleaned_data['site_name']
            item.site_link = form.cleaned_data['site_link']
            item.description = form.cleaned_data['description']

            item.save()
            return HttpResponseRedirect('/backboard/me/website_test/')
        else:
            #error message, form didn't validate
            pass
    else:
        form = WebsiteForm(item) # form with existing items data
    return render_to_response('me_websites_edit_test.html', {'form': form, 'item': item}, context_instance=RequestContext(request))





def DeleteWebsiteView(request, item_id):
    '''
    View to delete an existing website
    entry in the backboard/me section.
    '''
    WebsiteModel.objects.get(pk=item_id).delete()
    return HttpResponseRedirect('/backboard/me/website_test/')




