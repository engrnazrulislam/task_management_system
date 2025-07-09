from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import RegisterForm, CustomRegistrationForm

# Create your views here.
def sign_up(request):
    if request.method == 'GET': 
        # form = RegisterForm() # Previous use form
        form = CustomRegistrationForm() # Now use custom registration form
    elif request.method == 'POST':
        # form = RegisterForm(request.POST) # Previous use
        form = CustomRegistrationForm(request.POST) # Now use custom registration form
        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
        #     username = form.cleaned_data.get('username')
        #     password = form.cleaned_data.get('password1')
        #     confirmed_password = form.cleaned_data.get('password2')

        #     if password == confirmed_password:
        #         User.objects.create(username = username, password = confirmed_password)
        #     else:
        #         print('Password are not same')
        # else:
        #     print('Form is not valid')
            
    return render(request,'registration/register.html',{'form':form})