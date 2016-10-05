import h5py
from visearch import client
from configparser import ConfigParser
import pickle


class Visenze(object):
    def __init__(self):
        self.h5_file_name = 'data/metadata/sku_properties_sg.h5'
        config = ConfigParser()
        with open('visenze.key', 'r') as configfile:
            config.read_file(configfile)
            keys = dict(config['key'])
        self.api = client.ViSearchAPI(keys['access'], keys['secret'])
        self.param = {'detection': 'all'}
        self.score = True
        self.score_min = 0.5
        self.fq = {'node_country': 'sg'}

    # product_url	image_url	lq_image_url
    def _get_metadata(self, key):
        try:
            h5file = h5py.File(name=self.h5_file_name, mode='r')
            return pickle.loads(h5file[key].value)
        except:
            return False

    def add_meta_data(self, response):
        products = dict()
        keys = [i['im_name'] for i in response['result']]
        print keys
        for key in keys:
            metadata = self._get_metadata(key)
            if metadata:
                products[key] = metadata
        return products

    def search_image(self, image_path, gender="female"):
        self.fq['gender'] = gender
        param = {'detection': 'all'}
        response = self.api.uploadsearch(
            image_path=image_path,
            #     image_url = image_url,
            score=self.score,
            score_min=self.score_min,
            fq=self.fq,
            **param)
        return self.add_meta_data(response)

    def search_url(self, image_url, gender="female"):
        self.fq['gender'] = gender
        param = {'detection': 'all'}
        response = self.api.uploadsearch(
            # image_path=image_path,
            image_url=image_url,
            score=self.score,
            score_min=self.score_min,
            fq=self.fq,
            **param)
        return self.add_meta_data(response)
