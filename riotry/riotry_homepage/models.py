from django.db import models
from django.contrib.auth.models import User
import datetime
import uuid
import os

def get_file_path(instance, filename):
    '''
    This function creates a filepath and filename for a file object.
    
    It is used in the upload_to parameter of models.ImageField, and so the file
    is uploaded to the created filepath with the created filename.
    '''
    ext = filename.split('.')[-1] # copies existing extension to ext.
    filename = "%s.%s" % (uuid.uuid4(), ext) # creates a random uuid4 string as the filename, then concatenates the ext.
    today = datetime.date.today() # today's date, to be used in "%Y/%m/%d" filepath construction below
    return os.path.join('profile_pics', '%s/%s/%s' % (today.year, today.month, today.day), filename) # returns dynamic relative filepath: /%Year/%month/%day/<filename>

class Rioter(models.Model):    
    user = models.OneToOneField(User, unique=True)
    gender = models.CharField(max_length=10)
    middle_name = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    dob = models.DateField()
    activation_key = models.CharField(max_length=30)
    profile_pic_original = models.ImageField(upload_to=get_file_path,
                                    null=True,
                                    blank=True,)
    profile_pic_square_200 = models.ImageField(upload_to=get_file_path,
                                           null=True,
                                           blank=True)
    profile_pic_thumbnail = models.ImageField(upload_to=get_file_path,
                                           null=True,
                                           blank=True)		

    def __unicode__(self):
        return self.user.email


