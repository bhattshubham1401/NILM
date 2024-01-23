import json
import os
from datetime import date as datetime_date, timedelta, datetime
import holidays
from pathlib import Path
from typing import Any

import joblib
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import requests
import yaml
from box import ConfigBox
from box.exceptions import BoxValueError
from dotenv import load_dotenv
from ensure import ensure_annotations
from pymongo import MongoClient
from sklearn.model_selection import train_test_split , TimeSeriesSplit

# from src.mlProject.components.data_transformation import sensorDecode

from statsmodels.tsa.stattools import adfuller

from src.mlProject import logger
@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data

    Args\\\\\\\\\\\\\\
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")