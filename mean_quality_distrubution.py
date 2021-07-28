

import bioinfo
import numpy as np

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


def populate_array(file,array):   
	f=open(file,'r')
    
	current_record = 0 
	n = 0
    
	while True:
        
		line=(f.readline()).strip()

		if n%4==3: #if the file line is 3,7,11... i.e. the quality score line
		
			for position in range(args.read_length): #for each charcter in the quality score line
		
				array[position,current_record] = convert(line[position])
            
			current_record += 1
                
		if line=='': #if there are no more lines to read, break
			break
        
		n += 1

	f.close()
	
	return(array)


def make_data(array):
	mean = np.zeros(101)
	stdev = np.zeros(101)

	for position in range(len(array)):
		mean[position] = np.mean((array[position]))
		stdev[position] = np.std(array[position], ddof=1)
	
	return(mean,stdev)


def distribution(mean, stdev, print_to_terminal = False):
	import matplotlib.pyplot as plt

	y_data=mean
	x_data=range(len(mean))
	plt.xlabel('base position', size=20)
	plt.ylabel('mean value of base number', size=20)
	plt.title('Base Mean Quality Scores', size = 22)
	plt.bar(x_data,y_data, color='mediumspringgreen')
	plt.errorbar(x_data, y_data, yerr=stdev, fmt='.', elinewidth=1,color='teal', linewidth=2)
	plt.savefig('{}/{}.png'.format(args.directory, args.plot_title))
	if print_to_terminal == True:
		plt.show()


################## This section calls the appropriate functions to build a mean quality score distribution graph #################

file=args.input_file

array=np.zeros((args.read_length, args.number_records))

array=populate_array(file,array)

mean = make_data(array)[0]
stdev = make_data(array)[1]

distribution(mean,stdev)