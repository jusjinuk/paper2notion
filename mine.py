## Extract title through mining text with biggest font
## Referred To : https://stackoverflow.com/questions/68212263/parsing-the-author-names-of-a-research-paper-using-pdfminer

import sys
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTLine, LTChar
from argument import args


def getTitle(filepath, r=1):
    """method to extract the title of a pdf file"""

    try:
        filepath = filepath.strip()
    except TypeError:
        print("filepath not a string")

    if not filepath[len(filepath) - 4:len(filepath)] == ".pdf":
        sys.exit("filepath not ending with .pdf")

    data = extractFirstPageElements(filepath, verbose=args.verbose)
    texts = data[0]
    fonts = data[1]

    if len(
            texts
    ) == 0:  #in case no text is read, either the pdf text is not readable or first page is blank
        title = "Unknown"
    else:
        maxFontPos = extractTitlePos(fonts, r)
        uncleanedTitle = extractTitle(texts, maxFontPos)
        title = cleanTitle(uncleanedTitle)

    return title


def getAuthor(filepath):
    """method to extract the title of a pdf file"""

    try:
        filepath = filepath.strip()
    except TypeError:
        print("filepath not a string")

    if not filepath[len(filepath) - 4:len(filepath)] == ".pdf":
        sys.exit("filepath not ending with .pdf")

    texts, bolds = extractFirstPageElements(filepath, bold=True)

    if len(
            texts
    ) == 0:  #in case no text is read, either the pdf text is not readable or first page is blank
        title = "Unknown"
    else:
        boldPos = extractAuthorPos(bolds)
        uncleanedTitle = extractAuthor(texts, boldPos)
        title = cleanTitle(uncleanedTitle)

    return title


def extractFirstPageElements(filepath, bold=False, verbose=False):
    """helper method to extract text elements and their corresponding font sizes into lists"""

    fonts = []
    bolds = []
    elements = []
    lines = []
    for page in extract_pages(filepath):
        for element in page:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    for character in text_line:
                        if bold:
                            if isinstance(character, LTChar):
                                bold_fonts = ['SFBX', 'BZYN']
                                # SFBX : ICLR 2020
                                # BZYN : ICLR 2019
                                is_bold = any(i in character.fontname
                                              for i in bold_fonts)
                                if verbose:
                                    print(character.fontname)
                                break
                        else:
                            if isinstance(character, LTChar):
                                font_size = character.size
                                if verbose:
                                    print(character.get_text())
                                break  #the first character only, assuming all others in text_line have the same size
                    if bold:
                        bolds.append(is_bold)
                    lines.append(text_line.get_text())
                if not bold:
                    fonts.append(font_size)
                elements.append(element.get_text())
        break  #reading first page only
    return [lines if bold else elements, bolds if bold else fonts]


def extractTitlePos(fonts, rank=1):
    """helper method to extract the positions having the largest font size"""
    font_pos = []
    maxFont = sorted(fonts)[-rank]

    for pos, size in enumerate(fonts):
        if size == maxFont:
            font_pos.append(pos)
    return font_pos


def extractAuthorPos(bolds):
    """helper method to extract the positions having the largest font size"""
    bold_pos = []

    for pos, is_bold in enumerate(bolds):
        if is_bold:
            bold_pos.append(pos)
    return bold_pos


def extractTitle(elements, positions):
    """helper method to extract those elements having the largest font size, then return as a joint string"""
    title = []
    for i in positions:
        title.append(elements[i])
    return "".join(title)


def extractAuthor(text_line, positions):
    author = []
    for i in positions:
        author.append(text_line[i])
    return ", ".join(author)


def cleanTitle(title):
    """helper method to clean the title by removing \n and illegal filename symbols"""
    title = title.strip()  #remove whitespaces
    title = title.replace("\n", " ")  #remove any inline \n
    title = title.replace(":", " -")  #replace invalid filename : symbol
    title = title.replace("?", " ")  #replace invalid filename ? symbol
    return title
