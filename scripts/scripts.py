#!/usr/bin/env python3

import re
from typing import Union

import numpy as np
# from PIL import ImageFile

import pandas as pd
import requests
from video_highlights import get_cleaned_video_data

get_cleaned_video_data('tmp/result.out').to_csv('tmp/result2.csv')