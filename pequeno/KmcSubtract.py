import os
import logging
import tempfile
import subprocess
from pequeno.FastqReadNames import FastqReadNames
 
'''subtract 2 kmer databases to find novel kmers'''
class KmcSubtract:
	def __init__(self,kmc_sample, database, output_directory, threads,result_database):
		self.logger = logging.getLogger(__name__)
		self.kmc_sample = kmc_sample
		self.database = database
		self.threads = threads
		self.result_database = result_database
		self.temp_working_dir = tempfile.mkdtemp(dir=output_directory)

	def kmc_subtract_command(self):
		return ' '.join(['kmc_tools', '-t'+str(self.threads), 'kmers_subtract', self.kmc_sample, self.database, self.result_database ])
		
	def run(self):
		self.logger.info("Finding novel kmers")
		subprocess.call(self.kmc_subtract_command(), shell=True)
	
	def cleanup(self):
		os.remove(self.temp_working_dir)
