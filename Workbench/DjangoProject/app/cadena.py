tags = ['perro','gato','castor','ardilla','iguana','cocodrilo']
metadata = ['1','2','3','4','5','6']
tags_to_delete = ['perro', 'ardilla']


def delete_tags(tags_to_delete, tags, metadata):
    for tag1 in tags:
        for tag2 in tags_to_delete:
            if tag1 == tag2:
                index = tags.index(tag1)
                tags.remove(tag1)
                del metadata[index]
    return tags, metadata


tags2, metadata2 = delete_tags(tags_to_delete, tags, metadata)
print(tags2)
print(metadata2)

