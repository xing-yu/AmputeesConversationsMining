"""pushshift API

The functions utilize the pushshift API (https://github.com/pushshift/api) to get Reddit data

"""

# a python wrap function of the pushshift api
def search(endpoint = None, **kwargs):

	if not endpoint:
		print("An endpoint must be provided")
		return

	import requests

	url = "https://api.pushshift.io/reddit/" + endpoint + "/search?"

	para = []

	for key, value in kwargs.items():

		para.append(str(key) + "=" + str(value))

	if len(para) > 0:

		url += "&".join(para)

	r = requests.get(url)

	if r.status_code != 200:
		return None

	else:
		return r.json()["data"]

# search comments by submission id
def searchComments(fields_values_pairs, sort_type = "created_utc", sort = "asc", size = "500"):

	import requests

	url = "https://api.pushshift.io/reddit/search/comment/?"

	for each in fields_values_pairs:
		url += each[0]
		url += '='
		url += each[1]
		url += '&'

	# append size and sort
	url += 'size' + '=' + size + '&'
	url += 'sort' + '=' + sort + '&'
	url += 'sort_type' + '=' + sort_type

	r = requests.get(url)

	if r.status_code != 200:
		return None

	else:
		return r.json()["data"]

# dump data
def saveToFile(data, fout):

	import json

	json.dump(data, fout)

	fout.write('\n')


#<=================== test ==================>
'''
import json

search = [("link_id", "497b6x")]

ret = searchComments(search)

fout = open("pushshiftRet.txt", 'a')

json.dump(ret, fout)

fout.close()
'''