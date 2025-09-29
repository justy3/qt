import os
import json
import time
import logging
import requests
import zipfile
import urllib.request
import numpy as np
import pandas as pd
import datetime as dt
import multiprocessing as mp

# import specific functions
from io import StringIO
from pathlib import Path
from functools import partial
from typing import Optional, Literal, Union, Tuple, List, Dict
from IPython.display import display, HTML
from IPython.core.interactiveshell import InteractiveShell

# disable warnings for InsecureEquest in HTTPS
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

##############################################
##############      LOGGER      ##############
##############################################

logging.basicConfig(
	level		=	logging.INFO,
	format		=	"[JUSTY.LOG]\t%(asctime)s - %(name)s - %(levelname)s - %(message)s",
	handlers	=	[logging.StreamHandler()]
)

# create a logger
log = logging.getLogger(__name__)

# source code path
# path to QT folder in site-packages(qt installation)
QT_SOURCE_PATH = Path(__file__).parent.parent.__str__()