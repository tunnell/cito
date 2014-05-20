"""
cito.core.EventBuilding
~~~~~~~~~~~~~~~~~~~~~~~

Event building converts time blocks of data (from different digitizer boards) into DAQ events.

Event building (see jargon) occurs by taking all the data from all the boards recorded during a time window and,
using some trigger logic, identifying independent events within this time window.  An EventBuilder class is defined
that performs the following sequential operations:

* Build sum waveform
* Using trigger algorithm, identify peaks in time.
* If there is no pileup (read further for pileup details), an event corresponds to a predefined time range before
  and after each peak.

More technically, a boolean array is created for each time sample, where True corresponds to a sample being saved
and false corresponds to an event being discarded.  These values default to false.  Two variables are defined by the
user: t_pre and t_post.  For each peak that the triggering algorithm identifies (e.g., charge above 100 pe), the
range [peak_i - t_pre, peak_i + t_post] is set to true  (see get_index_mask_for_trigger).  Subsequently, continuous
blocks of 'true' are called an event.

In other words, if two particles interact in the detector within a typical 'event window', then these two
interactions are saved as one event.  Identifying how to break up the event is thus left for postprocessing.  For
example, for peak_k > peak_i, if peak_i + t_post > peak_k - t_pre, these are one event.


"""

import math
import logging
import time

import pymongo
from tqdm import tqdm
from wax.Database import InputDBInterface, OutputDBInterface, ControlDBInterface
from wax import Configuration
from wax.EventBuilder.Tasks import process_time_range

__author__ = 'tunnell'



def sizeof_fmt(num):
    for x in ['B', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')


def sampletime_fmt(num):
    num *= 10
    for x in ['ns', 'us', 'ms']:
        if num < 1000.0:
            return "%3.1f %s" % (num, x)
        num /= 1000.0
    return "%3.1f %s" % (num, 's')


class Base:
    def __init__(self,
                 chunksize=Configuration.CHUNKSIZE,
                 padding=Configuration.PADDING,
                 threshold=Configuration.THRESHOLD):
        """None dataset means it will find it

        """

        self.log = logging.getLogger(__name__)
        self._input = None
        self._output = None
        self._controldb = None

        if chunksize <= 0:
            raise ValueError("chunksize <= 0: cannot analyze negative number of samples.")
        self.log.info("Using chunk size of %s" % sampletime_fmt(chunksize))
        self.chunksize = chunksize

        if padding < 0:
            raise ValueError("padding < 0: cannot analyze negative number of samples.")
        if padding >= chunksize:
            self.warning("Padding is bigger than chunk?")
        self.log.info("Using padding of %s" % sampletime_fmt(padding))
        self.padding = padding
        self.threshold = threshold

        self.waittime = 1 # Wait 1 second, if no data around

    def _initialize(self, dataset=None, hostname='127.0.0.1'):
        """If dataset == None, finds a collection on its own"""
        self._controldb = ControlDBInterface.MongoDBControl(collection_name='triggerrate',
                                                            hostname=hostname)

        self.delete_collection_when_done = True
        if dataset is not None:
            # We've chosen a dataset to process, probably for testing so don't
            # delete
            self.delete_collection_when_done = False
        self.input = InputDBInterface.MongoDBInput(collection_name=dataset,
                                                   hostname=hostname)
        if self.input.initialized:
            self.output = OutputDBInterface.MongoDBOutput(collection_name=self.input.get_collection_name(),
                                                          hostname=hostname)
        else:
            self.log.debug("Cannot setup output DB.")
            self.output = None

    def process_single_dataset(self, hostname, dataset):
        # def EventBuilderDatasetLooper(hostname, dataset, chunks, chunksize, padding):
        """This function makes lots of processing classes"""

        try:
            self._initialize(dataset=dataset,
                             hostname=hostname)
        except Exception as e:
            self.log.exception(e)
            self.log.fatal("Exception resulted in fatal error; quiting.")
            raise

        if not self.input.initialized:
            self.log.fatal("No dataset available to process; exiting.")
            return
        else:
            self._process_chosen_dataset()

    def loop_and_find_new_datasets(self, hostname):
        # def EventBuilderDatasetLooper(hostname, dataset, chunks, chunksize, padding):
        """This function makes lots of processing classes"""
        while True:
            try:
                self._initialize(hostname=hostname)  # Dataset=None means it finds one
            except pymongo.errors.ConnectionFailure as e:
                self.log.error(e)
                self.log.error("Cannot connect to mongodb.  Will retry in 10 seconds.")
                time.sleep(10)
                continue

            if not self.input.initialized:
                self.log.warning("No dataset available to process; waiting one second.")
                self._controldb.send_stats()
                time.sleep(1)
            else:
                self._process_chosen_dataset()

    def _process_chosen_dataset(self):
        """This will process the dataset in chunks, but will wait until end of run
        chunks -1 means go forever"""

        # int rounds down
        min_time_index = int(self.input.get_min_time()/self.chunksize)

        current_time_index = min_time_index
        search_for_more_data = True

        while (search_for_more_data):
            if self.input.has_run_ended():
                # Round up
                self.log.info("Data taking has ended; processing remaining data.")
                max_time_index = math.ceil(self.input.get_max_time() / self.chunksize)
                search_for_more_data = False
            else:
                # Round down
                max_time_index = int(self.input.get_max_time() / self.chunksize)

            # Rates should be posted by tasks to mongo?
            if max_time_index > current_time_index:
                for i in tqdm(range(current_time_index, max_time_index)):
                    t0 = (i * self.chunksize)
                    t1 = (i + 1) * self.chunksize

                    process_time_range(t0, t1 + self.padding,
                                       collection_name=self.input.get_collection_name(),
                                       hostname=self.input.get_hostname())

                processed_time = (max_time_index - current_time_index)
                processed_time *= self.chunksize / 1e8
                self.log.warning("Processed %d seconds; searching for more data." % processed_time)

                current_time_index = max_time_index
            else:
                self.log.debug('Waiting %f seconds' % self.waittime)
                time.sleep(self.waittime)


        if self.delete_collection_when_done:
            self.drop_collection()


    def get_processing_function(self):
        raise NotImplementedError()

    def _print_stats(self, amount_data_processed, dt):

        self.log.debug("%d bytes processed in %d seconds" % (amount_data_processed,
                                                             dt))
        if dt < 1.0:
            self.log.debug("Rate: N/A")
        else:
            data_rate = amount_data_processed / dt
            rate_string = sizeof_fmt(data_rate) + 'ps'
            self.log.debug("Rate: %s" % (rate_string))

    def drop_collection(self):
        self.input.get_db().drop_collection(self.input.get_collection_name())


class SingleThreaded(Base):
    def get_processing_function(self):
        return process_time_range

class Celery(Base):
    def get_processing_function(self):
        return process_time_range.delay