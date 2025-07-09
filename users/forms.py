from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re

class RegisterForm(UserCreationForm):
    class Meta:
            model = User
            fields = ['username','first_name','last_name','password1','password2','email']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        # set helptext = none in all field
        # by using loop get all fields
        for fieldname in ['username','password1','password2']:
            self.fields[fieldname].help_text = None
        
# Customized Registration Forms:
class CustomRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput) # Here is not found any password field. 
    #So we use wigets which is used to unreadable password
    confirmed_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','confirmed_password','email']

        # Now we make some clean method for validation

        def clean_password1(self):
            password1 = self.cleaned_data.get('password1')

            if len(password1) < 8:
                 raise forms.ValidationError('Password must be 8 character long')
            
            if re.fullmatch(r'A-Za-z0-9#$%@+='):
                 raise forms.ValidationError('Password must contain uppercase, lowercase, min 8 character')
            

