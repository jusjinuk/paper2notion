from argument import args
from PyPDF2 import PdfFileReader
from glob import glob
import os
from mine import getTitle, getAuthor
import re
from datetime import datetime


class PaperRecord():

    def __init__(self,
                 file='Unknown File',
                 title='Unknown Title',
                 author='Unknown Authors',
                 year=-1):
        self.file = file
        self.title = title
        self.author = author
        self.year = int(year)

    def __str__(self) -> str:
        return f"""
    File : {self.file}
    Title : {self.title}
    Author : {self.author}
    Year : {self.year}
        """

    def __repr__(self) -> str:
        return f"PaperRecord('{self.file}')"


def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                  lambda word: word.group(0).capitalize(), s)


def find_ext(dr, ext):
    return glob(os.path.join(dr, "*.{}".format(ext)))


def read_path(path, verbose=True):
    papers = []
    if os.path.isdir(path):
        lst = find_ext(path, "pdf")
        for f in lst:
            title, author, year = get_info(f)
            _, filename = os.path.split(f)
            rec = PaperRecord(filename, title, author, year)
            print(rec)
            papers.append(rec)

    elif os.path.isfile(path):
        title, author, year = get_info(path)
        _, filename = os.path.split(path)
        rec = PaperRecord(filename, title, author, year)
        print(rec)
        papers.append(rec)

    return papers


def get_info(pdf):
    if os.path.isfile(pdf):
        with open(pdf, 'rb') as f:
            file = PdfFileReader(f)
            info = file.getDocumentInfo()
    else:
        print('File does not exist\n')

    try:
        if (not any(c.isalpha() for c in info.title)):
            title = titlecase(getTitle(pdf))
        else:
            title = info.title
    except TypeError:
        title = titlecase(getTitle(pdf))

    try:
        if (not any(c.isalpha() for c in info.author)):
            author = getAuthor(pdf)
        else:
            author = info.author
    except TypeError:
        author = getAuthor(pdf)

    try:
        raw = info['/CreationDate']
        year = raw[2:6]
    except:
        _, filename = os.path.split(pdf)
        srch = re.search('[1-3][0-9]{3}', filename)
        if (bool(srch)):
            year = srch.group(0)
        else:
            year = -1
    # print(info)

    if (not any(c.isalpha() for c in title)):
        title = "Unknown Title"
    if (not any(c.isalpha() for c in author)):
        author = "Unknown Authors"

    return title, author, year


def main():
    lst = read_path(args.path)
    from notion_api import upload_paper
    print(lst)
    for paper in lst:
        upload_paper(paper)


if __name__ == "__main__":
    main()
