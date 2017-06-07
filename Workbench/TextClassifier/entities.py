from google.cloud import language, translate
import os

cwd = os.getcwd()

def limpieza(lista):
    lista2 = []
    for elem in lista:
        if elem not in lista2:
            lista2.append(elem)
    return lista2


def juntar(lista):
    cadena = ""
    for tipo in lista:
        if lista[-1] != tipo:
            cadena += tipo+","
        else:
            cadena += tipo+","
    return cadena


def juntarDic(lista):
    cadena = ""
    for elem in lista:
        if len(elem.items()) != 0:
            cadena += elem.items()[0][1] + ","
    return cadena[:-1]


def separar(cadena):
    cadena2 = cadena.split(",")
    del cadena2[-1]
    return cadena2


def get_entities(sentence):
    names = []
    metadata = []

    # TRANSLATE API DOCS <https://google-cloud-python.readthedocs.io/en/latest/translate-usage.html>
    translate_client = translate.Client.from_service_account_json(
        '../TextClassifier/client_key.json')
    # NATURAL LANG API DOCS <https://googlecloudplatform.github.io/google-cloud-python/stable/language-usage.html>
    language_client = language.Client.from_service_account_json(
        '../TextClassifier/client_key.json')

    # DETECT LANGUAGE
    language_sentence = translate_client.detect_language(sentence)

    if language_sentence['language'] == 'es':
        try:
            document = language_client.document_from_text(sentence, language='es')
            entity_response = document.analyze_entities()

            for entity in entity_response.entities:
                names.append(entity.name)
                metadata.append(entity.metadata)
            return names, metadata
        except:
            names = ['Default']
            metadata = ['Default']
            return names, metadata
    elif language_sentence['language'] == 'en':
        try:
            document = language_client.document_from_text(sentence)
            entity_response = document.analyze_entities()

            for entity in entity_response.entities:
                translated_name = translate_client.translate(entity.name, target_language='es', format_='text',
                                                             source_language='en')
                names.append(translated_name['translatedText'])
                metadata.append(entity.metadata)
            return names, metadata
        except:
            names = ['Default']
            metadata = ['Default']
            return names, metadata
    else:
        try:
            translated = translate_client.translate(sentence, target_language='en', format_='text',
                                                    source_language=language_sentence['language'])
            document = language_client.document_from_text(translated['translatedText'])
            entity_response = document.analyze_entities()

            for entity in entity_response.entities:
                translated_name = translate_client.translate(entity.name, target_language='es', format_='text',
                                                             source_language='en')
                names.append(translated_name['translatedText'])
                metadata.append(entity.metadata)
            return names, metadata
        except:
            names = ['Default']
            metadata = ['Default']
            return names, metadata


def get_urls(metadata):
    urls = []
    for dic in metadata:
        if 'wikipedia_url' in dic:
            urls.append(dic['wikipedia_url'])
        else:
            urls.append('None')
    merged = juntar(urls)
    return merged



