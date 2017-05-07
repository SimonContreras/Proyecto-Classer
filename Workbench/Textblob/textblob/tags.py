from textblob.classifiers import NaiveBayesClassifier

train = [
('Gauss', 'Gauss'),
('Electricidad', 'Electricidad'),
]

test = [
    ('La ley de Gauss habla sobre el flujo electrico', 'Gauss'),
    ('Cuando se calcula flujo electrico, se usa la ley de Gauss', 'Gauss'),
]

cl = NaiveBayesClassifier(train)

print(cl.classify('La ley de Gauss habla sobre el flujo electrico'))
# cuando separo palabras si son dos oraciones y no hhay punto entre palabras quedan unidas
# ejemplo "... feo" "explicito" -> feoexplicito

# cuando quiero separar por oraciones, debe ir un punto y luego un espacio, sino no las separa