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

from aboutComp import compData
from people import compTopEmp


        # Comp_About_People_pages(driver, lst_of_comp_Links)


def CompPageLinks(driver, soup):
    # Parsing the soup to get the links of all companies and next page link.

    # Main tag having the li tags of each company on
    main_div_tag = soup.find("div", class_="search-results-container")  #id="9rvnjUBgQRaOgxrpEzk3+w=="

    # List of all the "li" tags which is having the url for each company page
    list_li_tags = main_div_tag.find_all("li", class_="reusable-search__result-container")

    # List of all companies links from the respective page. Here the respective page means the page this is currently loading/in process
    list_of_comp_links = []

    # Parsing through the tag and fetch the links of the companies
    for li in list_li_tags:
        comp_link = li.find("a")['href']
        Comp_About_People_pages(driver, comp_link)
    #     list_of_comp_links.append(li.find("a")['href'])

    # return list_of_comp_links


def Comp_About_People_pages(driver, comp_link):
    # About page of the company
    comp_about_page = comp_link + "/about/"
    # compData(driver, comp_about_page)
    # People or employees page of the company
    comp_people_page = comp_link + "/people/"
    compTopEmp(driver, comp_people_page)

    """
    # This list contains all the about pages of all companies from respective page
    comp_about_page_links = []

    # This list contains all the People page of all companies from the respective page
    comp_people_page_links = []

    # Getting all the 
    for comp in lst_of_comp_Links:

        # About page of the company
        comp_about_page = comp + "/about/"
        comp_about_page_links.append(comp_about_page)

        # People or employees page of the company
        comp_people_page = comp + "/people/"
        comp_people_page_links.append(comp_people_page)

    comp_data = compData(driver, comp_about_page_links)
    compTopEmp(driver, comp_people_page_links)
    return comp_data
    """

def LinkedInLogIn(email, password):
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service)
    driver.get("https://linkedin.com/uas/login")
    driver.maximize_window()
    time.sleep(.50)
    username = driver.find_element(By.ID, "username")
    username.send_keys(email) #enteremail
    time.sleep(1)
    pword = driver.find_element(By.ID, "password")
    time.sleep(1)
    pword.send_keys(password)       #passw
    time.sleep(1) 
    driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[3]/button").click()
    time.sleep(2)

    for page in range(0,9):
        driver.get(f"https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%22102221843%22%2C%22103644278%22%5D&companySize=%5B%22B%22%2C%22C%22%2C%22D%22%5D&keywords=azure%20data%20engineer&origin=FACETED_SEARCH&page={page+1}")
        time.sleep(2)

        # Extracting the html page of the main page 1 having the names of companies with the given filters
        main_page1_html = driver.page_source

        # Creating the soup of first page 
        soup = BeautifulSoup(main_page1_html, 'html.parser')

        # Here we will get all the links of companies in the page in process
        CompPageLinks(driver, soup)
    # comp_data.to_csv("C:\Users\Aridian Technologies\Desktop\Office\Desktop\Data Scrappers\Scraping_Companes_On_Linkedin\Data\CompData_01152024.csv")