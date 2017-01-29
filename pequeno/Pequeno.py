import sys
import os
import logging
import time
from pequeno.SampleData import SampleData
#from pequeno.SpreadsheetParser import SpreadsheetParser
from pequeno.Kmc import Kmc
#from pequeno.KmcComplex import KmcComplex
from pequeno.FastqReadNames import FastqReadNames
from pequeno.KmcFilter import KmcFilter
from pequeno.SpadesAssembly import SpadesAssembly
#from pequeno.Methods import Methods

class Pequeno:
	def __init__(self,options):
		self.start_time = int(time.time())
		self.logger = logging.getLogger(__name__)
		self.output_directory        = options.output_directory 
		self.forward_fastq           = options.forward_fastq
		self.reverse_fastq           = options.reverse_fastq
		self.database                = options.database
		self.verbose                 = options.verbose
		self.threads                 = options.threads
		self.kmer                    = options.kmer
		self.min_kmers_threshold     = options.min_kmers_threshold
		self.max_kmers_threshold     = options.max_kmers_threshold
		self.spades_exec             = options.spades_exec
		self.min_contig_len          = options.min_contig_len

	def run(self):
		os.makedirs(self.output_directory)
		sample = SampleData(self.forward_fastq,self.reverse_fastq)
		
		self.logger.info("Generating a kmer database for sample")
		kmc_sample = Kmc(self.output_directory, sample, self.threads, self.kmer, self.min_kmers_threshold, self.max_kmers_threshold)
		kmc_sample.run()
		
		self.logger.info("Finding novel kmers")
		kmc_subtract = KmcSubtract(self.output_directory, self.threads, self.min_kmers_threshold, kmc_sample, self.database)
		kmc_subtract.run()

		kmc_filter = KmcFilter(sample, self.output_directory, self.threads,kmc_subtract.result_database())
		kmc_filter.filter_fastq_file_against_kmers()
		
		spades_assembly = SpadesAssembly( sample, self.output_directory, self.threads, self.kmer, self.spades_exec, self.min_contig_len)
		spades_assembly.run()
		print(spades_assembly.filtered_spades_assembly_file() + '\n')
			
		#method_file = Methods(os.path.join(self.output_directory, 'methods_summary.txt'), trait_samples, nontrait_samples, self.min_kmers_threshold, self.min_contig_len, self.start_time, self.spades_exec)
		#method_file.create_file()
		
		#if not self.verbose:
		#	# Delete all sample temp directories
		#	self.logger.info("Deleting intermediate files, use --verbose if you wish to keep them")
		#	for kmc_sample in kmc_samples:
		#		kmc_sample.cleanup()
		#		
		#	kmc_complex.cleanup()
		#	
		#	for kmc_filter in kmc_filters:
		#		kmc_filter.cleanup()
		#	
		#	for spades_assembly in spades_assemblies:
		#		spades_assembly.cleanup()
		