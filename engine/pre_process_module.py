import re
import string
import json
import os
import unicodedata


from utils.constants import SRC_DIR

try:
    with open(os.path.join(SRC_DIR, 'contractions.json'), 'r') as jf:
        contractions_dict = json.load(jf)
except FileExistsError:
    contractions_dict = {}

contractions_re = re.compile('(%s)' % '|'.join(contractions_dict.keys()))


def remove_non_ascii(s):
    """Remove non-ASCII characters from list of tokenized words"""
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('utf-8', 'ignore')


def convert_to_lower(s):
    return s.lower()


def remove_html_tag(s):
    # """remove html tags from text"""
    # soup = BeautifulSoup(s, "html.parser")
    # stripped_text = soup.get_text(separator=" ")
    # return stripped_text
    return re.sub('<[^<]+?>', '', s)


def remove_digits(s):
    return re.sub(r'\d +', '', s)


def remove_punctuation(s):
    """
        The following code removes this set of symbols
            [!”#$%&’()*+,-./:;<=>?@[\]^_`{|}~]:
    """
    translator = str.maketrans(dict.fromkeys(string.punctuation))  # OR {key: None for key in string.punctuation}
    return s.translate(translator)
    # return s.translate(maketrans("", ""), string.punctuation)


def remove_white_space(s):
    return s.strip()


def remove_html_url(s):
    s = re.sub(r'http\S+', '', s)  # s = re.sub(r'http://.*?($| )', '', s)
    return s


def expand_contractions(s):
    def replace(match):
        return contractions_dict[match.group(0)]
    return contractions_re.sub(replace, s)


def is_ssh_credential(s):
    """public_key=BgIAAACkAABSU0ExAAgAAAEAAQCrqDYGBNhE25Tqxua2i..."""
    return len(s) > 128


def remove_escape(s):
    return s.replace("\n", ' ').replace("\\n", ' ')


def clean_sentence(sentence):
    """
        - remove non ascii words
        - convert to lower
        - remove html url
        - remove html tag
    :param sentence:
    :return:
    """
    # non ascii codes
    s = remove_non_ascii(sentence)

    # digits and uppers
    s = convert_to_lower(s)

    # html
    s = remove_html_tag(s)
    s = remove_html_url(s)

    return s


def clean_words(words):
    """
        - expand contractions
        - remove punctuations
        -
        - remove white space
    :param words:
    :return:
    """
    cle_words = []
    for w in words:
        # contractions
        w = expand_contractions(w)

        # punctuation
        w = remove_punctuation(w)

        # white spaces
        w = remove_white_space(w)

        if w != '' and not is_ssh_credential(w):
            cle_words.append(w)

    return cle_words

