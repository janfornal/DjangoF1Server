from urllib import request
from general import open_page, find
from PIL import ImageFile
import pandas as pd
import numpy as np

def get_constructor_dict():
    return_dict = {}
    with open('tmp/teams.out', 'r') as teams:
        lines = teams.readlines()
        for line in lines:
            val, key = line.split(sep='|')[0:2]
            key = key.split(sep='\n')[0]
            return_dict[key] = val
    return return_dict

def get_image_size(uri):
    # get image size (None if not known)
    with request.urlopen(uri) as file:
        p = ImageFile.Parser()
        while True:
            data = file.read(1024)
            if not data:
                break
            p.feed(data)
            if p.image:
                return p.image.size
    return np.nan

def size_of_photos():
    frame = pd.read_csv("tmp/extended_cars.csv")
    frame = frame[['Url', 'Photo']].iloc[:10]
    frame['Size'] = frame.apply(lambda row: get_image_size(row['Photo']) if row['Photo'] is not np.nan else np.nan, axis = 1)
    print(frame.head())

def verify_uniqueness(frame, column):
    series = frame[column]
    print(series[series.duplicated(keep=False)])