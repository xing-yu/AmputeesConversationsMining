# this program ranks the conversations by a chosen category in LIWC

# load dictionary
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

                
