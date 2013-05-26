from django import forms
from django.contrib.auth.models import User
from datetime import datetime
import country_choices
from django.forms.util import ErrorList
import re

GENDER_CHOICES = [('placeholder', 'gender'), ('male', 'male'), ('female', 'female')]
MONTH_CHOICES = [('placeholder', 'month'), ('01', '01'), ('02', '02'), ('03', '03'), ('04','04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12')]
DAY_CHOICES = [('placeholder', 'day'), ('01', '01'), ('02', '02'), ('03', '03'), ('04','04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16','16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28','28'), ('29', '29'), ('30', '30'), ('31', '31')]
YEAR_CHOICES = [('placeholder', 'year')] + [(str(i), str(i)) for i in range((datetime.now().year - 10), (datetime.now().year - 100), -1)]
COUNTRY_CHOICES = [('placeholder', 'country')] + country_choices.COUNTRIES 

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username'}),
                               error_messages={'required': 'username required for login'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}),
                               error_messages={'required': 'password required for login'})

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username'}),
                               required=True,
                               max_length=30,
                               min_length=5,
                               error_messages={'required': 'username required',
                                               'max_length': 'username cannot be longer than 30 characters',
                                               'min_length': 'username must be at least 5 characters in length'})
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'email'}),
                             required=True,
                             error_messages={'required': 'email required'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}),
                               required=True,
                               error_messages={'required': 'password required'})
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'retype password'}),
                                      required=True,
                                      error_messages={'required': 'retyped password required'})

    def clean_username(self):
        '''
        Checks to make sure the username is only using alphanumeric characters.
        Checks to make sure this username isn't already associated with an existing account.
        '''
        username = self.cleaned_data['username']
        if username.isalnum() == False:
            raise forms.ValidationError(r"username can only contain letters and numbers")
        try:
             User.objects.get(username=username) # This grabs all objects in User, and checks submitted username against all usernames in the table
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(r"that username is already taken")

    def clean_email(self):
        '''
        Checks to make sure this email isn't already associated with an existing account.
        '''
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(r"an account already exist for this email")

    def clean(self):
        '''
        Checks to make sure password and password_repeat match.
        '''
        super(forms.Form,self).clean()
        if 'password' in self.cleaned_data and 'password_repeat' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password_repeat']:
                # raise forms.ValidationError("The passwords did not match.")
                self._errors['password'] = self._errors.get('password', ErrorList())
                self._errors['password'].append(u'the passwords did not match')
            return self.cleaned_data


class RegisterPlusForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'first', 'tabindex': '1'}),
                                 max_length=30,
                                 min_length=2,
                                 error_messages={'required': 'First name required',
                                                 'max_length': 'First name cannot be longer than 30 characters',
                                                 'min_length': 'Please submit your whole first name'})
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'middle (optional)', 'tabindex': '2'}),
                                  required = False,
                                  max_length=30,
                                  error_messages={'max_length': 'Middle name cannot be longer than 30 characters'})
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'last', 'tabindex': '3'}),
                                max_length=30,
                                min_length=2,
                                error_messages={'required': 'Last name required',
                                                'max_length': 'Last name cannot be longer than 30 characters',
                                                'min_length': 'Please submit your whole last name'})
    gender = forms.CharField(widget=forms.Select(attrs={'class': 'chzn-slct-gender', 'tabindex': '4'}, choices=GENDER_CHOICES))
    b_month = forms.CharField(widget=forms.Select(attrs={'class': 'chzn-slct-month', 'tabindex': '8'}, choices=MONTH_CHOICES))
    b_day = forms.CharField(widget=forms.Select(attrs={'class': 'chzn-slct-day', 'tabindex': '9'}, choices=DAY_CHOICES))
    b_year = forms.CharField(widget=forms.Select(attrs={'class': 'chzn-slct-year', 'tabindex': '10'},choices=YEAR_CHOICES))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'city', 'tabindex': '5'}),
                           min_length=2,
                           max_length=51,
                           error_messages={'required': 'Current city is required',
                                           'min_length': 'Enter full name of city',
                                           'max_length': 'Name of city is too long'})
    state = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'state', 'tabindex': '6'}),
                            required = False)
    country = forms.CharField(widget=forms.Select(attrs={'class': 'chzn-slct-country', 'tabindex': '7'},choices=COUNTRY_CHOICES))

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not re.match("^[a-zA-Z-]+$", first_name):
            raise forms.ValidationError(r"Letters only")
        else:
            return first_name

    def clean_middle_name(self):
        middle_name = self.cleaned_data['middle_name']
        if len(middle_name) > 0:
            if not re.match("^[a-zA-Z-]+$", middle_name):
                raise forms.ValidationError(r"Letters only")
            else:
                return middle_name
        else:
            return middle_name
            
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not re.match("^[a-zA-Z-]+$",last_name):
            raise forms.ValidationError(r"Letters only")
        else:
            return last_name

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        if gender == 'placeholder':
            raise forms.ValidationError(r"Gender required")
        else:
            return gender

    def clean_b_month(self):
        b_month = self.cleaned_data['b_month']
        if b_month == 'placeholder':
            raise forms.ValidationError(r"Full date of birth required")
        else:
            return b_month

    def clean_b_year(self):
        b_year = self.cleaned_data['b_year']
        if b_year == 'placeholder':
            raise forms.ValidationError(r"Full date of birth required")
        else:
            return b_year

    def clean_b_day(self):
        b_day = self.cleaned_data['b_day']
        if b_day == 'placeholder':
            raise forms.ValidationError(r"Full date of birth required")
        else:
            return b_day

    def clean_city(self):
        city = self.cleaned_data['city']
        if len(city) < 2:
            raise forms.ValidationError(r"Please submit the city in which you live or work")
        else:
            return city


    def clean_country(self):
        country = self.cleaned_data['country']
        if country == 'placeholder':
            raise forms.ValidationError(r"Country required")
        else:
            return country

    def clean(self):
        '''
        If `country` is United States, check to make sure `state` has been submitted.
        If `country` is United States and `state` has been submitted, check to make sure it's a 2-letter abbreviation.

        If `country` is not United States, don't require `state` (but accept `state` if they do submit it).

        `country` required regardless.
        '''
        super(forms.Form,self).clean()
        if 'country' in self.cleaned_data:
            if self.cleaned_data['country'] == u'US':
                if 'state' not in self.cleaned_data:
                    self._errors['state'] = self._errors.get('state', ErrorList())
                    self._errors['state'].append(u'State required')
                else:
                    if len(self.cleaned_data['state']) != 2:
                        self._errors['state'] = self._errors.get('state', ErrorList())
                        self._errors['state'].append(u'Examples: CA, NY')
                    else:
                        return self.cleaned_data
            else:
                return self.cleaned_data
