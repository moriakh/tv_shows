import bcrypt
from django.shortcuts import render, redirect
from .models import Shows, Networks, Users
from django.contrib import messages
from .decorators import login_required

@login_required
def index(request):
    context = {
        'tv_shows': Shows.objects.all()
    }
    return render(request, 'index.html', context)

@login_required
def show(request, tv_show_id):
    show = Shows.objects.get(id=tv_show_id)
    context = {
        'tv_show' : show
    }
    return render(request, 'show.html', context)

@login_required
def edit(request, tv_show_id):
    show = Shows.objects.get(id=tv_show_id)
    release_date = show.release_date.strftime('%Y-%m-%d')
    context = {
        'tv_show' : show,
        'release_date' : release_date
    }
    return render(request, 'edit.html', context)

@login_required
def new_show(request):
    context = {
        'networks' : Networks.objects.all()
    }
    return render(request, 'new_show.html', context)

@login_required
def add_show(request):
    network_id = int(request.POST['network_id'])
    network = Networks.objects.get(id=network_id)

    errors = Shows.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('shows/new')
    else:
        s_title = request.POST['title']
        s_release_date = request.POST['release_date']
        s_desc = request.POST['desc']
        show = Shows.objects.create(title = s_title, release_date = s_release_date, desc = s_desc)
        show.networks.add(network)
        messages.success(request, "Show successfully created")

        return redirect('/shows')

@login_required
def destroy(request, tv_show_id):
    show = Shows.objects.get(id=tv_show_id)
    show.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def update(request, tv_show_id):
    network_id = request.POST['network_id']
    network = Networks.objects.get(id=network_id)
    errors = Shows.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'../{tv_show_id}/edit')
    else:
        show = Shows.objects.get(id=tv_show_id)
        show_title = request.POST['title']
        show_date = request.POST['date']
        show_desc = request.POST['desc']
        show.title = show_title
        show.release_date = show_date
        show.desc = show_desc
        show.networks.add(network)
        show.save()
        messages.success(request, "Show successfully updated")
        return redirect('/shows')

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        errors = Users.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, error_message in errors.items():
                messages.error(request, error_message)
            return redirect('/register')
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = Users.objects.create(name = name, email = email, password = password)
        
        request.session['user'] = {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
        messages.success(request, 'User successfully registered')
        return redirect('/shows')


def login(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        user = Users.objects.get(email = email)
    except Users.DoesNotExist:
        messages.error(request, 'The user or password does not exist')
        return redirect('/register')
    
    if  not bcrypt.checkpw(password.encode(), user.password.encode()): 
        messages.error(request, 'The user or password does not exist')
        return redirect('/register')
    
    request.session['user'] = {
        'id': user.id,
        'name': user.name,
        'email': user.email
    }

    messages.success(request, f'Welcome {user.name}')
    return redirect('/shows')


def logout(request):
    del request.session['user']
    return redirect('/register')