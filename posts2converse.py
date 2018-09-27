

#------------------------ convert posts into converdations --------------------

def post2conversation(in_file, out_file):
	import json
	import os

	# open the post file

	f = open(in_file, 'r')

	# read comments line by line
	# each line is a comment
	# in json format

	# cashing data in a post
	memo = {}

	for line in f:

		# 10 hashtags means the starting of a new post
		# TODO: check the data to confirm

		if line == "##########":
			
			write2converse(memo, out_file)

			# reset memo for the next post
			memo = {}
		

		# add each line into the memo

		data = json.load(line)

		post_id = data['link_id'].split('_')[1]
		author = data['author']
		parent_id = data['parent_id'].split('_')[1]

		# t1 are comments, t3 are posts
		parent_type = data['parent_id'].split('_')[0]

		# time stamp
		time_create = data['created_utc']

		# text
		text = data['body']

		# link
		link = data['permalink']

		# save info into memo
		row = [post_id, parent_id, author, time_create, link, text, parent_type]
		memo[idx] = row

	f.close()

#--------------- break and write post into conversations (sub) ----------------

def write2converse(memo, out_file):

	from functools import cmp_to_key

	# store idx for each conversation marked by a pair of users

	converse = {}

	# mark the comments that replied to the post
	# if true, the comment is already in a conversation stored in converse

	reply2post = {}

	# write conversations to output file

	for idx in memo.keys():

		# check to see if parent type is t1 or t3
		parent_type = memo[idx][-1]

		# if the parent is t3/post
		# mark for later process

		if parent_type == 't3':

			# make sure it is not saved in converse already

			if idx not in reply2post:
				
				reply2post[idx] == False

		# if the parent t1/comment

		else:

			author = memo[idx][2]

			p_author = memo[memo[idx][1]][2]

			timestamp = memo[idx][3]

			p_id = memo[idx][1]

			p_timestamp = memo[memo[idx][1]][3]

			p_parent_type = memo[p_id][-1]

		if (author, p_author) not in converse and (p_author, author) not in converse:

			if p_parent_type == 't3':

				converse[(author, p_author)] = [(p_id, p_timestamp), (idx, timestamp)]

				reply2post['p_id'] = True

			else:
				converse[(author, p_author)] = [(idx, timestamp)]

		elif (author, p_author) in converse:

			if p_parent_type == 't3':

				converse[(author, p_author)].append((p_id, p_timestamp))

				reply2post['p_id'] = True

			converse[(author, p_author)].append((idx, timestamp))

		elif (p_author, author) in converse:

			if p_parent_type == 't3':

				converse[(author, p_author)].append((p_id, p_timestamp))

				reply2post['p_id'] = True

			converse[(p_author, author)].append((idx, timestamp))


	# sort the converses by timestamp

	for userpair in converse.keys():

		converse[userpair] = sorted(converse[userpair], key = cmp_to_key(cmp))

	# write conversations to file

	fout = open(out_file, 'a')

	for userpair in converse.keys():

		# write the separator of a conversation

		fout.write("==========\n")

		for t in converse[userpair]:

			idx = t[0]

			time = memo[idx][3] + '\n'

			author = memo[idx][2] + '\n'

			link = memo[idx][4] + '\n'

			body = memo[idx][5] + '\n'

			fout.write(time)
			fout.write(author)
			fout.write(link)
			fout.write(body)

	# write single comment replied to the post
	for idx in reply2post.keys():

		# write the separator
		fout.write("==========\n")

		time = memo[idx][3] + '\n'

		author = memo[idx][2] + '\n'

		link = memo[idx][4] + '\n'

		body = memo[idx][5] + '\n'

		fout.write(time)
		fout.write(author)
		fout.write(link)
		fout.write(body)


	fout.close()

#----------------------- customized comparison function -----------------------
def cmp(a, b):
	import datetime

	t1 = datetime.datetime.fromtimestamp(a[1])
	t2 = datetime.datetime.fromtimestamp(b[1])

	if t1 < t2:

		return -1

	elif t1 == t2:

		return 0

	else:

		return 1
