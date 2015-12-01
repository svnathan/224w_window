import sys
import gzip
import time
import json
import os

directory = '/Users/home/Desktop/Google Drive/Courses/224W/Project/Data/'
item = 'Cell_Phones_and_Accessories'

fList = []

if not os.path.exists(directory+item+'/'):
    os.makedirs(directory+item+'/')

for year in range(1999, 2015):
	fList.append(open(directory + item + '/reviews_' + item + '_' + str(year) +'.json', 'w'))

def parseIterator(path):
	g = gzip.open(path, 'r')
	for l in g:
		yield eval(l)

def parseReviews(path, directory):
	for review in parseIterator(path):
		time = review['reviewTime'].split()
		year = int(time[2])
		f = fList[year-1999]
		f.write("%s\n" % review)

def main(argv):
	parseReviews(directory + 'reviews_' + item + '.json.gz', directory)

if __name__ == '__main__':
	start_time = time.time()
	main(sys.argv)
	print 'Execution time is ' + str(time.time() - start_time) + ' seconds'