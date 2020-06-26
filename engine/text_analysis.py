import nltk
from autocorrect import Speller
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import utils.logger as logger
from engine.pre_process_module import clean_sentence, clean_words, remove_escape


class TextProcessor:
    def __init__(self, debug=False):
        self.debug = debug
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('popular')

        self.wordnet_lemmatizer = WordNetLemmatizer()
        self.snowball_stemmer = SnowballStemmer("english")
        self.speller = Speller(lang='en')
        self.stopwords = stopwords.words("english")

    def pre_process(self, text):
        tokenized_sentences = []

        sentences = nltk.sent_tokenize(remove_escape(text))

        for sentence in sentences:
            # [sentence clean]
            cleaned_sentence = clean_sentence(sentence=sentence)
            if self.debug:
                logger.info("sentence    : \t {}".format(sentence))

            # [word tokenize]
            token_words = nltk.word_tokenize(cleaned_sentence)
            if self.debug:
                logger.info("token_words : \t {}".format(token_words))

            # [word clean]  remove negative words e.g. ssh-key
            cleaned_words = clean_words(words=token_words)
            if self.debug:
                logger.info("cleaning   : \t {}".format(cleaned_words))

            # [spell check]
            spelling_words = [self.speller.autocorrect_word(w) for w in cleaned_words]
            if self.debug:
                logger.info("spelling    : \t {}".format(spelling_words))

            # [removing stop words]
            # removing_stopwords = [w for w in spelling_words if w not in self.stopwords]
            # if self.debug:
            #     logger.info("rm stopwords: \t {}".format(removing_stopwords))

            # [stemming]
            # norm_words = [self.snowball_stemmer.stem(w) for w in spelling_words]  # lemmatized_words
            # if self.debug:
            #     logger.info(f"stemmed     : \t {norm_words}")

            # [lemmatize]
            norm_words = [self.wordnet_lemmatizer.lemmatize(word) for word in spelling_words]
            if self.debug:
                logger.info(f"lemmatized  : \t {norm_words}")

            tokenized_sentences.append([w for w in norm_words if len(w) > 0])
            if self.debug:
                print('n')

        return tokenized_sentences

    @staticmethod
    def get_revised_field(query_data):
        db_filed_list = [
            'product_type', 'product_name', 'account_number', 'customer_name',
            'customer_id', 'balance', 'month_end', 'flag'
        ]

        revised_field = {}
        for key in query_data.keys():
            text = None
            if query_data[key] is not None:
                text, precision = process.extractOne(query_data[key], db_filed_list)

            revised_field[key] = text

        return revised_field


def get_query_data(input_str):
    text_processor = TextProcessor(debug=True)
    pre_processed_texts = text_processor.pre_process(input_str)

    pos_tagged_text = nltk.pos_tag(pre_processed_texts[0])
    # pattern = 'NP: {<DT>?<JJ>*<NN>}'
    pattern = r"""
          NPT: {<NN|VBG><IN>}
          NPC: {<NN><NN|NNP|CD>}
              {<NN>}                 
        """
    cp = nltk.RegexpParser(pattern)
    tree = cp.parse(pos_tagged_text)
    print(tree)

    target_field = None
    condition_field = None
    condition_value = None
    for subtree in tree.subtrees():
        if subtree.label() == 'NPT':
            target_field = subtree[0][0]
        if subtree.label() == 'NPC':
            condition_field = subtree[0][0]
            if len(subtree) > 1:
                condition_value = subtree[1][0]

    if condition_value is not None:
        query_data = {
            'target_field': target_field,
            'condition_field': condition_field
        }
    else:
        query_data = {
            'target_field': condition_field + '_' + target_field,
            'condition_field': condition_field + '_' + target_field
        }

    revised_data = text_processor.get_revised_field(query_data)
    revised_data['condition_value'] = condition_value
    print(revised_data)

    return revised_data


# if __name__ == '__main__':
    # import os
    # from utils.constants import SRC_DIR
    #
    # input_str = open(os.path.join(SRC_DIR, "sample_reference.txt"), 'r').read()
    # text_processor = TextProcessor(debug=True)
    # pre_processed_texts = text_processor.pre_process(input_str)
    #
    # pos_tagged_text = nltk.pos_tag(pre_processed_texts[0])
    # # pattern = 'NP: {<DT>?<JJ>*<NN>}'
    # pattern = r"""
    #   NPT: {<NN|VBG><IN>}
    #   NPC: {<NN><NNP|CD>}
    # """
    # cp = nltk.RegexpParser(pattern)
    # tree = cp.parse(pos_tagged_text)
    # print(tree)
    #
    # target_field = None
    # condition_field = None
    # condition_value = None
    # for subtree in tree.subtrees():
    #     if subtree.label() == 'NPT':
    #         target_field = subtree[0][0]
    #     if subtree.label() == 'NPC':
    #         condition_field = subtree[0][0]
    #         condition_value = subtree[1][0]
    #
    # query_filed = {
    #     'target': target_field,
    #     'condition': condition_field
    # }
    #
    # revised_filed = text_processor(query_filed)
    # print(revised_filed)

    # iob_tagged = tree2conlltags(cs)
    # pprint(iob_tagged)
    #
    # ne_tree = ne_chunk(iob_tagged)
    # print(ne_tree)
