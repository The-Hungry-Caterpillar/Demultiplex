import bioinfo
import gzip

convert=bioinfo.convert_phred

def get_args(): #defines all the independent variables
	import argparse
	parser = argparse.ArgumentParser(description = "still need description")
	#parser.add_argument('- command line variable', '-- python variable', description)
	parser.add_argument('-f', '--input_file', help='filename for input')
	parser.add_argument('-l', '--read_length', type=int, help='input read length')
	parser.add_argument('-Q', '--quality_cutoff', type=int, help='input quality cutoff')
	return parser.parse_args()

args=get_args()

i=0
bad_records=0

f=gzip.open(args.input_file,'rt')
while True:
	line=(f.readline())

	if i%4==3: #if the file line is 3,7,11... i.e. the quality score line
		for n in range(args.read_length):
			if convert(line[n]) < args.quality_cutoff:
				bad_records+=1
				break
			
	if line=='': #if there are no more lines to read, break
		break
	
	i+=1
f.close()

print('There are {} records that fall below quality score {} in the file {}'.format(bad_records, args.quality_cutoff, args.input_file))