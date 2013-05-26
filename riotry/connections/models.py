from django.db import models
from django.contrib.auth.models import User

class ConnectionModel(models.Model):
    CONNECTION_VALUES = [(i,i) for i in range(6)] #Choices 0, 1, 2, 3, 4, 5...'0' is 'no interest'
    
    initiator = models.ForeignKey(User, unique=False, related_name='user_initiator')
    recipient = models.ForeignKey(User, unique=False, related_name='user_recipient')
    initiator_interest = models.IntegerField(choices=CONNECTION_VALUES)
    recipient_interest = models.IntegerField(choices=CONNECTION_VALUES, default=0) # set default to 0
    date = models.DateTimeField(auto_now_add=True)
    initiator_blocking = models.BooleanField(default=False)
    recipient_blocking = models.BooleanField(default=False)

