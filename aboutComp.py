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




def About_Comp_Data(comp_aboutPage_soup):
    sections = comp_aboutPage_soup.find_all("section")
    final_result = []
    csv_file_path = 'C:\\Users\\Aridian Technologies\\Desktop\\Office\\Desktop\\Data Scrappers\\Scraping_Companes_On_Linkedin\\Data\\DatacompData_25172024.csv'
    for section in sections:
        h2_tag = section.find("h2")
        if h2_tag:
            
            if h2_tag.text.strip() == "Overview":
                
                about_page_dl_tag = section.find("dl", class_="overflow-hidden")
                
                # Titles from the about page line website, industry, comp size, headquarters, specialities etc
                dt_tag_list = about_page_dl_tag.find_all("dt", class_="mb1 text-heading-medium")
                print("found the list of dt tags")
                list_dict_aboutpate = []
                comp_name = "RAis" #section.find("div", class_="block mt2").find("h1").find("span").text.strip()
                """
                about_page_dict = {
                        # "Company Name":comp_name,
                        "Website":'',
                        "Phone":[],
                        "Industry":[],
                        "Company size":[],
                        "Headquarters":[],
                        "Founded":[],
                        "Specialties":[]
                }

                """
                Phone = Industry = Company_size = Headquarters = Founded = Specialties = None
                              
                for tag in dt_tag_list:
                    # print(tag.text.strip())
                    com_ind = tag.text.strip()
                    if com_ind == "Website":
                        Website_tag = tag.find_next_sibling("dd")
                        Website = Website_tag.find("a")['href']
                        # final_result.append(Website)
                        # print("Website", Website)
                    if com_ind == "Phone":
                        Phone_tag1 = tag.find_next_sibling("dd")
                        Phone_tag = Phone_tag1.find("a", class_="link-without-visited-state ember-view")
                        Phone = Phone_tag.find("span", class_="link-without-visited-state").text.strip()
                        # about_page_dict["Phone"].append(Phone)
                        # print("Phone", Phone)
                    if com_ind =="Industry":
                        Industry = tag.find_next_sibling("dd").text.strip()
                        # about_page_dict["Industry"].append(Industry)
                        # print("Industry", Industry)
                    if com_ind =="Company size":
                        Company_size = tag.find_next_sibling("dd").text.strip()
                        # about_page_dict["Company size"].append(Company_size)
                        # print("Company_size", Company_size)
                    if com_ind =="Headquarters":
                        Headquarters = tag.find_next_sibling("dd").text.strip()
                        # about_page_dict["Headquarters"].append(Headquarters)
                        # print("Headquarters", Headquarters)
                    if com_ind =="Founded":
                        Founded = tag.find_next_sibling("dd").text.strip()
                        # about_page_dict["Founded"].append(Founded)
                        # print("Founded", Founded)
                    if com_ind =="Specialties":
                        Specialties = tag.find_next_sibling("dd").text.strip()
                        # about_page_dict["Specialties"].append(Specialties)
                        # print("Specialties", Specialties)

                    about_page_dict = {
                        # "Company Name":comp_name,
                        "Website":[Website],
                        "Phone":[Phone],
                        "Industry":[Industry],
                        "Company size":[Company_size],
                        "Headquarters":[Headquarters],
                        "Founded":[Founded],
                        "Specialties":[Specialties]
                    }
                    final_result.append(about_page_dict)   
    comp_df = pd.DataFrame(about_page_dict, columns=["Website", "Phone", "Industry", "Company size" ,"Headquarters", "Founded", "Specialties"])
    comp_df.to_csv(csv_file_path, mode='a', header=False, index=False)
                    # final_result.append([Website, Phone, Industry, Company_size, Headquarters, Founded, Specialties])
                    # products_df = pd.DataFrame(final_result, columns=['Website','Phone','Industry','Company size','Headquarters','Founded','Specialties'])
                    # products_df.to_csv(csv_file_path, mode='a', header=False, index=False)


                

                # list_dict_aboutpate.append(about_page_dict)
                            
                # # return about_page_dict
                # csv_file_path = 'C:\\Users\\Aridian Technologies\\Desktop\\Office\\Desktop\\Data Scrappers\\Scraping_Companes_On_Linkedin\\Data\\DatacompData_22172024.csv'
                
                
               
                # with open(csv_file_path, mode='a', newline='') as csv_fileComp:
                #     # Create a CSV writer object
                #     csv_writerComp = csv.writer(csv_fileComp)
                #     # If the file is empty, write the header
                #     if csv_fileComp.tell() == 0:
                #         header = list(about_page_dict.keys())
                #         csv_writerComp.writerow(header)

                #     # Write data to the CSV file
                #     for i in range(len(about_page_dict["Website"])):
                #         row_data = [about_page_dict[key][i] for key in about_page_dict]
                #         csv_writerComp.writerow(row_data)
                #         print("Data appended to DatacompData_01172024.csv file.")
                
                # try:
                #     print("Csv is created for about page of company")
                #     with open(csv_file_path, 'x', newline='') as file:
                #         writer = csv.writer(file)
                #         # Write header only if the file is newly created
                #         writer.writerow(about_page_dict.values())
                # except FileExistsError:
                #     print("Exception occured while opeining csv for about comp")
                #     # If the file already exists, open it in append mode
                #     with open(csv_file_path, 'a', newline='') as file:
                #         writer = csv.writer(file)

                #     # Append the new row to the CSV file
                #     with open(csv_file_path, 'a', newline='') as file:
                #         writer = csv.writer(file)
                #         writer.writerow([])  # An empty row to separate new entries

                # print("CSV file created in append mode.")

def compData(driver, comp_about_page):
    print(f"Loading for {comp_about_page}")
    driver.get(comp_about_page)
    time.sleep(2)
    # soup for the about page
    comp_aboutPage_soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(2)
    About_Comp_Data(comp_aboutPage_soup)
    # comp_details_list.append(details_dict)

    """
    # comp_details_list = []
    for about_page in comp_about_page_links:
        print(about_page)
        driver.get(about_page)
        time.sleep(2)
        # soup for the about page
        comp_aboutPage_soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(2)
        details_dict = About_Comp_Data(comp_aboutPage_soup)
        # comp_details_list.append(details_dict)

    # df = pd.DataFrame(comp_details_list)
    # return df
    """


