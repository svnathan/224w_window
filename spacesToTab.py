filename = './Edge_List_Users_Amazon_Instant_Video.txt'

string = ''
with open(filename, 'r') as f:
	for line in f.readlines():
		data = '\t'.join(line.split())+'\n'
		string += data

with open(filename, 'w') as f:
	f.write(string)

