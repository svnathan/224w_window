import sys
import gzip
import time
import json
import os
import datetime

directory = './Data/'
item = 'Cell_Phones_and_Accessories'

fList = {}
years = [2005, 2006]

if not os.path.exists(directory+item+'/'):
    os.makedirs(directory+item+'/')

for year in years:
    fList[year] = {}
    for week in range(1,54):
	    fList[year][week] = open(directory + item + '/reviews_' + item + '_' + str(year) + '_' + str(week) +'.json', 'w')

def parseIterator(path):
	g = gzip.open(path, 'r')
	for l in g:
		yield eval(l)

def parseReviews(path, directory):
	for review in parseIterator(path):
		time = review['reviewTime'].split()
		year = int(time[2])
		month = int(time[0])
		date = int(time[1].replace(',',''))
		week = datetime.date(year, month, date).isocalendar()[1]
		try:
			f = fList[year][week]
			f.write("%s\n" % review)
		except Exception as e:
			pass

def main(argv):
	parseReviews(directory + 'reviews_' + item + '.json.gz', directory)
	
# for yearPointers in fList.itervalues():
#     for filePointer in yearPointers.itervalues():
#         filePointer.close()

if __name__ == '__main__':
	start_time = time.time()
	main(sys.argv)
	print 'Execution time is ' + str(time.time() - start_time) + ' seconds'