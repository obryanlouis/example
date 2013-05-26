from django.db import models
from django.contrib.auth.models import User
import datetime
import uuid
import os

def img_get_file_path(instance, filename):
    '''
    This function creates a filepath and filename for a file object.
    
    It is used in the upload_to parameter of models.ImageField, and so the file
    is uploaded to the created filepath with the created filename.
    '''
    ext = filename.split('.')[-1] # copies existing extension to ext.
    filename = "%s.%s" % (uuid.uuid4(), ext) # creates a random uuid4 string as the filename, then concatenates the ext.
    today = datetime.date.today() # today's date, to be used in "%Y/%m/%d" filepath construction below
    return os.path.join('img_items', '%s/%s/%s' % (today.year, today.month, today.day), filename) # returns dynamic relative filepath: /%Year/%month/%day/<filename>

def aud_get_file_path(instance, filename):
    '''
    This function creates a filepath and filename for a file object.
    
    It is used in the upload_to parameter of models.FileField, and so the file
    is uploaded to the created filepath with the created filename.
    '''

    
    ext = filename.split('.')[-1] # copies existing extension to ext.
    filename = "%s.%s" % (uuid.uuid4(), ext) # creates a random uuid4 string as the filename, then concatenates the ext.
    today = datetime.date.today() # today's date, to be used in "%Y/%m/%d" filepath construction below
    return os.path.join('aud_items', '%s/%s/%s' % (today.year, today.month, today.day), filename) # returns dynamic relative filepath: /%Year/%month/%day/<filename>

def vid_get_file_path(instance, filename):
    '''
    This function creates a filepath and filename for a file object.
    
    It is used in the upload_to parameter of models.FileField, and so the file
    is uploaded to the created filepath with the created filename.
    '''
    ext = filename.split('.')[-1] # copies existing extension to ext.
    filename = "%s.%s" % (uuid.uuid4(), ext) # creates a random uuid4 string as the filename, then concatenates the ext.
    today = datetime.date.today() # today's date, to be used in "%Y/%m/%d" filepath construction below
    return os.path.join('vid_items', '%s/%s/%s' % (today.year, today.month, today.day), filename) # returns dynamic relative filepath: /%Year/%month/%day/<filename>


class Library(models.Model):
    user = models.OneToOneField(User, unique=True)

#class Doing(models.Model):
#    user = models.ForeignKey(User)
    # category
#    title = models.CharField(max_length=100)
    
    

class ImageItem(models.Model):
    user = models.ForeignKey(User)
    upload_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    #doing = models.ForeignKey(Doing,
    #                          blank=True)
    library = models.ForeignKey(Library)
    img_big = models.ImageField(upload_to=img_get_file_path)
    img_363 = models.ImageField(upload_to=img_get_file_path)
    img_186 = models.ImageField(upload_to=img_get_file_path)
    i_caption = models.CharField(max_length=1000,
                                 blank=True)

class AudioItem(models.Model):
    user = models.ForeignKey(User)
    upload_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    #doing = models.ForeignKey(Doing,
    #                          blank=True)
    library = models.ForeignKey(Library)
    audio_file = models.FileField(upload_to=aud_get_file_path)
    a_icon = models.CharField(max_length=200)
    a_title = models.CharField(max_length=50,
                             blank=True)
    a_description = models.CharField(max_length=1000,
                               blank=True)

class VideoItem(models.Model):
    user = models.ForeignKey(User)
    upload_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    #doing = models.ForeignKey(Doing,
    #                          blank=True)
    library = models.ForeignKey(Library)
    video_file = models.FileField(upload_to=vid_get_file_path)
    v_icon = models.CharField(max_length=200)
    v_title = models.CharField(max_length=50,
                             blank=True)
    v_description = models.CharField(max_length=1000,
                               blank=True)

class TextItem(models.Model):
    user = models.ForeignKey(User)
    upload_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    #doing = models.ForeignKey(Doing,
    #                          blank=True)
    library = models.ForeignKey(Library)
    t_icon = models.CharField(max_length=200)
    t_title = models.CharField(max_length=50)
    t_body = models.CharField(max_length=5000)
