from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def create(request):
    if request.method == 'POST':
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            this_user = User.objects.create(
                first_name= request.POST['first_name'],
                last_name= request.POST['last_name'],
                email= request.POST['email'],
                password= pw_hash
            )
            request.session['user_id'] = this_user.id
            return redirect('/user/success')
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        user_by_email = User.objects.filter(email=request.POST['email'])
        if user_by_email:
            this_user = user_by_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
                request.session['user_id'] = this_user.id
                return redirect('/user/success')
        messages.error(request, "Email or password are not valid!")
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {'this_user': User.objects.get(id=request.session['user_id'])}
        return render(request, 'success.html', context)

def logout(request):
    request.session.flush()
    return redirect ('/')
