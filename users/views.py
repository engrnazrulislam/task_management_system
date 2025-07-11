from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from users.forms import RegisterForm, CustomRegistrationForm
from users.forms import LoginForm

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

def sign_in(request):
    # print(request.POST)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html')

    # form = LoginForm()
    # if request.method == 'POST':
    #     form = LoginForm(data=request.POST)
    #     if form.is_valid():
    #         user = form.get_user()
    #         login(request, user)
    #         return redirect('home')
    return render(request, 'registration/login.html', {'form': form})

# logout implementation
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('sign_in')