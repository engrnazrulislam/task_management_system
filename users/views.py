from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from users.forms import RegisterForm, CustomRegistrationForm
from users.forms import LoginForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from users.forms import LoginForm
from django.contrib.auth.tokens import default_token_generator

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
            user = form.save(commit=False)
            print('user',user)
            user.set_password(form.cleaned_data.get('password1'))
            print(form.cleaned_data)
            user.is_active = False
            user.save()

            messages.success(request,'A Confirmation mail was sent. Pleas check your email')

            return redirect('sign_in')
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

# def sign_in(request):
#     # print(request.POST)
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(username=username,password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')
#     return render(request, 'registration/login.html')

# implement django authentication form
# def sign_in(request):
#     form = AuthenticationForm()
#     if request.method == "POST":
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')
#     return render(request, 'registration/login.html',{'form':form})
def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html', {'form': form})


# logout implementation
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('sign_in')
    

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign_in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')
