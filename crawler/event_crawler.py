'''Events crawler

    Collect comments in an post
'''

link_id_file = '/home/yu64/Desktop/bplabel1/data/event_text_all.txt'
outputfile = '/home/yu64/Desktop/event_all.json'

import pushshift

def main(link_id_file, outputfile):

    link_ids = (line.strip().split(',')[0].split('_')[1] for line in open(link_id_file, 'r'))

    crawled_link_ids = {}

    for line in open(outputfile, 'r'):
        link_id = line.strip().split(',')[0].split('_')[1]
        crawled_link_ids[link_id] = 1

    fout = open(outputfile, 'a')

    print("start crawling...")

    count = 0

    for link_id in link_ids:
        if link_id not in crawled_link_ids:
            try:
            	search = [("link_id", link_id)]

            	ret = pushshift.searchComments(search)

            	if ret == None:
            		continue

            	pushshift.saveToFile(ret, fout)
            	count += 1
            	print("Crawled count:" + str(count))

            except:
                continue


    fout.close()

main(link_id_file, outputfile)
