from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from app.forms import SignUpForm
from app.models import ScrapedData, ScrapedImage
from itertools import chain


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('menu')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def showdata(request):
    all_data = ScrapedData.objects.all()
    return render(request, 'showdata.html', {'all_data': all_data})


def imagenes(request):
    all_img = ScrapedImage.objects.all()
    return render(request, 'imagenes.html', {'all_data': all_img})


def img_in_data(request):
    all_data = ScrapedData.objects.all()
    all_img = ScrapedImage.objects.all()
    result_list = list(chain(all_data, all_img))
    return render(request, 'showdata.html', {'result_list': result_list})