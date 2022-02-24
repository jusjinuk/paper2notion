import nltk
import os
from nameparser.parser import HumanName
from nltk.corpus import wordnet


def download_nltk():
    list = [
        'punkt', 'averaged_perceptron_tagger', 'maxent_ne_chunker', 'words',
        'wordnet', 'omw-1.4'
    ]
    dir_nltk = 'nltk_data'
    nltk.data.path.append(os.path.join(os.getcwd(), dir_nltk))
    for l in list:
        nltk.download(l, dir_nltk, quiet=True)


def get_human_names(text):
    person_list = []
    person_names = person_list
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary=False)

    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1:  #avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []

    return person_list, person_names


if __name__ == "__main__":
    download_nltk()

    text = """
    Nothing
    """

    list, names = get_human_names(text)
    for person in list:
        person_split = person.split(" ")
        for name in person_split:
            if wordnet.synsets(name):
                if (name in person):
                    names.remove(person)
                    break

    print(names)