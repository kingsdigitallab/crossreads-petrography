from typing import *
from .constants import *

import os
import csv
import pandas as pd
import numpy as np
import gspread
from google.oauth2 import service_account
from loguru import logger
import sys
from functools import cache
from collections import defaultdict


try:
    from google.colab import auth, drive
    from google.auth import default
    IN_COLAB = True
except ImportError:
    IN_COLAB = False


import gspread
from google.oauth2 import service_account


logger.remove()
logger.add(
    sink=sys.stderr,
    format="<level>{message}</level><cyan> @ {time:YYYY-MM-DD HH:mm:ss,SSS}</cyan>",
    level="DEBUG",
)

from .utils import *