import sys
import os
import logging
import tempfile

from pequeno.Kmc import Kmc


class PrepareDb:
	def __init__(self,options):
		self.logger = logging.getLogger(__name__)
		self.output_directory        = options.output_directory 
		self.verbose                 = options.verbose
		self.threads                 = options.threads
		self.input_file              = options.input_file
		self.kmer                    = options.kmer
		self.min_kmers_threshold     = options.min_kmers_threshold
		self.temp_working_dir        = tempfile.mkdtemp(dir=os.path.abspath(output_directory))

	def db_full(self):
		return os.path.join(self.output_directory,'db_full')
	
	def db_compact(self):
		return os.path.join(self.output_directory,'db')

	def kmc_command(self):
		return ' '.join(['kmc', '-k'+self.kmer, '-ci'+self.min_kmers_threshold, '-t'+self.threads, '-fm', self.input_file, self.db_full(), self.temp_working_dir])
	
	def kmc_compact_command(self):
		return ' '.join(['kmc_tools', 'compact', self.db_full(), self.db_compact()])
	
	def run(self):
		os.makedirs(self.output_directory)
		
		self.logger.info("Counting kmers" )
		subprocess.call(self.kmc_command(),shell=True)
		
		self.logger.info("Compacting database" )
		subprocess.call(self.kmc_compact_command(),shell=True)

	def cleanup(self):
		shutil.rmtree(self.temp_working_dir)
		# delete the full db
		