# this program ranks the conversations by a chosen category in LIWC

import sys
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from rank_conversations import sort_conversations, cmp

ps = PorterStemmer()

if len(sys.argv) < 4:

    print("usage: script input_file, dict_file, target_category")
    sys.exit(-1)

fname = sys.argv[1]
dict_file = sys.argv[2]
target_category = sys.argv[3]

#------------------------ main ---------------------------
def main(fname, dict_file, target_cate):

    fin = open(fname, 'r')

    dict_header, dict_words = load_dict(dict_file)

    print("load dictionary complete...")

    conversations = parse_conversations_liwc(fin, target_cate, dict_header, dict_words)

    conversations_sorted = sort_conversations(conversations)

    fout = open("./output/annotation_sort_" + target_cate + ".txt", 'w')

    for each in conversations_sorted:

        fout.write(each[1])
        fout.write('\n')
        fout.write('==========\n')

    fin.close()
    fout.close()

#-----------------------parse file liwc ------------------
def parse_conversations_liwc(f, target_cate, dict_header, dict_words):

    ret = []

    mark = False
    content = ''
    body = ''

    cate_num = dict_header[target_cate]

    for line in f:

        if line == "==========\n":

            cate_count = 0

            count = count_words(body, dict_header, dict_words)

            if cate_num in count:

                cate_count = count[cate_num]

            ret.append((cate_count, content))

            content = ''
            body = ''

        else:

            content += line

            if line == "COMMENT:\n":

                mark = True

            elif line == "END_OF_COMMENT\n":

                mark = False

            elif mark == True:

                body += line

    return ret

#-----------------------load dictionary-------------------
# return: {header}, {words}
def load_dict(dictionary_file):

    header = {}

    words = {}

    f = open(dictionary_file, 'r')

    # the dic file is a flat dictionary file with word and its categories

    # load the table head first

    ishead = False

    for line in f:
        data = line.strip().split("\t")

        # toggle header
        if data[0] == '%':
            if ishead == False:
                ishead = True
            else:
                ishead = False

        else:

            # save header info

            if ishead == True:
                # {str: int}
                header[data[1]] = int(data[0])

            # if not header, load the word and category
            else:

                word = data[0]

                if word[-1] == '*':
                    word = word[:-1]

                stemmed_word = ps.stem(word)
                
                # {str: [int]}
                words[stemmed_word] = list(map(int, data[1:]))

    return header, words

#-----------------count frequency function-----------------
def count_words(text, dict_header, dict_words):

    tokens = word_tokenize(text)

    tokens = [token.lower() for token in tokens]

    stems = [ps.stem(token) for token in tokens]

    count = {}

    # count appearances of each stem

    for stem in stems:

        if stem in dict_words:

            for category in dict_words[stem]:

                if category in count:

                    count[category] += 1

                else:

                    count[category] = 1

    return count

#----------------------- call main ------------------------
main(fname, dict_file, target_category)