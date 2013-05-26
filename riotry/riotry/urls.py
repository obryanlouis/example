# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from backboard_me import views as me_views
from connections import views as connection_views
from django.views.generic.simple import direct_to_template
from riotry_homepage.views import activate_user
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       # homepage (login and registration if not logged in; redirects to backboard otherwise)
                       url(r'^$', 'riotry_homepage.views.LoginRegister'),
                       # homepage, with the registration toggle button on upon arrival
                       url(r'^r/$', 'riotry_homepage.views.LoginRegister', {'toggle': 'reg'}),
                       # registerplus (stage two of registration process. stage 1 is located on the homepage '')
                       url(r'^registration/$', 'riotry_homepage.views.RegisterPlus'),
                       # this is the url sent to users via email to activate their accounts
                       url(r'^registration/activate/([a-zA-Z0-9_.-]+)/$', activate_user),
                       # in case the activation key is incorrect
                       url(r'^registration/key_not_found/$', 'riotry_homepage.views.KeyNotFound'),
                       # activation email sent
                       url(r'^registration/email_sent', 'riotry_homepage.views.EmailSent'),
                       # for users who try to login, using a valid username/password that is not yet activated (ie. they never clicked the email link)
                       url(r'^registration/must_activate/$', 'riotry_homepage.views.MustActivate'),
                       # resends activation email, then immediately renders email_sent.html
                       url(r'^registration/resend_activation_email', 'riotry_homepage.views.ResendActivationEmail'),
                       # backboard, main homepage
                       url(r'^backboard/$', 'backboard_general.views.Backboard_Home'),
                       # takes user to his/her profile page. for now, this is a simple html page with their name on it, a logout link, and a change password link
                       url(r'^profile/$', 'riotry_homepage.views.Profile'),
                       # logs the user out, redirects to the riotry homepage (login/register page)
                       url(r'^logout/$', auth_views.logout, {'next_page': '/'}),
                       # page for changing an old password to a new password (@login required)
                       url(r'^password/change/$', auth_views.password_change),
                       # password change done (simple success page)
                       url(r'^password/change/done/$', auth_views.password_change_done, name='auth_password_change_done'),
                       # password reset (Forgotten your password?)
                       url(r'^password/reset/$', auth_views.password_reset, name='auth_password_reset'),
                       # email has been sent to reset password
                       url(r'^password/reset/done/$', auth_views.password_reset_done, name='auth_password_reset_done'),
                       # link sent in email to reset the password
                       url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='auth_password_reset_confirm'),
                       # password reset complete
                       url(r'^password/reset/complete/$', auth_views.password_reset_complete, name='auth_password_reset_complete'),
                       # temporary profile_pic upload form...for testing.
                       url(r'^upload/profile_pic/$', 'backboard_general.views.UploadProfilePic'),
                       # media url...not typically for direct access (for serving all user-uploaded content)
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       # see all uploaded items, that are not currently being used in a doing
                       url(r'^library/$', 'backboard_general.views.LibraryMain'),
                       # upload text item
                       url(r'^upload_text/$', 'backboard_general.views.UploadText'),
                       # upload image item(s)
                       url(r'^upload_images/$', 'backboard_general.views.UploadImages'),
                       # add title and caption to image item(s)
                       url(r'^upload_images/add_info/$', 'backboard_general.views.AddInfoImage'),
                       # upload audio item
                       url(r'^upload_audio_test/$', 'backboard_general.views.UploadAudioToLibrary'),
                       # upload video item
                       url(r'^upload_video_test/$', 'backboard_general.views.UploadVideoToLibrary'),
                       # add websites to me section
                       url(r'^backboard/me/website_test/$', 'backboard_me.views.WebsiteView'),
                       # edit a website in the me section
                       url(r'^backboard/me/website_test/edit/(?P<item_id>[0-9]+)/$', me_views.EditWebsiteView, name="edit_website"),
                       # delete a website in the me section
                       url(r'^backboard/me/website_test/delete/(?P<item_id>[0-9]+)/$', me_views.DeleteWebsiteView, name="delete_website"),
                       # add a job title/position to me section
                       url(r'^backboard/me/title_test/$', 'backboard_me.views.TitleView'),
                       # edit a job title/position in the me section
                       url(r'^backboard/me/title_test/edit/(?P<item_id>[0-9]+)/$', me_views.EditTitleView, name="edit_title"),
                       # delete a job title/position in the me section
                       url(r'^backboard/me/title_test/delete/(?P<item_id>[0-9]+)/$', me_views.DeleteTitleView, name="delete_title"),
                       # add an award or mention to me section
                       url(r'^backboard/me/award_test/$', 'backboard_me.views.AwardView'),
                       # edit an award or mention in me section
                       url(r'^backboard/me/award_test/edit/(?P<item_id>[0-9]+)/$', me_views.EditAwardView, name="edit_award"),
                       # delete an award or mention in me section
                       url(r'^backboard/me/award_test/delete/(?P<item_id>[0-9]+)/$', me_views.DeleteAwardView, name="delete_award"),
                       # make a "connection" with another user, specify interest
                       url(r'^connections/make_connection/$', 'connections.views.MakeConnection'),
                       # edit an existing connection
                       url(r'^connections/edit_connection/(?P<item_id>[0-9]+)/$',connection_views.EditConnection, name="edit_connection"),
                       # delete an existing connection
                       url(r'^connections/delete_connection/(?P<item_id>[0-9]+)/$', connection_views.DeleteConnection, name="delete_connection"),
                       # testing ajax
                       url(r'^ajax_test/$', 'backboard_general.views.AjaxTest'),
                       # test doings backboard
                       url(r'^doings/backboard/$', 'backboard_general.views.DoingsBackboard'),
                      
)

