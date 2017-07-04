from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from app.forms import SignUpForm, ClassifyForm, DocumentForm
from app.models import ScrapedData, ScrapedImage, ScrapedVideo, ScrapUrl
from itertools import chain
from django.db.models import Q
#first change the cwd to the script path
import os
import sys
cwd = os.getcwd()
rpath = cwd + '../../TextClassifier/'
sys.path.append(rpath)
from classifier import classify, update_classifier_file, update_classifier_text
from entities import get_entities, get_urls, separar, juntar, limpieza
from subprocess import Popen, PIPE


def signup(request):
    message = ''
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
            message = 'Datos incorrectos:'
            if form.cleaned_data.get('password1') != form.cleaned_data.get('password2'):
                message += ' Passwords distintas.'
            if form.cleaned_data.get('email') != form.cleaned_data.get('email2'):
                message += ' E-mail distintos.'
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'message':message})


def showdata(request):
    buscador = []
    if request.method == 'POST':
        if "Entrenar" in request.POST:
            registro_a_entrenar = request.POST.getlist('Entrenar')
            info = ScrapedData.objects.get(id=registro_a_entrenar[0])
            info.data_entrenamiento = True
            info.save()
            update_classifier_text(info.information, info.classification)

        tags_to_delete = request.POST.getlist('tags')
        tags_to_add = request.POST.getlist('Tagx')
        link = request.POST.getlist('Linkx')
        classification_to_change = request.POST.getlist('type')
        data_id = request.POST.getlist('id')
        buscador = request.POST.getlist('buscador')

        # CHANGE CLASSIFICATION IF:
        if len(classification_to_change) > 0:
            ScrapedData.objects.filter(id=data_id[0]).update(classification=classification_to_change[0])

        #DELETE TAGS IF
        if len(tags_to_delete) > 0:
            data = ScrapedData.objects.filter(id=data_id[0])
            existing_tags = separar(data[0].tags)
            existing_metadata = separar(data[0].metadata)
            new_tags, new_metadata = delete_tags_from_data(tags_to_delete, existing_tags, existing_metadata)
            new_tags_str = juntar(new_tags)
            new_metadata_str = juntar(new_metadata)
            ScrapedData.objects.filter(id=data_id[0]).update(tags=new_tags_str,
                                                             metadata=new_metadata_str)
        #ADD TAGS IF
        if len(tags_to_add) > 0:
            data = ScrapedData.objects.filter(id=data_id[0])
            if len(link[0]) == 0:
                existing_tags_a, existing_metadata_a = add_tags_from_data(tags_to_add[0], "None", data[0].tags,
                                                                          data[0].metadata)
            else:
                existing_tags_a, existing_metadata_a = add_tags_from_data(tags_to_add[0], link[0], data[0].tags,
                                                                          data[0].metadata)
            ScrapedData.objects.filter(id=data_id[0]).update(tags=existing_tags_a,
                                                             metadata=existing_metadata_a)

    all_data = ScrapedData.objects.all()
    tags_metadata = ScrapedData.objects.values_list('tags', 'metadata', flat=False)
    references = []
    if buscador:
        all_data = ScrapedData.objects.all().filter(Q(tags__icontains=buscador[0]) | Q(classification__icontains=buscador[0]))
        tags_metadata = all_data.values_list('tags', 'metadata', flat=False)
    for tag, metadata in tags_metadata:
        references.append((separar(tag), separar(metadata)))
    all_info = zip(all_data, references)
    return render(request, 'showdata.html', {'all_data': all_info})


def imagenes(request):
    buscador = []
    if request.method == 'POST':
        tags_to_delete = request.POST.getlist('tags')
        tags_to_add = request.POST.getlist('Tagx')
        data_id = request.POST.getlist('id')
        buscador = request.POST.getlist('buscador')
        if len(tags_to_delete) > 0:
            data = ScrapedImage.objects.filter(id=data_id[0])
            existing_tags = separar(data[0].tags)
            new_tags = delete_tags_from_img(tags_to_delete, existing_tags)
            new_tags_str = juntar(new_tags)
            ScrapedImage.objects.filter(id=data_id[0]).update(tags=new_tags_str)
        # ADD TAGS IF
        if len(tags_to_add) > 0:
            data = ScrapedImage.objects.filter(id=data_id[0])
            existing_tags = separar(data[0].tags)
            existing_tags.append(tags_to_add[0])
            new_tags_str = juntar(existing_tags)
            ScrapedImage.objects.filter(id=data_id[0]).update(tags=new_tags_str)

    all_img = ScrapedImage.objects.all()
    tags = ScrapedImage.objects.values_list('tags', flat=False)
    keywords = []
    if buscador:
        all_img = ScrapedImage.objects.all().filter(Q(tags__icontains=buscador[0]))
        tags = all_img.values_list('tags',flat=False)
    for tag in tags:
        keywords.append(separar(tag[0]))
    all_info = zip(all_img, keywords)
    return render(request, 'imagenes.html', {'all_data': all_info})


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


def urls(request):
    if request.method == 'POST':
        if "Url_annadida" in request.POST:
            urls = request.POST.getlist('Url_annadida')
            print(urls[0])
            if urls[0]:
                if request.POST.getlist('Url_annadida'):
                    U = ScrapUrl(url=urls[0], propagacion_interna=False)
                    U.save()
        if "eliminar_url" in request.POST:
            url_a_eliminar = request.POST.getlist('eliminar_url')
            for url in url_a_eliminar:
                u = ScrapUrl.objects.get(id=url)
                u.delete()
        if "extraer" in request.POST:
            process = Popen(['scrapy','crawl', 'quotes'],cwd= cwd + "../../ScrapyProject/", stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            print(stderr)
            print(stdout)

    all_info = ScrapUrl.objects.all()
    return render(request, 'urls.html', {'all_data': all_info})


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
    message = ''
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            filename = str(request.FILES['document'])
            if filename.endswith('.json'):
                form.save()
                file_path = 'C:/Users/SimónContreras/Downloads/Classer099/Workbench/DjangoProject/media/documents' + filename
                #update_classifier_file(file_path)
                message = 'Subida Exitosa'
                render(request, 'upload_document.html', {'form': form, 'message': message})
            else:
                form = DocumentForm()
                message = 'Formato no compatible'
                render(request, 'upload_document.html', {'form': form, 'message': message})
        else:
            form = DocumentForm()
            message = "Un error ha ocurrido, vuelve a intentar"
    else:
        form = DocumentForm()
    return render(request, 'upload_document.html', {'form': form, 'message': message})


def show_videos(request):
    all_videos = ScrapedVideo.objects.all()
    return render(request, 'videos.html', {'all_videos': all_videos})


def delete_tags_from_data(tags_to_delete, tags, metadata):
    for tag1 in tags_to_delete:
        for tag2 in tags:
            if tag1 == tag2:
                index = tags.index(tag2)
                tags.remove(tag2)
                del metadata[index]
    return tags, metadata


def delete_tags_from_img(tags_to_delete, tags):
    for tag1 in tags_to_delete:
        for tag2 in tags:
            if tag1 == tag2:
                tags.remove(tag1)
    return tags


def add_tags_from_data(tag_to_add, link, tags, metadata):
    lista = separar(tags)
    lista.append(tag_to_add)
    lista2 = separar(metadata)
    lista2.append('https://'+link)
    return juntar(lista), juntar(lista2)





