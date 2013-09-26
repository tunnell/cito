#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cito
----------------------------------

Tests for `cito` module.
"""

import unittest

import numpy as np

from cito.helpers import InterfaceV1724
from cito.helpers import cInterfaceV1724


class BaseInterfaceV1724():
    def _testGoodData(self):
        #  Not nice to include raw data in a file, but this ensures the test and raw data are in sync.
        #  This data is already unzipped
        data = b'\x0c\x02\x00\xa0\xff\x00\x00\x01\xbd\x1d\x00\x00$\xd6z\x8bA\x00\x00\x00\xeb\x00\x00\x00=\x00\x00\x80\x83>\x82>\x84>\x83>\x82>\x82>\x84>\x83>\x81>\x83>\x84>\x83>\x85>\x84>\x83>\x83>\x83>\x82>\x82>\x83>\x83>\x84>\x81>\x81>\x81>\x82>\x84>\x82>\x82>\x82>\x83>\x84>\x80>\x84>\x81>\x83>\x84>\x82>\x83>\x83>\x84>\x82>\x83>\x80>\x83>\x82>\x80>\x82>\x82>\x84>\x82>\x82>\x82>\x82>\x82>\x84>\x83>\x82>\x83>\x84>\x83>\x81>\x82>\x83>\x82>\x83>\x83>\x84>\x82>\x84>\x82>\x83>\x84>\x82>\x82>\x82>\x83>\x84>\x83>\x81>\x83>\x82>\x82>\x82>\x82>\x82>\x84>\x84>\x83>\x83>\x81>\x82>\x84>\x83>\x83>\x83>\x82>\x85>\x82>\x81>y>\xf7,\x10&\xcd$\x99$\x8d$\x83$~$a,\xae:\xf4=s>\x83>\x84>\x84>\x84>\x83>\x82>\x85>\x83>\x82>\x83>\xd8\x00\x00\x00A\x00\x00\x00\xeb\x00\x00\x00=\x00\x00\x80\x82>\x83>\x81>\x82>\x82>\x82>\x82>\x82>\x83>\x81>\x80>\x81>\x82>\x83>\x81>\x82>\x81>\x82>\x81>\x82>\x81>\x82>\x81>\x80>\x82>\x81>\x82>\x80>\x82>\x82>\x81>\x82>\x82>\x84>\x81>\x7f>\x81>\x80>\x81>\x80>\x82>\x82>\x82>\x81>\x83>\x82>\x81>\x81>\x81>\x83>\x81>\x81>\x81>\x81>\x82>\x82>\x82>\x81>\x83>\x80>\x83>\x80>\x82>\x81>\x7f>\x80>\x83>\x80>\x82>\x81>\x82>\x81>\x81>\x82>\x80>\x81>\x7f>\x81>\x84>\x81>\x81>\x82>\x82>\x80>\x82>\x80>\x82>\x81>\x80>\x80>\x80>\x81>\x83>\x82>\x80>\x81>\x84>\x82>\x80>\x82>e>\xbb,#&\xee$\xbe$\xb1$\xa8$\xa0$\xf4,\xcd:\xf5=o>|>\x7f>\x81>\x81>\x81>\x81>\x81>\x80>\x82>\x81>\xd8\x00\x00\x00A\x00\x00\x00\xeb\x00\x00\x00=\x00\x00\x80\x80>\x81>\x83>\x83>\x82>\x81>\x80>\x81>\x80>\x81>\x80>\x81>\x81>\x7f>\x80>\x81>\x80>\x81>\x7f>\x80>\x81>~>\x80>\x7f>\x81>\x82>\x7f>\x80>\x7f>\x81>\x80>\x7f>\x81>\x83>\x80>\x81>\x82>\x80>\x82>\x83>\x82>\x80>\x80>\x80>\x81>\x80>\x80>~>\x81>\x81>\x81>\x7f>\x80>\x7f>\x80>\x7f>\x81>\x82>\x82>\x81>~>\x7f>\x80>\x81>\x82>\x81>\x80>\x80>\x81>\x7f>\x81>\x82>\x80>\x81>\x80>\x80>\x80>~>\x80>\x81>\x80>\x81>\x82>\x81>\x81>\x81>\x80>\x81>\x7f>\x82>\x80>\x81>\x81>\x7f>\x81>\x81>\x80>\x7f>\x83>\x80>t>\xdc,\x04&\xc3$\x92$\x82${$s$\x80,\xa2:\xf0=p>\x81>\x84>\x83>\x81>\x80>\x82>\x83>\x81>\x81>\x81>\xd8\x00\x00\x00A\x00\x00\x00\xeb\x00\x00\x00=\x00\x00\x80\x83>\x83>\x84>\x83>\x83>\x81>\x84>\x83>\x82>\x85>\x84>\x84>\x83>\x82>\x84>\x84>\x82>\x82>\x83>\x83>\x85>\x83>\x84>\x84>\x84>\x84>\x84>\x83>\x83>\x84>\x83>\x84>\x84>\x84>\x83>\x82>\x82>\x85>\x83>\x84>\x82>\x83>\x85>\x85>\x84>\x83>\x84>\x84>\x83>\x84>\x84>\x84>\x83>\x83>\x84>\x84>\x86>\x83>\x84>\x85>\x82>\x84>\x81>\x83>\x85>\x83>\x85>\x83>\x83>\x84>\x84>\x85>\x84>\x84>\x83>\x82>\x83>\x83>\x83>\x84>\x83>\x83>\x83>\x83>\x85>\x84>\x83>\x83>\x84>\x83>\x84>\x83>\x85>\x85>\x86>\x84>\x83>\x83>\x85>\x85>~>\x01-\x1b&\xd4$\x9f$\x94$\x89$\x82$T,\xa6:\xf3=s>\x83>\x85>\x84>\x84>\x83>\x83>\x85>\x82>\x85>\x83>\xd8\x00\x00\x00A\x00\x00\x00\xeb\x00\x00\x00=\x00\x00\x80\x81>\x7f>~>\x80>\x80>~>\x81>\x81>~>~>\x81>\x80>\x7f>~>~>\x80>\x81>\x81>\x80>\x7f>\x80>\x81>~>\x7f>\x81>\x80>\x7f>\x80>\x80>\x80>\x81>\x80>\x81>\x80>\x80>\x80>\x81>\x7f>\x81>\x80>\x82>\x81>\x80>\x81>\x7f>\x7f>}>~>\x7f>\x80>\x80>\x80>\x7f>\x80>\x7f>~>\x7f>\x7f>\x80>\x81>\x7f>\x80>\x7f>\x81>}>~>\x7f>\x7f>\x80>\x7f>\x7f>\x7f>\x7f>}>\x7f>\x7f>~>\x80>\x82>\x7f>\x80>\x7f>\x7f>\x81>\x7f>\x7f>\x7f>\x80>\x7f>\x80>\x81>\x80>~>\x81>\x81>\x80>~>\x80>\x7f>~>w>v,8%\xe8#\xb0#\xa5#\x99#\x90#\x00+E:\xdf=l>~>\x81>\x80>\x80>\x80>\x80>\x80>\x7f>~>\x80>\xd8\x00\x00\x00A\x00\x00\x00\xeb\x00\x00\x00=\x00\x00\x80\x81>\x81>\x81>\x81>\x80>\x81>\x81>\x7f>\x81>\x80>\x80>\x80>\x81>\x81>~>~>\x7f>\x81>\x81>\x81>\x81>\x80>\x80>\x81>\x80>\x81>\x80>\x7f>\x80>\x80>\x81>\x7f>\x81>\x80>\x80>\x80>\x80>\x81>\x80>\x81>\x80>\x81>\x81>\x7f>\x80>\x81>\x80>\x80>\x81>\x80>\x81>\x81>\x81>\x81>\x82>\x80>\x81>\x82>\x81>\x83>\x80>\x81>\x80>\x81>\x80>\x81>\x80>\x80>\x7f>\x82>\x80>\x80>\x82>~>\x80>\x80>\x81>\x82>\x82>\x80>\x80>\x7f>\x7f>\x81>\x81>\x7f>\x80>\x82>\x80>\x82>\x80>\x80>\x80>\x82>\x81>\x82>\x81>\x81>\x82>\x83>z>\xcf,\xdb%\x98$_$Q$H$@$\xd9+\x87:\xec=n>\x7f>\x82>\x82>\x82>\x83>\x83>\x83>\x7f>\x80>\x82>\xd8\x00\x00\x00A\x00\x00\x00\xeb\x00\x00\x00=\x00\x00\x80\x82>\x84>\x85>\x84>\x82>\x85>\x86>\x83>\x81>\x83>\x84>\x84>\x84>\x84>\x84>\x84>\x83>\x85>\x85>\x85>\x86>\x84>\x84>\x83>\x83>\x83>\x83>\x82>\x84>\x85>\x83>\x84>\x83>\x83>\x82>\x85>\x85>\x83>\x84>\x83>\x83>\x82>\x82>\x84>\x85>\x83>\x83>\x82>\x83>\x84>\x82>\x83>\x82>\x85>\x82>\x84>\x81>\x84>\x85>\x82>\x85>\x83>\x84>\x84>\x85>\x86>\x82>\x82>\x82>\x82>\x85>\x86>\x84>\x83>\x83>\x86>\x85>\x83>\x83>\x83>\x83>\x82>\x83>\x84>\x83>\x84>\x86>\x84>\x85>\x84>\x82>\x83>\x83>\x83>\x84>\x83>\x85>\x84>\x85>\x84>v>D,5%\xef#\xbb#\xac#\xa0#\x99#D+l:\xeb=s>\x84>\x84>\x85>\x85>\x89>\x84>\x86>\x84>\x85>\x85>\xd8\x00\x00\x00A\x00\x00\x00\xeb\x00\x00\x00=\x00\x00\x80\x89>\x89>\x8a>\x89>\x89>\x87>\x8c>\x89>\x8a>\x8b>\x8a>\x88>\x8a>\x89>\x88>\x8b>\x89>\x89>\x8a>\x89>\x8b>\x89>\x8b>\x8a>\x8a>\x8a>\x89>\x8a>\x88>\x88>\x8a>\x8a>\x88>\x89>\x89>\x8b>\x8b>\x8a>\x88>\x88>\x8a>\x8b>\x8a>\x8a>\x8a>\x8b>\x88>\x89>\x8b>\x89>\x88>\x89>\x8a>\x89>\x8a>\x8a>\x8b>\x8a>\x89>\x8a>\x88>\x8a>\x8a>\x88>\x88>\x8b>\x89>\x8a>\x88>\x89>\x88>\x8a>\x8c>\x8c>\x88>\x8a>\x8b>\x8c>\x8a>\x8a>\x88>\x8a>\x89>\x88>\x8a>\x8b>\x89>\x8b>\x89>\x89>\x8a>\x89>\x8a>\x8a>\x89>\x8a>\x8b>\x8a>\x88>\x89>\x87>\xf6,\xe4%\x9e$i$Y$P$I$\xa8+\x84:\xf2=x>\x87>\x89>\x8a>\x87>\x8a>\x8a>\x8b>\x89>\x8a>\x89>\xd8\x00\x00\x00'
        return data

    def _testBadData(self):
        """Return list of bad data
        """
        return [b"0",
                b'\x81>\x80>\x82>\x83>\x81>\x81>\x81>\xd8\x00\x00\x00A\x00\x00\x00\xeb\x00\x00\x00=\x00\x00\x80\x83>\x83>\x84>\x83>\x83>\x81>\x84>\x83>\x82>\x85>\x84>\x84>\x83>\x82>\x84>\x84>\x82>\x82>\x83>\x83>\x85>\x83>\x84>\x84>\x84>\x84>\x84>\x83>\x83>\x84>\x83>\x84>\x84>\x84>\x83>\x82>\x82>\x85>\x83>\x84>\x82>\x83>\x85>\x85>\x84>\x83>\x84>\x84>\x83>\x84>\x84>\x84>\x83>\x83>\x84>\x84>\x86>\x83>\x84>\x85>\x82>\x84>\x81>\x83>\x85>\x83>\x85>\x83>\x83>\x84>\x84>\x85>\x84>\x84>\x83>\x82>\x83>\x83>\x83>\x84>\x83>\x83>\x83>\x83>\x85>\x84>\x83>\x83>\x84>\x83>\x84>\x83>\x85>\x85>\x86>\x84>\x83>\x83>\x85>\x85>~>\x01-\x1b&\xd4$\x9f$\x94$\x89$\x82$T,\xa6:\xf3=s>\x83>\x85>\x84>\x84>\x83>\x83>\x85>\x82>\x85>\x83>\xd8\x00\x00\x00A\x00\x00\x00\xeb\x00\x00\x00=\x00\x00\x80\x81>\x7f>~>\x80>\x80>~>\x81>\x81>~>~>\x81>']

    def _get_n_digitizers(self):
        return 8

    def setUp(self):
        raise NotImplementedError()


    def test_trigger_time_tag(self):
        data = self._testGoodData()
        ttt = self.interfaceClass.get_trigger_time_tag(data)
        self.assertEqual(ttt, 192599588)

    def test_check_header(self):
        data = self._testGoodData()
        self.interfaceClass.check_header(data)

    def test_get_size_value(self):
        data = self._testGoodData()
        data_size = self.interfaceClass.get_block_size(data)
        self.assertEqual(data_size, 524)

        #  Crop data so header size isn't data size
        self.assertRaises(AssertionError,
                          self.interfaceClass.get_block_size,
                          data[0:int(len(data) / 2)])

    def test_get_word_by_index_values(self):
        data = self._testGoodData()
        self.assertEqual(self.interfaceClass.get_word_by_index(data, 0), 2684355084)
        self.assertEqual(self.interfaceClass.get_word_by_index(data, 1), 16777471)


    def test_get_waveform(self):
        data = self._testGoodData()
        result = self.interfaceClass.get_waveform(data, 2 * len(data))
        self.assertEqual(self._get_n_digitizers(),
                         len(result))
        self.assertIsInstance(result,
                              np.ndarray)

        for i in range(self._get_n_digitizers()):
            self.assertEqual(253,
                             len(result[i]))

        expected_result = [0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 16009, 16009, 16010, 16009,
                           16009, 16007, 16012, 16009, 16010, 16011, 16010, 16008, 16010,
                           16009, 16008, 16011, 16009, 16009, 16010, 16009, 16011, 16009,
                           16011, 16010, 16010, 16010, 16009, 16010, 16008, 16008, 16010,
                           16010, 16008, 16009, 16009, 16011, 16011, 16010, 16008, 16008,
                           16010, 16011, 16010, 16010, 16010, 16011, 16008, 16009, 16011,
                           16009, 16008, 16009, 16010, 16009, 16010, 16010, 16011, 16010,
                           16009, 16010, 16008, 16010, 16010, 16008, 16008, 16011, 16009,
                           16010, 16008, 16009, 16008, 16010, 16012, 16012, 16008, 16010,
                           16011, 16012, 16010, 16010, 16008, 16010, 16009, 16008, 16010,
                           16011, 16009, 16011, 16009, 16009, 16010, 16009, 16010, 16010,
                           16009, 16010, 16011, 16010, 16008, 16009, 16007, 11510, 9700,
                           9374, 9321, 9305, 9296, 9289, 11176, 14980, 15858, 15992,
                           16007, 16009, 16010, 16007, 16010, 16010, 16011, 16009, 16010, 16009]

        for i in range(len(result[-1])):
            self.assertAlmostEqual(result[-1][i],
                                   expected_result[i])
            self.assertIsInstance(result[0][i],
                                  np.uint16)


    def tearDown(self):
        pass


class TestInterface1724(unittest.TestCase, BaseInterfaceV1724):
    def setUp(self):
        self.interfaceClass = InterfaceV1724

    def test_get_word_by_index_asserts(self):
        data = self._testGoodData()

        self.assertRaises(IndexError,
                          self.interfaceClass.get_word_by_index,
                          data, 100000)

        self.assertRaises(IndexError,
                          self.interfaceClass.get_word_by_index,
                          b'',
                          0)

    def test_bad_data(self):
        bad_data_list = self._testBadData()
        for data in bad_data_list:
            self.assertRaises(AssertionError,
                              self.interfaceClass.get_trigger_time_tag,
                              data)
            self.assertRaises(AssertionError,
                              self.interfaceClass.get_block_size,
                              data)
            self.assertRaises(AssertionError,
                              self.interfaceClass.check_header,
                              data)


class TestcInterface1724(unittest.TestCase, BaseInterfaceV1724):
    def setUp(self):
        self.interfaceClass = cInterfaceV1724


if __name__ == '__main__':
    unittest.main()
