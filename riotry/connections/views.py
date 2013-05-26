from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from connections.forms import ConnectionForm, EditConnectionForm
from connections.models import ConnectionModel
from django.template import RequestContext
from django.contrib.auth.models import User

def MakeConnection(request):
    '''
    Temporary view that allows the logged in user
    to make a connection to another user, by inputting
    the other user's username.
    '''
    user = request.user
    
    friends = [] # empty list for User.usernames of people with which user has a connection 
    connections_i = ConnectionModel.objects.filter(initiator=user) # connections in which user is initiator
    connections_they = ConnectionModel.objects.filter(recipient=user) # connections in which user is recipient
    for connection in connections_i:
        friends.append(connection.recipient.username) # the "other" guy in the connection
    for connection in connections_they:
        friends.append(connection.initiator.username) # the "other" guy in the connection
    
    # if the user has submitted form....
    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            friend_to_be = User.objects.get(username=form.cleaned_data['recipient_username']) # this form is to make a connection, thus the user is always the initiator, and the "other guy" is always the recipient.
            new_connection = ConnectionModel.objects.create(initiator=user,
                                                            recipient=friend_to_be,
                                                            initiator_interest=form.cleaned_data['interest'], # will have to be recipient_interest when "responding" to a oonnection notification
                                                            # all other fields have default specifications in the model
                                                            )
            new_connection.save()
            return HttpResponseRedirect('/connections/make_connection/')
    else:
        form = ConnectionForm(user=user, friends=friends) # unbound form, with everyone in the network who is NOT friends with the user, as choices for users to befriend.
    return render_to_response('make_connection.html', {'form': form, 'connections_i': connections_i, 'connections_they': connections_they}, context_instance=RequestContext(request))


def EditConnection(request, item_id):
    '''
    Temporary view that allows a logged in user
    to edit a connection to another user (blocking (not yet implemented),
    changing user's interest, removing connection)
    '''
    user = request.user
    connection = ConnectionModel.objects.get(pk=item_id) # item to be edited
    
    #if user has submitted the form....
    if request.method == 'POST':
        form = EditConnectionForm(request.POST) # bound with POST data
        if form.is_valid():
            if connection.initiator == user:
                connection.initiator_interest = form.cleaned_data['interest'] # edit the user's interest...aka, the initiator_interest
            else:
                connection.recipient_interest = form.cleaned_data['interest'] # edit the user's interest...aka, the recipient_interest
            connection.save()
            return HttpResponseRedirect('/connections/make_connection/')
        else:
            # to-do...redirect to error page
            raise Exception
    else:
        # we'll pass established_interest into edit_connection.html, to use as value in <input name="interest">
        if connection.initiator == user:
            established_interest = connection.initiator_interest # display the user's interset...aka, the initiator_interest
        else:
            established_interest = connection.recipient_interest # display the user's interest...aka, the recipient_interest
        form = EditConnectionForm() # unbound form
    return render_to_response('edit_connection.html', {'form': form, 'established_interest': established_interest}, context_instance=RequestContext(request))


def DeleteConnection(request, item_id):
    '''
    View to delete an existing connection to
    another user.
    '''
    ConnectionModel.objects.get(pk=item_id).delete()
    return HttpResponseRedirect('/connections/make_connection/')


def BlockUser(request, item_id):
    '''

    '''
    pass
