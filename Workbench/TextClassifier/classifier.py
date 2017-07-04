from google.cloud import translate
import pickle
import json


def read_json(json_name):
    with open(json_name) as data_file:
        data = json.load(data_file, encoding='UTF-8')
    return data


def parse_and_clean_json(data):
    data_training = []
    # TRANSLATE API DOCUMENTATION <https://google-cloud-python.readthedocs.io/en/latest/translate-usage.html>
    translate_client = translate.Client.from_service_account_json('../TextClassifier/client_key.json')
    for text in data:
        # DETECT LANGUAGE
        language = translate_client.detect_language(text['text'])
        # SENTENCE LANGUAGE SAME AS ENGLISH
        if language['language'] != 'en':
            translated = translate_client.translate(text['text'],
                                                    target_language='en',
                                                    format_='text',
                                                    source_language=language['language'])
            sentence = translated['translatedText']
        else:
            sentence = text['text']

        if text["label"] == 'Definicion':
            label = "Definicion"
            data_training.append((sentence, label))
        else:
            data_training.append((sentence, text['label']))

    return data_training


def process_json(json_name):
    data = read_json(json_name)
    data_training = parse_and_clean_json(data)
    return data_training


def open_classifier(classifier_name_file):
    classifier_file = open(classifier_name_file, 'rb')
    classifier = pickle.load(classifier_file)
    classifier_file.close()
    return classifier


def update_classifier_file(file_name_json):
    # OPEN CLASSIFIER
    classifier = open_classifier('../TextClassifier/classifier_bayes.pickle')
    # PROCESS JSON
    training_data = process_json(file_name_json)
    # UPDATE CLASSIFIER
    classifier.update(training_data)
    # SAVE UPDATED CLASSIFIER
    save_file = open('../TextClassifier/classifier_bayes.pickle', 'wb')
    pickle.dump(classifier, save_file)
    save_file.close()


def update_classifier_text(raw_text, classification):
    # TRANSLATE API DOCUMENTATION <https://google-cloud-python.readthedocs.io/en/latest/translate-usage.html>
    print("HOLA")
    translate_client = translate.Client.from_service_account_json('../TextClassifier/client_key.json')
    # DETECT LANGUAGE
    language = translate_client.detect_language(raw_text)
    # SENTENCE LANGUAGE SAME AS ENGLISH
    if language['language'] != 'en':
        translated = translate_client.translate(raw_text,
                                                target_language='en',
                                                format_='text',
                                                source_language=language['language'])
        sentence = translated['translatedText']
    else:
        sentence = raw_text

    # OPEN CLASSIFIER
    classifier = open_classifier('../TextClassifier/classifier_bayes.pickle')
    # FORMAT DATA
    training_data = [(sentence, classification)]
    # UPDATE CLASSIFIER
    classifier.update(training_data)
    # SAVE UPDATED CLASSIFIER
    save_file = open('../TextClassifier/classifier_bayes.pickle', 'wb')
    pickle.dump(classifier, save_file)
    save_file.close()


def classify(classifier_file_name, sentence):
    # TRANSLATE API DOCUMENTATION <https://google-cloud-python.readthedocs.io/en/latest/translate-usage.html>
    translate_client = translate.Client.from_service_account_json('../TextClassifier/client_key.json')
    # DETECT LANGUAGE
    language = translate_client.detect_language(sentence)

    # CLASSIFIER TO USE
    classifier = open_classifier(classifier_file_name)

    # SENTENCE LANGUAGE SAME AS ENGLISH
    if language['language'] == 'en':
        try:
            classified = classifier.classify(sentence)
            return classified
        except:
            classified = 'Default'
            pass
            return classified
    else:
        try:
            translated = translate_client.translate(sentence,
                                                    target_language='en',
                                                    format_='text',
                                                    source_language=language['language'])
            classified = classifier.classify(translated['translatedText'])
            return classified
        except:
            classified = 'Default'
            pass
            return classified
