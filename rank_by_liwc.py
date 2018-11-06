# this program ranks the conversations by a chosen category in LIWC

from nltk.stem import PorterStemmer

ps = PorterStemmer()

# load dictionary
# return: {header}, {words}
def load_dict(dictionary_file):

    header = {}

    words = {}

    f = open(dictionary_file, 'r')

    # the dic file is a flat dictionary file with word and its categories

    # load the table head first

    header = False

    for line in f:
        data = line.strip().split("\t")

        # toggle header
        if data[0] == '%':
            if header == False:
                header = True
            else:
                header = False

        else:

            # save header info

            if header == True:
                # {int: str}
                header[int(data[0])] = data[1]

            # if not header, load the word and category
            else:

                word = data[0]

                if word[-1] == *:
                    word = word[:-1]

                stemmed_word = ps.stem(word)
                
                # {str: [int]}
                words[stemmed_word] = list(map(int, data[1:]))

    return header, words

# count frequency function
def count_words(text, dict):
