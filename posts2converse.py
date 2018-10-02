
in_file = 'post_snippet.txt'
out_file = 'conversation.txt'
log_file = 'logs.txt'

annotation_file = 'annotation.txt'

candidates = {'disability':1, 'amputee':1, 'Prosthetics':1}

#------------------------ convert posts into converdations --------------------

def post2conversation(in_file, out_file, process_log):
	import json
	import os

	# open the post file

	f = open(in_file, 'r')

	# read post line by line
	# each line is a post
	# in json format

	# cashing data in a post
	memo = {}

	# counter for conversations
	conversation_counter = [0]

	# read log 
	# (post_id, counter)
	try:
		logs = open(process_log, 'r')

		id_log = {}

		for line in logs:
			log = line.strip().split(',')
			id_log[log[0]] = 1
			conversation_counter[0] = int(log[1])

		logs.close()
	except IOError:
		open(process_log, 'a').close()
		id_log = {}

	# open log file
	logs = open(process_log, 'a')

	for post in f:
		p = json.loads(post)

		# guard agaist duplicated post
		if len(p) <= 0:
			continue

		elif p[0]['link_id'].split('_')[1] in id_log:
			continue
		
		# use subreddit to screen post for annotation
		sub = p[0]['subreddit']

		for comment in p:
			
			# each comment is a dict
			# all dicts in a list
			# first read all comments into cash
			# break and sort comments into conversation
			# write conversations into a new file

			# add each comment into the memo

			data = comment

			# link id
			post_id = data['link_id'].split('_')[1]

			# comment id
			idx = data['id']

			# author name
			author = data['author']

			# parent id
			parent_id = data['parent_id'].split('_')[1]

			# t1 are comments, t3 are posts
			parent_type = data['parent_id'].split('_')[0]

			# time stamp
			time_create = data['created_utc']
			time_create = str(time_create)

			# text
			text = data['body']

			# subreddit
			subreddit = data['subreddit']

			# link
			link = "https://www.reddit.com/r/"
			link += subreddit + '/'
			link += "comments/"
			link += post_id + '/'
			link += '_/'
			link += idx + '/'

			# save info into memo
			
			row = [post_id, parent_id, author, time_create, link, text, parent_type]
			
			memo[idx] = row
			
		# break the post into conversations
		conversation_counter_copy = conversation_counter.copy()
			
		write2converse(memo, out_file, conversation_counter)

		if sub in candidates:
			write2converse(memo, annotation_file, conversation_counter_copy)

		# reset memo for the next post
		memo = {}

		# update log file

		new_entry = p[0]['link_id'].split('_')[1] + ',' + str(conversation_counter[0]) + '\n'

		logs.write(new_entry)

	f.close()
	logs.close()

#--------------- break and write post into conversations (sub) ----------------

def write2converse(memo, out_file, counter):

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
				
				reply2post[idx] = False

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

					reply2post[p_id] = True

				else:
					converse[(author, p_author)] = [(idx, timestamp)]

			elif (author, p_author) in converse:

				if p_parent_type == 't3':

					converse[(author, p_author)].append((p_id, p_timestamp))

					reply2post[p_id] = True

				converse[(author, p_author)].append((idx, timestamp))

			elif (p_author, author) in converse:

				if p_parent_type == 't3':

					converse[(author, p_author)].append((p_id, p_timestamp))

					reply2post[p_id] = True

				converse[(p_author, author)].append((idx, timestamp))


	# sort the converses by timestamp

	for userpair in converse.keys():

		converse[userpair] = sorted(converse[userpair], key = cmp_to_key(cmp))

	# write conversations to file

	fout = open(out_file, 'a')

	for userpair in converse.keys():

		# write the separator of a conversation
		# also the counter
		fout.write("==========\n")
		fout.write("COUNTER:" + str(counter[0]) + '\n\n')

		for t in converse[userpair]:

			idx = t[0]

			time = memo[idx][3] + '\n'

			author = memo[idx][2] + '\n'

			link = memo[idx][4] + '\n'

			body = memo[idx][5] + '\n'

			
			fout.write("TIMESTAMP:" + time)
			fout.write("AUTHOR:" + author)
			fout.write("LINK:" + link)
			fout.write("COMMENT:\n" + body)
			fout.write('END_OF_COMMENT\n')
			fout.write('\n')

		print("Writing conversation NO. " + str(counter[0]) + '...')

		counter[0] += 1

	# write single comment replied to the post
	for idx in reply2post.keys():

		# write the separator and the counter
		fout.write("==========\n")
		fout.write("COUNTER:" + str(counter[0]) + '\n\n')

		time = memo[idx][3] + '\n'

		author = memo[idx][2] + '\n'

		link = memo[idx][4] + '\n'

		body = memo[idx][5] + '\n'

		
		fout.write("COMMENT_TO_THE_POST\n")
		fout.write("TIMESTAMP:" + time)
		fout.write("AUTHOR:" + author)
		fout.write("LINK:" + link)
		fout.write("COMMENT:\n" + body)
		fout.write('END_OF_COMMENT\n')
		fout.write('\n')

		print("Writing conversation NO. " + str(counter[0]) + '...')
		
		counter[0] += 1

	fout.close()

#----------------------- customized comparison function -----------------------
def cmp(a, b):
	import datetime

	t1 = datetime.datetime.fromtimestamp(int(a[1]))
	t2 = datetime.datetime.fromtimestamp(int(b[1]))

	if t1 < t2:

		return -1

	elif t1 == t2:

		return 0

	else:

		return 1

#------------------------------------ call main func ------------------------------

post2conversation(in_file, out_file, log_file)
