import json
import h5py, pickle
import os
from configparser import ConfigParser
import pandas as pd
from datetime import datetime, timedelta


class CombineData(object):

    def load_skus_properties(self, file_name):
        h5_file = file_name + '.h5'
        csv_file = file_name + '.csv'
        try:
            h5file = h5py.File(h5_file, mode='w')
            if os.path.exists(csv_file):
                print 'reload data from local file'
                with open(csv_file, "r") as ins:
                    for line in ins:
                        tokens = line.split()
                        key = tokens[1]
                        value = tokens[2:]
                        try:
                            h5file[key] = pickle.dumps(value)
                        except Exception as e:
                            print 'H5 fail!'
                            print e.__doc__
                            print e.message
                        
            h5file.close()
        except Exception as e:
            print 'something is wrong!'
            print e.__doc__
            print e.message
            # remove all file and reload at the beginning to make sure nothing wrong will happen! :()

test = CombineData()
test.load_skus_properties('data/metadata/sku_properties_sg')