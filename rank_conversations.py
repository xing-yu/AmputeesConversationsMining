# this program ranks conversations by word count

import sys

if len(sys.argv) < 2:
	print("usage: script input_file")
	sys.exit(-1)

fname = sys.argv[1]	# input file name, format is conversation

#------------------- main function --------------------------
def main(fname):

	fin = open(fname, 'r')

	conversations = parse_conversations(fin)

	conversations_sorted = sort_conversations(conversations)

	fout = open("./output/annotation_sort.txt", 'w')

	for each in conversations_sorted:

		print(each[0])
		fout.write(each[1])

	fin.close()
	fout.close()

#----------------- parse conversations ----------------------
def parse_conversations(f):

	ret = []

	mark = False # mark body
	content = ''
	body = ''

	for line in f:

		# end of a conversation

		if line == "==========\n":

			word_count = len(body)

			ret.append((word_count, content))

			content = ''
			body = ''

		else:

			content += line

			if line == "COMMENT\n":
				mark = True

			if line == "END_OF COMMENT\n":
				mark = False

			if mark == True:
				body += line

	return ret

#----------------- rank conversation ------------------------
# convers: [(int, str)]

def sort_conversations(convers):

	from functools import cmp_to_key

	ret = sorted(convers, key = cmp_to_key(cmp), reverse = True)

	return ret

#------------------ cmp function -----------------------------

def cmp(a, b):

	if a[0] < b[0]:

		return -1

	else:

		return 1

#------------------ run main ---------------------------------
main(fname)