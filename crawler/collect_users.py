# collect usernames through subreddit posts/comments
# call push shift api

import json
import datetime
import sys

sys.path.append('../api')
import pushshift


subreddits = ()

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

		# search endpoint
		data = pushshift.search(endpoint, subreddit = subreddit)

		# process endpoint
		process(data, memo, before)

		# re-call api with the lower time bound
		while True:

			data = pushshift.search(endpoint, subreddit = subreddit, before = before[0])

			if data == None:
				break

			else:
				process(data, memo, before)

	output_file_name = subreddit + '_usernames.csv'
	fout = open(output_file_name, 'w')

	for username in memo.keys():
		fout.write(username)
		fout.write(',')
		fout.write(','.join(memo[username]))
		fout.write('\n')

	fout.close()

#------------------ process data --------------------
def process(data, memo, before):

	for line in data:

		comments = json.loads(line)

		for comment in comments:

			try:
				# get username
				author = comment['author']

				# get flair text if any
				flair_text = comment['author_flair_text']

				# get timestamp
				timestamp = comment['created_utc']
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
					before[0] = timestamp

				elif time < datetime.datetime.fromtimestamp(before[0]):
					before[0] = timestamp

			except:
				continue

#------------------ call main func -----------------
main(subreddits)

