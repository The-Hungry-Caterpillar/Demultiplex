import bioinfo
import numpy as np
import gzip

convert=bioinfo.convert_phred

################################################# functions ####################################################

def get_args(): #defines all the independent variables
	import argparse
	parser = argparse.ArgumentParser(description = "still need description")
	#parser.add_argument('- command line variable', '-- python variable', description)
	parser.add_argument('-f', '--input_file', help='filename for input')
	parser.add_argument('-l', '--read_length', type=int, help='input read length')
	parser.add_argument('-nr', '--number_records', type=int, help="input number of records, use this command to count: ~$ records=$(grep -c '^@K00337' <filename>)'")
	parser.add_argument('-t', '--plot_title', help = 'input desired distribution plot title')
	parser.add_argument('-d', '--directory', help= 'input directory to save plots')
	return parser.parse_args()

args=get_args()


def find_mean(file):   
	
	for n in range(args.read_length):
		f=gzip.open(file,'rt') #this needs to be in the loop so that the readline() argument starts over
		#f=open(file,'r')
		total=0

		i=0
		
		while True:
			line=(f.readline()).strip()

			if i%4==3: #if the file line is 3,7,11... i.e. the quality score line
				total+=convert(line[n])
					
			if line=='': #if there are no more lines to read, break
				break
			
			i+=1
		f.close()

		mean = total/args.number_records
		means.append(mean)


def distribution(mean, print_to_terminal = False):
	import matplotlib.pyplot as plt

	y_data=mean
	x_data=range(len(mean))
	plt.xlabel('base position', size=20)
	plt.ylabel('mean value of base number', size=20)
	plt.title('Base Mean Quality Scores', size = 22)
	plt.bar(x_data,y_data, color='mediumspringgreen')
	plt.savefig('{}/{}.png'.format(args.directory, args.plot_title))
	if print_to_terminal == True:
		plt.show()


################## This section calls the appropriate functions to build a mean quality score distribution graph #################

file=args.input_file

means=[]
find_mean(file)

distribution(means)