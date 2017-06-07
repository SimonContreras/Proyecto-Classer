from google.cloud import translate
from textblob.classifiers import NaiveBayesClassifier
import pickle


def create_classifier(training_data):
    classifier = NaiveBayesClassifier(training_data)

    return classifier


def open_classifier(classifier_name_file):
    classifier_file = open(classifier_name_file, 'rb')
    classifier = pickle.load(classifier_file)
    classifier_file.close()
    return classifier


def update_classifier(classifier, file_name_classifier, training_data):
    updated_classifier = classifier.update(training_data)
    save_file = open(file_name_classifier, 'wb')
    pickle.dump(updated_classifier, save_file)
    save_file.close()
    return updated_classifier


def classify(classifier_file_name, sentence):
    # TRANSLATE API DOCUMENTATION <https://google-cloud-python.readthedocs.io/en/latest/translate-usage.html>
    translate_client = translate.Client.from_service_account_json('../TextClassifier/client_key.json')
    #DETECT LANGUAGE
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
