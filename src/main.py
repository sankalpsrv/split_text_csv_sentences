import re

def split_into_sentences(text):
    # Regex pattern
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|Mt)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    # website regex from https://www.geeksforgeeks.org/python-check-url-string/
    websites = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    digits = "([0-9])"
    section = "(Section \d+)([.])(?= \w)"
    item_number = "(^|\s\w{2})([.])(?=[-+ ]?\d+)"
    abbreviations = "(^|[\s\(\[]\w{1,2}s?)([.])(?=[\s\)\]]|$)"
    parenthesized = "\((.*?)\)"
    bracketed = "\[(.*?)\]"
    curly_bracketed = "\{(.*?)\}"
    enclosed = '|'.join([parenthesized, bracketed, curly_bracketed])
    # text replacement
    # replace unwanted stop period with <prd>
    # actual stop periods with <stop>
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites, lambda m: m.group().replace('.', '<prd>'), text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    if "..." in text: text = text.replace("...","<prd><prd><prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    text = re.sub(section,"\\1<prd>",text)
    text = re.sub(item_number,"\\1<prd>",text)
    text = re.sub(abbreviations, "\\1<prd>",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    text = re.sub(enclosed, lambda m: m.group().replace('.', '<prd>'), text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")

    # Tokenize sentence based upon <stop>
    sentences = text.split("<stop>")
    if sentences[-1].isspace():
        # remove last since only whitespace
        sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]

    return sentences
