from django.shortcuts import render, redirect
from tv_shows.models import Shows, Networks
from django.contrib import messages

def index(request):
    context = {
        'tv_shows': Shows.objects.all()
    }
    return render(request, 'index.html', context)

def show(request, tv_show_id):
    show = Shows.objects.get(id=tv_show_id)
    context = {
        'tv_show' : show
    }
    return render(request, 'show.html', context)

def edit(request, tv_show_id):
    show = Shows.objects.get(id=tv_show_id)
    release_date = show.release_date.strftime('%Y-%m-%d')
    context = {
        'tv_show' : show,
        'release_date' : release_date
    }
    return render(request, 'edit.html', context)

def new_show(request):
    context = {
        'networks' : Networks.objects.all()
    }
    return render(request, 'new_show.html', context)

def add_show(request):
    network_id = int(request.POST['network_id'])
    network = Networks.objects.get(id=network_id)

    errors = Shows.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('../new')
    else:
        s_title = request.POST['title']
        s_release_date = request.POST['release_date']
        s_desc = request.POST['desc']
        show = Shows.objects.create(title = s_title, release_date = s_release_date, desc = s_desc)
        show.networks.add(network)
        messages.success(request, "Show successfully created")

        return redirect('/shows')

def destroy(request, tv_show_id):
    show = Shows.objects.get(id=tv_show_id)
    show.delete()
    return redirect(request.META.get('HTTP_REFERER'))


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

