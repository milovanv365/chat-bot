import nltk

from engine.text_analysis import TextProcessor


text_processor = TextProcessor(debug=True)


def get_query_data(input_str):
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
