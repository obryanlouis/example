from django import forms
import os
from backboard_general.models import ImageItem


### LEFT OFF HERE: forms.TextInput / forms.Textarea appear to be SyntaxErrors. Keyword argument repeated??

class UploadTextForm(forms.Form):
    t_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'title',
                                                            'label': 'title'}),
                              max_length=50,
                              required=True)
    t_body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'body',
                                                          'label': 'body'}),
                             required=True)

class UploadImagesForm(forms.Form):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': 'multiple'}),
                             required=True)

    def clean(self):
        files = self.files.getlist('images')
        for file in files:            
            if file:
                if file._size > 15*1024*1024:
                    raise forms.ValidationError("Image file is too large ( > 15mb ).")
                if not file.content_type in ['image/jpeg']: #,'image/gif', 'image/png', 'image/tiff']:
                    raise forms.ValidationError("Sorry, we do not support that video MIME type. Please try uploading a jpeg or png file.")
                return files
            else:
                raise forms.ValidationError("Could not read the uploaded file.")


class UploadAudioForm(forms.Form):
    audio_file = forms.FileField(required=True)

    def clean_audio_file(self):
        '''
        Validates size of file, MIME type, and extension of an audio file.

        Does not (yet) read data for added security of knowing it is, in fact, audio content.
        '''
        file = self.cleaned_data['audio_file']
        if file:
            if file._size > 12*1024*1024:
                print "a"
                raise forms.ValidationError("Audio file is too large ( > 12mb ).")
            #if not file.content_type in ['audio/mpeg', 'audio/mpeg3', 'audio/x-mpeg-3','audio/mp4', 'audio/basic', 'audio/x-midi', 'audio/ogg', 'audio/vorbis', 'audio/x-pn-realaudio', 'audio/vnd.rn-realaudio', 'audio/x-pn-realaudio', 'audio/vnd.rn-realaudio', 'audio/wav', 'audio/x-wav', 'audio/x-m4a']:
            #    print "b"
            #    raise forms.ValidationError("Sorry, we do not support that audio MIME type. Please try uploading an mp3 file, or other common audio type.")
            if not os.path.splitext(file.name)[1] in ['.mp3', '.au', '.midi', '.ogg', '.ra', '.ram', '.wav', '.m4a']:
                print "c"
                raise forms.ValidationError("Sorry, your audio file doesn't have a proper extension.")
            # Here, I want to read the file and make sure it is 
            # a valid audio file. How should I do this? Use a library?
            # Read a portion of the file? ...?
            #
            # EDIT: it appears we should use the audiotools library:
            # http://stackoverflow.com/a/14265226/1337422
            #
            #
            #if not ???.is_audio(file.content):
            #    raise ValidationError("Not a valid audio file.")
            return file
        else:
            raise forms.ValidationError("Could not read the uploaded file.")

class UploadVideoForm(forms.Form):
    video_file = forms.FileField(required=True)

    def clean_video_file(self):
        '''
        Validates size of file, MIME type, and extension of a video file.

        Does not (yet) read data for added security of knowing it is, in fact, video content.
        '''
        file = self.cleaned_data['video_file']
        if file:
            if file._size > 25*1024*1024:
                raise forms.ValidationError("Video file is too large ( > 25mb ).")
            if not file.content_type in ['video/mp4']:#'video/mpeg', 'video/mp4', 'video/ogg', 'video/quicktime', 'video/webm', 'video/x-matroska', 'video/x-ms-wmv', 'video/x-flv']:
                raise forms.ValidationError("Sorry, we do not support that video MIME type. Please try uploading an mp4 file.")
            if not os.path.splitext(file.name)[1] in ['.mp4']:#'.mpg', '.mp4', '.ogg', '.mov', '.wmv', '.swf', '.avi', '.asx', '.asf', '.3g2', '.3gp', '.flv', '.rm', '.vob']:
                raise forms.ValidationError("Sorry, your video file doesn't have an mp4 extension.")
            # Here, I want to read the file and make sure it is 
            # a valid video file. How should I do this? Use a library?
            # Read a portion of the file? ...?
            #if not ???.is_video(file.content):
            #    raise ValidationError("Not a valid video file.")
            return file
        else:
            raise forms.ValidationError("Could not read the uploaded file.")


class UploadProfilePicForm(forms.Form):
    profile_pic = forms.ImageField(label='Select an image',
                                   required=True)


class InfoForImagesForm(forms.ModelForm):
    class Meta:
        model = ImageItem

    def __init__(self, *args, **kwargs):
        super(InfoForImagesForm, self).__init__(*args, **kwargs)
        self.fields['i_caption'].widget = forms.Textarea(attrs={'placeholder': 'caption'})
        
    i_caption = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'caption'}),
                                max_length=1000,
                                required=True)

class InfoForVideoForm(forms.Form):
    v_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'title'}),
                              max_length=50,
                              required=True)
    v_description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'description'}),
                                    max_length=1000,
                                    required=True)

class InfoForAudioForm(forms.Form):
    a_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'title'}),
                              max_length=50,
                              required=True)
    a_description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'description'}),
                                    max_length=1000,
                                    required=True)


