from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from riotry_homepage.models import Rioter
from backboard_general.models import Library
from django.template import RequestContext
from riotry_homepage.forms import *
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import Http404
import random, string
from django import forms



def LoginRegister(request, toggle='log'):
    if request.user.is_authenticated() and request.user.is_active == True:
        return HttpResponseRedirect('/backboard/')
    if request.method == 'POST':
        if 'log_sub' in request.POST:
            login_form = LoginForm(request.POST) # Bound LoginForm
            register_form = RegisterForm() # Unbound RegisterForm
            if not login_form.has_changed():
                l_fill_form_error =  'Please fill out the form'
                return render_to_response('index.html', {'login_form': login_form, 'register_form': register_form, 'l_fill_form_error': l_fill_form_error}, context_instance=RequestContext(request))
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username=username, password=password) ## might have to be user.email, user.password (referencing foreign key fields)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/backboard/')
                    else:
                        request.session['username'] = username
                        return HttpResponseRedirect('/registration/must_activate/')
                else:
                    u_and_p_error = "Username and password did not match"
                    return render_to_response('index.html', {'login_form': login_form, 'register_form': register_form, 'u_and_p_error': u_and_p_error}, context_instance=RequestContext(request))
            else:
                return render_to_response('index.html', {'login_form': login_form, 'register_form': register_form}, context_instance=RequestContext(request))
        elif 'reg_sub' in request.POST:
            login_form = LoginForm() # Unbound LoginForm
            register_form = RegisterForm(request.POST) # Bound RegisterForm
            if not register_form.has_changed():
                r_fill_form_error =  'Please fill out the form'
                return render_to_response('index.html', {'login_form': login_form, 'register_form': register_form, 'r_fill_form_error': r_fill_form_error}, context_instance=RequestContext(request))
            if register_form.is_valid(): # All validation rules pass, create user/rioter objects on RegisterPlus view
                email = register_form.cleaned_data['email']
                username = register_form.cleaned_data['username']
                password = register_form.cleaned_data['password']
                request.session['email'] = email
                request.session['username'] = username
                request.session['password'] = password
                #return redirect('RegisterPlus', 'email': email, 'username': username, 'password': password, 'register_form': register_form}, context_instance=RequestContext(request))
                return HttpResponseRedirect('/registration')
            else:
                return render_to_response('index.html', {'login_form': login_form, 'register_form': register_form} , context_instance=RequestContext(request))
    elif toggle == 'reg':
        '''user is not submitting form, show them a blank login/registration form'''
        login_form = LoginForm() # An unbound form
        register_form = RegisterForm() # An unbound form
        context = {'login_form': login_form, 'register_form': register_form, 'toggle': toggle}
        return render_to_response('index.html', context, context_instance=RequestContext(request))
    else:
        '''user is not submitting form, show them a blank login/registration form'''
        login_form = LoginForm() # An unbound form
        register_form = RegisterForm() # An unbound form
        context = {'login_form': login_form, 'register_form': register_form}
        return render_to_response('index.html', context, context_instance=RequestContext(request))

def Profile(request):
    username = request.user.username
    profilepic = request.user.rioter.profile_pic_original
    profilepic200 = request.user.rioter.profile_pic_square_200
    thumbnail = request.user.rioter.profile_pic_thumbnail
    context = {'username': username, 'profilepic': profilepic, 'profilepic200': profilepic200, 'thumbnail': thumbnail}
    return render_to_response('profile.html', context, context_instance=RequestContext(request))

#@login_required
#def Profile(request):
#        if not request.user.is_authenticated():
#                return HttpResponseRedirect('/homepage/')
#        rioter = request.user.get_profile() #we definied our get_profile() as person.Person in the AUTH_PROFILE_MODULE of the settings.py file
#        context= {'rioter': rioter}
#        return render_to_response('profile.html', context, context_instance=RequestContext(request))

def RegisterPlus(request):
    #if not user.is_authenticated():
    #    return "You're not authenticated...how'd you get here?"
    if request.method == 'POST':
        if 'reg_plus_sub' in request.POST:
            register_plus_form = RegisterPlusForm(request.POST) # A form bound to the POST data
            if register_plus_form.is_valid(): # All validation rules pass
                email = request.session['email']
                username = request.session['username']
                password = request.session['password']
                date_of_birth = "%s-%s-%s" % (str(register_plus_form.cleaned_data['b_year']), str(register_plus_form.cleaned_data['b_month']), str(register_plus_form.cleaned_data['b_day']))

                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password)
                user.is_active = False
                
                user.first_name = register_plus_form.cleaned_data['first_name']
                user.last_name = register_plus_form.cleaned_data['last_name']
                
                rioter = Rioter.objects.create(user=user, gender=register_plus_form.cleaned_data['gender'],
                                middle_name=register_plus_form.cleaned_data['middle_name'],
                                city=register_plus_form.cleaned_data['city'],
                                state=register_plus_form.cleaned_data['state'],
                                country=register_plus_form.cleaned_data['country'],
                                dob=date_of_birth,
                                activation_key=''.join(random.choice(string.ascii_uppercase + string.digits) for n in range(20))
                                )
                library = Library.objects.create(user=user)
                recipient_list = []
                recipient_list.append(user.email)
                send_mail('Riotry Activation Code',
                          'Please visit http://127.0.0.1:8000/registration/activate/%s/ to active your account.' % (rioter.activation_key),
                          'riotrytest@gmail.com',
                          recipient_list)

                user.save()
                rioter.save()
                library.save()

                return HttpResponseRedirect('/registration/email_sent')

                # u = authenticate(username=username, password=password)
                # login(request, u)
                # return HttpResponseRedirect('/profile')
            else:
                context = {'register_plus_form': register_plus_form}
                return render_to_response('registerplus.html', context, context_instance=RequestContext(request))
    else:
        '''user is not submitting the form, show them a blank registerplus form'''
        register_plus_form = RegisterPlusForm()
        context = {'register_plus_form': register_plus_form}
        return render_to_response('registerplus.html', context, context_instance=RequestContext(request))

def activate_user(request, activation_key):
    try:
        #First, the code tries to look up the user based on the activation key
        user = User.objects.get(rioter__activation_key=activation_key)
        if user.is_active == False:
            #If found, and the user is not active, the user's account is activated.
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user.is_active = True
            user.save()
            login(request, user)
        else:
            #Else, if the user is already active, an error page is passed
            return HttpResponseRedirect('/backboard/')
    except User.DoesNotExist:
        #If no user is found with the activation key, an error page is passed
        return HttpResponseRedirect('/registration/key_not_found')
    return HttpResponseRedirect('/backboard/')

def KeyNotFound(request):
    return render_to_response('key_not_found.html', context_instance=RequestContext(request))

def Activated(request):
    return render_to_response('activated.html', {
        }, context_instance=RequestContext(request))

def MustActivate(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    email = user.email
    return render_to_response('must_activate.html', {'email' : email}, context_instance=RequestContext(request))

def ResendActivationEmail(request):
    if request.user: # if user is authenticated and active (ie, logged in currently)
        return HttpResponseRedirect('/') # send them to their home page
    elif request.session['username']: # elif the user submitted their form during this request, but is not logged in
        username = request.session['username']
        rioter = Rioter.objects.get(user__username=username)

        rioter.activation_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for n in range(20))   
        user.save()
        rioter.save()
        
        recipient_list = []
        recipient_list.append(user.email)
        send_mail('Riotry Activation Code',
                  'Please visit http://127.0.0.1:8000/registration/activate/%s/ to active your account.' % (rioter.activation_key),
                  'riotrytest@gmail.com',
                  recipient_list)
        
        return HttpResponseRedirect('/registration/email_sent')
    else: # else (if this user is not currently logged in, and did not submit a registration form during this request) 
        return HttpResponseRedirect('/r/') # send them to the registration page












def EmailSent(request):
    return render_to_response('email_sent.html', context_instance=RequestContext(request))

def UBuild(request):
    return render_to_response('ubuild.html', context_instance=RequestContext(request))
