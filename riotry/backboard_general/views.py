from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from riotry_homepage.models import Rioter
from backboard_general.models import Library, TextItem, ImageItem, VideoItem, AudioItem
from backboard_general.forms import UploadProfilePicForm, UploadTextForm, UploadImagesForm, InfoForImagesForm, UploadAudioForm, UploadVideoForm, InfoForVideoForm, InfoForAudioForm
from django.template import RequestContext
from backboard_general.upload_handlers import handle_uploaded_profile_pic, handle_uploaded_text, handle_uploaded_images, handle_uploaded_audio, handle_uploaded_video
from itertools import chain
import backboard_general.utils as utils
from django.http import HttpResponse
from PIL import Image
from django.forms.models import modelformset_factory
from django.utils import simplejson
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from itertools import chain
from operator import attrgetter

def backboard_main_context(request):
    context = {}
    user = request.user
    context['user'] = user
    context['username'] = user.username
    context['first_name'] = user.first_name
    context['full_name'] = user.first_name + ' ' + user.last_name
    context['profile_pic_square_200'] = user.rioter.profile_pic_square_200
    context['profile_pic_thumbnail'] = user.rioter.profile_pic_thumbnail
    context['toggle'] = False
    return (request, context)


def header_functionality(request, context):
    if request.method == 'POST':
        if 't_title' and 't_body' in request.POST: # using names of UploadTextForm fields to differentiate
            text_form = UploadTextForm(request.POST)
            if text_form.is_valid():
                handle_uploaded_text(request, text_form)
                print "Text Upload Successful"
            else:
                # Instead, we could validate on the front-end, so as not to reload page.
                print 'Validation ERROR @ Text Images' 
        elif 'id_images' in request.POST:
            image_form = UploadImagesForm(request.POST, request.FILES)
            if image_form.is_valid():
                image_pks = handle_uploaded_images(request)
                ImageInfoFormset = modelformset_factory(ImageItem, form=InfoForImagesForm, fields=['i_caption'], extra=0)
                formset = ImageInfoFormset(queryset=ImageItem.objects.filter(pk__in=image_pks)) # TOO MANY VALUES ERROR HERE!
                images_uploaded = ImageItem.objects.filter(pk__in=image_pks).values_list('img_363', flat=True)
                context['toggle'] = 'image_info_modal'
                context['images_and_formset'] = zip(images_uploaded, formset)
            else:
                print 'Validation ERROR @ Upload Image'
        elif 'id_video_file' in request.POST:
            video_form = UploadVideoForm(request.POST, request.FILES)
            if video_form.is_valid():
                video_pk = handle_uploaded_video(request) # File validation is complete, we now write the file to disk
                context['video_info_form'] = InfoForVideoForm()
                context['toggle'] = 'video_info_modal'
                video_icon = VideoItem.objects.filter(pk=video_pk)[0:1].values_list('v_icon', flat=True)
                video_uploaded_list = VideoItem.objects.filter(pk=video_pk)[0:1].values_list('video_file', flat=True)
                context['video_icon'] = video_icon[0]
                context['video_uploaded'] = video_uploaded_list[0]
                request.session['pk_to_edit'] = video_pk
                print "Video Upload Successful"
            else:
                print 'Validation ERROR @ Upload Video'
        elif 'id_audio_file' in request.POST:
            audio_form = UploadAudioForm(request.POST, request.FILES)
            if audio_form.is_valid():
                audio_pk = handle_uploaded_audio(request) # File validation is complete, we now write the file to disk
                context['audio_info_form'] = InfoForAudioForm()
                context['toggle'] = 'audio_info_modal'
                audio_icon = AudioItem.objects.filter(pk=audio_pk)[0:1].values_list('a_icon', flat=True)
                print audio_icon
                context['audio_icon'] = audio_icon[0]
                request.session['pk_to_edit'] = audio_pk
                print "Audio Upload Successful"
            else:
                print 'Validation ERROR @ Upload Audio'
        elif 'id_profile_pic' in request.POST:
            profile_pic_form = UploadProfilePicForm(request.POST, request.FILES)
            if profile_pic_form.is_valid():
                pic_200 = handle_uploaded_profile_pic(request)
                user = context['user']
                context['profile_pic_square_200'] = pic_200
            else:
                print 'Validation ERROR @ Profile Pic'
    ## INFO FORMS
        elif 'i_caption' in request.POST: # these are the fields of InfoForImagesForm
            ImageInfoFormset = modelformset_factory(ImageItem, form=InfoForImagesForm, fields=['caption'], extra=0)
            formset = ImageInfoFormset(request.POST)
            if formset.is_valid():
                formset.save()
                print "Image Info Formset Successful!"
            else:
                print 'Validation ERROR @ Image Info Formset'
        elif 'v_title' and 'v_description' in request.POST:
            v_i_form = InfoForVideoForm(request.POST)
            if v_i_form.is_valid():
                item = VideoItem.objects.get(pk=request.session['pk_to_edit'])
                item.v_title = form.cleaned_data['v_title']
                item.v_description = form.cleaned_data['v_description']
                item.save()
                print "Video Info Form Successful!"
            else:
                print 'Validation ERROR @ Video Info Form'
        elif 'a_title' and 'a_description' in request.POST:
            a_i_form = InfoForAudioForm(request.POST)
            if a_i_form.is_valid():
                item = VideoItem.objects.get(pk=request.session['pk_to_edit'])
                item.a_title = form.cleaned_data['a_title']
                item.a_description = form.cleaned_data['a_description']
                item.save()
                print "Audio Info Form Successful!"
            else:
                print 'Validation ERROR @ Video Info Form'
            
    context['text_form'] = UploadTextForm()
    context['image_form'] = UploadImagesForm()
    context['video_form'] = UploadVideoForm()
    context['audio_form'] = UploadAudioForm()
    context['profile_pic_form'] = UploadProfilePicForm()
    return (request, context)


def Backboard_Home(request):
    request, context = backboard_main_context(request)
    print context['profile_pic_square_200']
    request, context = header_functionality(request, context)
    return render_to_response('backb_base.html', context, context_instance=RequestContext(request))


def LibraryMain(request):
    request, context = backboard_main_context(request)
    request, context = header_functionality(request, context)
    text = TextItem.objects.filter(user=request.user)
    images = ImageItem.objects.filter(user=request.user)
    video = VideoItem.objects.filter(user=request.user)
    audio = AudioItem.objects.filter(user=request.user)
    context['result_list'] = sorted(chain(text, images, video, audio),
                                    key=attrgetter('upload_date'),
                                    reverse=True)
    return render_to_response('library.html', context, context_instance=RequestContext(request))

def DoingsBackboard(request):
    request, context = backboard_main_context(request)
    request, context = header_functionality(request, context)
    return render_to_response('doings.html', context, context_instance=RequestContext(request))


def AddInfoImage(request):
    image_pks = request.session['recently_uploaded']
    InfoForImagesFormset = modelformset_factory(ImageItem, fields=('title', 'caption'), extra=0)
    queryset = ImageItem.objects.filter(pk__in=image_pks)
    images = queryset.values_list('img_363', flat=True)
    if request.method == 'POST':
        formset = InfoForImagesFormset(request.POST)
        if formset.is_valid():
            # do something with formset ##LEFT OFF HERE!!! CURRENTLY, EACH FORM IN THE FORMSET ISN'T CONNECTED TO ANY PARTICULAR INSTANCE OF A MODEL. MAYBE, WE CAN GRAB THE FORM "NUMBERS" AND ASSIGN THEM IN ASCENDING ORDER TO THE IMAGEITEM INSTANCES FROM THE IMAGE_PKS LIST? MIGHT WORK...
             formset.save()
        else:
            # error
            pass
    else:
        formset = InfoForImagesFormset(queryset)
    return render_to_response('image_info.html', {'formset': formset, 'images': images}, context_instance=RequestContext(request))


def AjaxTest(request):
    response_dict = {}
    #response_dict.update(csrf(request))
    if not request.POST: # go straight to a template with an empty context
        return render_to_response('ajax_test.html', response_dict, context_instance=RequestContext(request))
    textinput = request.POST.get('text_input', False)
    response_dict.update({'textinput': textinput})
    if textinput:
        response_dict.update({'success': True})
    else:
        response_dict.update({'errors': {}})
    if request.is_ajax:
        response_dict = simplejson.dumps(response_dict)
        return HttpResponse(response_dict, content_type='application/json')
    return render_to_response('ajax_test.html', response_dict, context_instance=RequestContext(request))

    
