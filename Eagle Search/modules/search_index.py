import pickle
import os

moduledir = os.path.dirname(os.path.abspath('__file__'))
pkl_file = open(os.path.join(moduledir, 'applications\unt_searchengine\modules\unt_index.pkl'), 'rb')
inverted_index = pickle.load(pkl_file)
pkl_file.close()
