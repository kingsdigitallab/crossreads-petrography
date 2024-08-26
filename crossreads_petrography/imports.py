from typing import *
from .constants import *
import warnings
warnings.filterwarnings('ignore')
import os
from functools import cached_property
import csv
import pandas as pd
import numpy as np
import gspread
from google.oauth2 import service_account
from loguru import logger
import sys
import json
from functools import cache
from collections import defaultdict
from shapely.geometry import Point, Polygon
import plotly.graph_objects as go
from scipy.interpolate import splprep, splev
from sklearn.linear_model import LinearRegression
import gspread
from google.oauth2 import service_account


logger.remove()
logger.add(
    sink=sys.stderr,
    format="<level>{message}</level><cyan> @ {time:YYYY-MM-DD HH:mm:ss,SSS}</cyan>",
    level="DEBUG",
)

from .utils import *