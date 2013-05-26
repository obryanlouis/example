from django.contrib.auth.models import User
from riotry_homepage.models import Rioter
from backboard_general.models import Library, TextItem, ImageItem, AudioItem, VideoItem
import backboard_general.utils as utils

def handle_uploaded_profile_pic(request):
    user_profile = Rioter.objects.get(user__username__exact=request.user.username) # get appropriate Rioter model instance (ie. user_profile)
    original = request.FILES['profile_pic'] # user-uploaded profile_pic file
    (square_200, thumbnail) = utils.create_sizes_profile_pic(original) # creates a 200x200 square from the original, and a 32x32 thumbnail
    user_profile.profile_pic_original = original
    user_profile.profile_pic_square_200 = square_200
    user_profile.profile_pic_thumbnail = thumbnail
    user_profile.save()
    return user_profile.profile_pic_square_200

def handle_uploaded_text(request, form):
    user = User.objects.get(username=request.user.username)
    library = Library.objects.get(user=user)
    full_text = form.cleaned_data['t_body']
    if len(full_text) > 5000:
        words_list = full_text.split()
        words_per_page = 1000
        pages = [' '.join(words_list[x:x+words_per_page]) for x in xrange(0, len(words_list), words_per_page)]
        # pks = []
        for i, page in enumerate(pages):
            divided_text_block = TextItem.objects.create(user=user,
                                                         library=library,
                                                         t_title='%s (page %d)' % (form.cleaned_data['t_title'], i+1),
                                                         t_body=page,
                                                         t_icon="temp_images/t.jpg")
                                    
            divided_text_block.save()
            # pks.append(divided_text_block.pk)
        # return pks
    else:
        single_text_block = TextItem.objects.create(user=user,
                                                    library=library,
                                                    t_title=form.cleaned_data['t_title'],
                                                    t_body=full_text,
                                                    t_icon="temp_images/t.jpg")
        single_text_block.save()
        # return single_text_block.pk
        
        

def handle_uploaded_images(request):
    user = User.objects.get(username=request.user.username)
    library = Library.objects.get(user=user)
    img_pks = []
    for f in request.FILES.getlist('images'):
        original = f # user-uploaded img item
        (img_big, img_363, img_186) = utils.create_sizes_img_item(original)
        img_item = ImageItem.objects.create(user=user, library=library, img_big = img_big, img_363=img_363, img_186=img_186)
        img_item.save()
        img_pks.append(img_item.pk)
    return img_pks

def handle_uploaded_audio(request):
    user = User.objects.get(username=request.user.username)
    library = Library.objects.get(user=user)
    original = request.FILES['audio_file']
    aud_item = AudioItem.objects.create(user=user, library=library, audio_file=original, a_icon="temp_images/a.jpg")
    aud_item.save()
    return aud_item.pk
    #ext = os.path.splitext(original.name)[1]
    #destination = open('some/file/name%s'%(ext), 'wb+')
    #for chunk in f.chunks():
    #    destination.write(chunk)
    #destination.close()

def handle_uploaded_video(request):
    user = User.objects.get(username=request.user.username)
    library = Library.objects.get(user=user)
    original = request.FILES['video_file']
    vid_item = VideoItem.objects.create(user=user, library=library, video_file=original, v_icon="temp_images/v.jpg")
    vid_item.save()
    return vid_item.pk
    
