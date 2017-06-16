from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from app.forms import SignUpForm, ClassifyForm, DocumentForm
from app.models import ScrapedData, ScrapedImage, ScrapedVideo
from itertools import chain
#first change the cwd to the script path
import os
import sys
cwd = os.getcwd()
rpath = cwd + '../../TextClassifier/'
sys.path.append(rpath)
from classifier import classify
from entities import get_entities, get_urls, separar, juntar, limpieza


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
    tags_metadata = ScrapedData.objects.values_list('tags', 'metadata', flat=False)
    references = []
    for tag, metadata in tags_metadata:
        references.append((separar(tag), separar(metadata)))
    all_info = zip(all_data, references)
    return render(request, 'showdata.html', {'all_data': all_info})


def imagenes(request):
    all_img = ScrapedImage.objects.all()
    return render(request, 'imagenes.html', {'all_data': all_img})


def img_in_data(request):
    all_data = ScrapedData.objects.all()
    all_img = ScrapedImage.objects.all()
    result_list = list(chain(all_data, all_img))
    tags = ScrapedData.objects.values_list('tags', 'metadata', flat=False)
    references = []
    for tag, metadata in tags:
        references.append((separar(tag), separar(metadata)))
    return render(request, 'showdata.html', {'result_list': result_list, 'reference': references})


def classify_example(request):
    form = ClassifyForm(request.POST)
    if form.is_valid():
        sentence = form.cleaned_data['sentence']
        classified = classify(rpath + 'classifier_bayes.pickle',
                              sentence)
        args = {'form': form, 'classified': classified}
        return render(request, 'classify_example.html', args)
    else:
        form = SignUpForm()
        args = {'form': form}
        return render(request, 'classify_example.html', args)


def entities_example(request):
    form = ClassifyForm(request.POST)
    if form.is_valid():
        sentence = form.cleaned_data['sentence']
        entities, metadata = get_entities(sentence)
        urls = separar(get_urls(metadata))
        entities_fixed = separar(juntar(limpieza(entities)))

        args = {'form': form, 'entities': entities_fixed, 'urls': urls}
        return render(request, 'entities_example.html', args)
    else:
        form = SignUpForm()
        args = {'form': form}
        return render(request, 'entities_example.html', args)


def file_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            mensaje = 'Subida Exitosa'
            render(request, 'upload_document.html', {'form': form, 'success' : mensaje})
    else:
        form = DocumentForm()
    return render(request, 'upload_document.html', {'form': form})


def show_videos(request):
    all_videos = ScrapedVideo.objects.all()
    return render(request, 'videos.html', {'all_videos': all_videos})
