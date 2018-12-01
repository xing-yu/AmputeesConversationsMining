# collect usernames through subreddit posts/comments
# call push shift api

import json
import datetime
import sys

sys.path.append('../api')
import pushshift


subreddits = ["amputee"]

#------------------ main ------------------
def main(subreddits):

	for subreddit in subreddits:
		collect_usernames(subreddit)

#----------- collect usernames from a subreddit -----------
def collect_usernames(subreddit):

	# memo
	memo = {}

	# endpoints
	endpoints = ("comment", "submission")

	# exhaustively search both endpoints
	for endpoint in endpoints:

		# timestamp lower bound of api data
		before = []

		print("Starting crawling data from %s : %s"%(subreddit, endpoint))

		# search endpoint
		data = pushshift.search(endpoint, subreddit = subreddit)

		# process endpoint
		process(data, memo, before)

		# re-call api with the lower time bound
		while True:

			data = pushshift.search(endpoint, subreddit = subreddit, before = before[0])

			if data == []:
				break

			else:
				process(data, memo, before)

	output_file_name = subreddit + '_usernames.csv'
	fout = open(output_file_name, 'w')

	for username in memo.keys():
		fout.write(username)
		fout.write(',')
		fout.write(','.join(list(set(memo[username]))))
		fout.write('\n')

	fout.close()

#------------------ process data --------------------
def process(data, memo, before):

	for line in data:

		try:
			# get username
			author = line['author']

			# get flair text if any
			flair_text = line['author_flair_text']

			# get timestamp
			timestamp = line['created_utc']
			time = datetime.datetime.fromtimestamp(timestamp)

			# record username
			if author not in memo:
				memo[author] = []			
			
			# record flair text
			# may be multiple since each subreddit can have one
			if flair_text != None:
				memo[author].append(flair_text)

			# update lower boundary
			if len(before) == 0:
				before.append(timestamp)

			elif time < datetime.datetime.fromtimestamp(before[0]):
				before[0] = timestamp

			print("Username: %s, Flair_text : %s, Time: %s" % (author, flair_text, timestamp))

		except Exception as e:
			print(e)

#------------------ call main func -----------------
main(subreddits)

