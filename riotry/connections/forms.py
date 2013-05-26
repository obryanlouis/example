from django import forms
from connections.models import ConnectionModel
from django.contrib.auth.models import User

class ConnectionForm(forms.Form):
    '''
    Expects 'user' and 'friends' as kwargs, when
    constructing an 'unbound' form for the user to fill out.
    In this case, __init__generates ConnectionForm['recipient_username'].choices,
    dynamically using the negation of user's existing connections (friends).

    Otherwise (ie. when POSTing), simply pass data like usual.
    '''
    
    def __init__(self, *args, **kwargs):       
        user = kwargs.pop('user', None) # if user is submitted as a kwarg, we pop off the key, return the value, and assign it to user variable, else return user=None      
        friends = kwargs.pop('friends', None) # if friends is submitted as a kwarg, we pop off the key, return the value, and assign it to the friends variable, else return friends=None
        super(ConnectionForm, self).__init__(*args, **kwargs) # inherit original __init__ constructor
        
        if user != None and friends != None: # if user and friends have been passed in as kwargs (ie. to display a blank form with dynamic recipient_username.choices           
            self.fields['recipient_username'] = forms.ChoiceField(choices=[(o, o) for o in User.objects.all().exclude(username__in=friends).exclude(pk=user.id).values_list('username', flat=True)]) # create a ChoiceField 'recipient_username' that has as its choices a list of tuples in the fashion [('User.username', 'User.username'),...] for each User who is not currently connected to 'user'    
        else: # if user and friends are not provided upon construction (ie. Connection(request.POST)):
            self.fields['recipient_username'] = forms.CharField(max_length=100) # create a CharField 'recipient_username', to receive and validate the username POSTed in this field. (we're assuming that submitted username is definitely in the choices_list)
    interest = forms.ChoiceField(label='how interested?', choices=ConnectionModel.CONNECTION_VALUES)

class EditConnectionForm(forms.Form):
    interest = forms.ChoiceField(label='how interested?', choices=ConnectionModel.CONNECTION_VALUES)
