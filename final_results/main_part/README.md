## Introduction
This project is to find 10 restaurants based on the city users choose.  
All information about each restaurant is got from yelp api.  

## all required packages
```
import requests
from urllib.parse import quote
import json
import pandas as pd
import secret as se
from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import yelp
```
Note: the secret and yelp module are two python file I wrote. You can find them under the same folder

## How to interact with my program
### 01 get your own yelp api key from yelp
You can apply for an authentic key from yelp.  
Yelp provides specific instruction to show how to get a key.  
website: https://www.yelp.com/login?return_url=%2Fdevelopers%2Fv3%2Fmanage_app  
If you don't know how to do, please visit this website: https://www.ultimatebeaver.com/docs/find-yelp-api-key/  

### 02 download all files in this folder
Download all files in this folder to your locally.  
Open the secret.py file. Fill up your own key to replace None
Note: for anyone who is interested in this project, you don't need to download 
