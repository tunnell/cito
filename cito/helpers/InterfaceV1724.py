# cito - The Xenon1T experiments software trigger
# Copyright 2013.  All rights reserved.
# https://github.com/tunnell/cito
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of the Xenon experiment, nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""Interface to Caen V1724

Flash ADC board
"""

import numpy as np

SAMPLE_TYPE = np.uint16  # Samples are actually 14 bit
MAX_ADC_VALUE = 2 ** 14   # 14 bit ADC samples
SAMPLE_TIME_STEP = 1    # 10 ns
WORD_SIZE_IN_BYTES = 4  # 4 bytes in a 32 bit word
N_CHANNELS_IN_DIGITIZER = 8  # number of channels in digitizer board


def get_word(data):
    """Generator for words
    """
    word_size_in_bytes = 4

    number_of_words = int(len(data) / word_size_in_bytes)
    for i in range(number_of_words):
        yield get_word_by_index(data, i)


def get_word_by_index(data, i, do_checks=True):
    """Get 32-bit word by index

    This function is called often so be sure to check
    """
    if do_checks:
        if len(data) == 0:
            print("Warning: data has zero length")
        if i > int(len(data) / 4):
            raise IndexError('i does not exist')

    i0 = i * WORD_SIZE_IN_BYTES
    i1 = (i + 1) * WORD_SIZE_IN_BYTES

    word = int.from_bytes(data[i0:i1], 'little')

    return word


def check_header(data, do_checks=True):
    word = get_word_by_index(data, 0)
    if do_checks:
        assert word >> 20 == 0xA00, 'Data header misformated'
    return True


def get_event_size(data, do_checks=True):
    check_header(data, do_checks)
    word = get_word_by_index(data, 0)
    size = (word & 0x0FFFFFFF)  # size in words
    if do_checks:
        # len(data) is in bytes, word = 4 bytes
        assert size == (len(data) / 4), 'Size from header not equal to data size'

    return size  # number of words


def get_trigger_time_tag(data):
    check_header(data)
    word = get_word_by_index(data, 3)

    # The trigger time is a 31 bit number.  The 32nd bit is pointless since it
    # is zero for the first clock cycle then 1 for each cycle afterward.  This
    # information from from Dan Coderre (Bern).  28/Aug/2013.
    word = word & 0x7FFFFFFF

    return word


def get_waveform(data, n_samples):
    # TODO: maybe make an 8 by N_SAMPLES array?  Makes easier to use numpy
    # routines.

    # Each 'occurence' is a continous sequence of ADC samples for a given
    # channel.  Due to zero suppression, there can be multiple occurences for
    # a given channel.  Each item in this array is a dictionary that will be
    # returned.

    check_header(data)

    pnt = 1

    word_chan_mask = get_word_by_index(data, pnt, False)
    chan_mask = word_chan_mask & 0xFF
    pnt += 3

    max_time = None

    samples = np.zeros((N_CHANNELS_IN_DIGITIZER, n_samples),
                       dtype=SAMPLE_TYPE)

    for j in range(N_CHANNELS_IN_DIGITIZER):
        if not ((chan_mask >> j) & 1):
            #print("Skipping channel", j)
            continue

        words_in_channel_payload = get_word_by_index(data, pnt, False)

        pnt += 1

        counter_within_channel_payload = 2
        wavecounter_within_channel_payload = 0

        while (counter_within_channel_payload <= words_in_channel_payload):
            word_control = get_word_by_index(data, pnt, False)

            if (word_control >> 28) == 0x8:
                num_words_in_channel_payload = word_control & 0xFFFFFFF
                pnt = pnt + 1
                counter_within_channel_payload += 1

                for k in range(num_words_in_channel_payload):
                    double_sample = get_word_by_index(data, pnt, False)
                    sample_1 = double_sample & 0xFFFF
                    sample_2 = (double_sample >> 16) & 0xFFFF

                    samples[j][wavecounter_within_channel_payload] = sample_1
                    wavecounter_within_channel_payload += 1

                    samples[j][wavecounter_within_channel_payload] = sample_2
                    wavecounter_within_channel_payload += 1

                    pnt = pnt + 1
                    counter_within_channel_payload += 1

                if max_time is None or \
                        (wavecounter_within_channel_payload > max_time):
                    max_time = wavecounter_within_channel_payload
            else:
                wavecounter_within_channel_payload += 2 * \
                    words_in_channel_payload + 1
                pnt = pnt + 1
                counter_within_channel_payload += 1

    # This drops off any zeros at the rightward colums
    samples = np.compress(max_time * [True], samples, axis=1)

    return samples