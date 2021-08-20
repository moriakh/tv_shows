from django.shortcuts import render, HttpResponse, redirect
from tv_shows.models import Shows, Networks

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

    s_title = request.POST['title']
    s_release_date = request.POST['release_date']
    s_desc = request.POST['desc']
    show = Shows.objects.create(title = s_title, release_date = s_release_date, desc = s_desc)
    show.networks.add(network)
    return redirect(request.META.get('HTTP_REFERER'))

def destroy(request, tv_show_id):
    show = Shows.objects.get(id=tv_show_id)
    show.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def update(request, tv_show_id):
    network_id = request.POST['network_id']
    network = Networks.objects.get(id=network_id)

    show = Shows.objects.get(id=tv_show_id)
    show_title = request.POST['title']
    show_date = request.POST['date']
    show_desc = request.POST['desc']
    show.title = show_title
    show.release_date = show_date
    show.desc = show_desc
    show.networks.add(network)
    show.save()
    return redirect(request.META.get('HTTP_REFERER'))

