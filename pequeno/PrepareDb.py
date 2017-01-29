import sys
import os
import logging
import urllib
import tempfile

from pequeno.Kmc import Kmc


class PrepareDb:
	def __init__(self,options):
		self.start_time = int(time.time())
		self.logger = logging.getLogger(__name__)
		self.output_directory        = options.output_directory 
		self.url                     = options.url
		self.verbose                 = options.verbose
		self.threads                 = options.threads
		self.kmer                    = options.kmer
		self.min_kmers_threshold     = options.min_kmers_threshold
		self.temp_working_dir        = tempfile.mkdtemp(dir=os.path.abspath(output_directory))

	def downloaded_file(self):
		return os.path.join(self.output_directory,'nt.gz')

	def download_file(self):
		urllib.urlretrieve(self.url, self.downloaded_file())
	
	def nt_database(self):
		return os.path.join(self.output_directory,'ntdb')

	def kmc_command(self):
		return ' '.join(['kmc', '-k'+self.kmer, '-ci'+self.min_kmers_threshold, '-t'+self.threads, '-fm', self.downloaded_file(), self.nt_database(), self.temp_working_dir])
	
	def run(self):
		os.makedirs(self.output_directory)
		self.logger.info("Downloading database" )
		self.download_file()
		
		self.logger.info("Counting kmers" )
		subprocess.call(self.kmc_command(),shell=True)
		
		# compact

	def cleanup(self):
		shutil.rmtree(self.temp_working_dir)