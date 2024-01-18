import csv
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.common.exceptions import WebDriverException

from li_login import LinkedInLogIn

import sys
sys.path.insert(0, r'C:\\Users\Aridian Technologies\\Desktop\\Office\\Desktop\\Data Scrappers\\Scraping_Companes_On_Linkedin')
from utils.settings import get_setting


if __name__ == "__main__":

    email = get_setting()["email"]
    password = get_setting()["password"]


    LinkedInLogIn(email, password)
