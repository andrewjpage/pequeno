import os
import argparse

class InputTypesPequeno:
	
	def is_database_valid(filename):
		if not os.path.exists(filename):
			raise argparse.ArgumentTypeError("Database not found")
		return filename
	
	def is_output_directory_valid(filename):
		if os.path.exists(filename):
			raise argparse.ArgumentTypeError("The output directory already exists")
		return filename
			
	def is_kmer_valid(value_str):
		if value_str.isdigit():
			kmer = int(value_str)
			if kmer%2 == 1 and kmer >= 21 and kmer <= 127:
				return kmer
		raise argparse.ArgumentTypeError("Invalid Kmer value, it must be an odd integer between 21 and 127")
		
	def is_min_kmers_threshold_valid(value_str):
		if value_str.isdigit():
			min_kmers_threshold = int(value_str)
			if  min_kmers_threshold >= 0 and min_kmers_threshold <= 255:
				return min_kmers_threshold
		raise argparse.ArgumentTypeError("Invalid minimum kmers threshold, it must be between 0 and 255, but ideally 1.")
		
	def is_max_kmers_threshold_valid(value_str):
		if value_str.isdigit():
			max_kmers_threshold = int(value_str)
			if  max_kmers_threshold >= 10 and max_kmers_threshold <= 255:
				return max_kmers_threshold
		raise argparse.ArgumentTypeError("Invalid maximum kmers threshold, it must be between 10 and 255, and greater than the minimum kmer value, but ideally greater than the coverage.")
		
		
	def is_threads_valid(value_str):
		if value_str.isdigit():
			threads = int(value_str)
			if  threads > 0 and threads <= 512:
				return threads
		raise argparse.ArgumentTypeError("Invalid number of threads, it must at least 1 and less than the No. of CPUs")
		