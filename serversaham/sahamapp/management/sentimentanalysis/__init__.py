import numpy as np
import re
import nltk
from sklearn.datasets import load_files
nltk.download('stopwords')
import pickle
from nltk.corpus import stopwords

#ACQUISITION
movie_data = load_files('txt_sentoken')
X, y = movie_data.data, movie_data.target
print(y)