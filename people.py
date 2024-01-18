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





def profile_page_data(driver, profile_page_html):
    soup = BeautifulSoup(profile_page_html, 'html.parser')
    time.sleep(2)
    # Parsing through each profile page html and extract the profile data
    profile_data = {
    "Name": [],
    "Profile Title": [],
    "Job": [],
    "Company Name": [],
    "Email": [],
    "Location": []
    }
    #Fetching the name of the profile
    name_tag = soup.find("h1", class_='text-heading-xlarge inline t-24 v-align-middle break-words')
    name = name_tag.text.strip()
    profile_data["Name"].append(name)
    print(f"name is: {name}")

    # Fetching the profile tag
    profile_title_tag = soup.find("div", class_='text-body-medium break-words')
    profile_title = profile_title_tag.text.strip()
    profile_data["Profile Title"].append(profile_title)
    print(f"Profile Title is: {profile_title}")
    # print("Profile Title tag line", profile_title_tag.text.strip())

    # Fetching the job title of the profile
    sections = soup.find_all("section")

    final_res = [] #["name", "profile_title", "Job", "Company" ,"email", "Location"]
    for section in sections:
        div = section.find("div", id="experience")
        p_job = company = None
        if div:
            div_exp_tag = section.find("div",class_="pvs-list__outer-container")
            profile_job_tag = div_exp_tag.find("div", class_='display-flex flex-wrap align-items-center full-height')
            job = profile_job_tag.find('span', {"aria-hidden":"true"})
            p_job = job.text.strip()
            print(job.text.strip())
            profile_job_company_tag = div_exp_tag.find("span", class_='t-14 t-normal')
            company_name_tag = profile_job_company_tag.find('span', {"aria-hidden": "true"})
            company = company_name_tag.text.strip().split("·")[0]
            profile_data["Job"].append(job.text.strip())
            profile_data["Company Name"].append(company)
            print(f"Job is: {job.text.strip()}")
            print(f"company is: {company}")

    # print("Job title", job.text.strip())

    # Fetching the name of a company a profile holder working in
    """
    sections = soup.find_all("section")
    for section in sections:
        div = section.find("div", id="experience")
        if div:
            div_exp_tag = section.find("div",class_="pvs-list__outer-container")
            profile_job_company_tag = div_exp_tag.find("span", class_='t-14 t-normal')
            company_name_tag = profile_job_company_tag.find('span', {"aria-hidden": "true"})
            company = company_name_tag.text.strip().split("·")[0]
            profile_data["Company Name"].append(company)
            # print("Company Name", company)

    """
    # Fetching the location of profile holder working
    location = soup.find('span', class_='text-body-small inline t-black--light break-words')
    loc = location.text.strip()
    profile_data["Location"].append(loc)
    # print(location.text.strip())

    # Fetching the link for profile info page
    profile_info_page_link = soup.find("a", id='top-card-text-details-contact-info')
    profile_contact_info_link = "https://www.linkedin.com" + profile_info_page_link['href']
    driver.find_element(By.ID, "top-card-text-details-contact-info").click()
    time.sleep(2)
    driver.get(profile_contact_info_link)
    time.sleep(1)
    email_page = driver.page_source
    soup = BeautifulSoup(email_page, 'html.parser')
    div_tag = soup.find('a', {"class":"bWCFkfQvJKVrOchJdgENAUvGnHahyLIMLqpA link-without-visited-state t-14", "target":"_blank", "rel":"noopener noreferrer"})
    if div_tag:
        email = div_tag.text.strip()
        profile_data["Email"].append(email)
        # print(div_tag.text.strip())
    else:
        email = None
        profile_data["Email"].append(None)

    

    csv_file_path = "C:\\Users\\Aridian Technologies\\Desktop\\Office\\Desktop\\Data Scrappers\\Scraping_Companes_On_Linkedin\\Data\\linkedInData_25172024.csv"
    final_res.append([name, profile_title, p_job, company, email, loc])

    print("The data in final_res is: ", final_res[0])

    comp_df1 = pd.DataFrame(final_res[0], columns=["name", "profile_title", "Job", "Company" ,"email", "Location"])
    comp_df1.to_csv(csv_file_path, mode='a', header=True, index=False)
    
    
    """
    with open("C:\\Users\\Aridian Technologies\\Desktop\\Office\\Desktop\\Data Scrappers\\Scraping_Companes_On_Linkedin\\Data\\linkedInData_22172024.csv", mode='a', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)
        # If the file is empty, write the header
        if csv_file.tell() == 0:
            header = list(profile_data.keys())
            csv_writer.writerow(header)

        # Write data to the CSV file
        for i in range(len(profile_data["Name"])):
            row_data = [profile_data[key][i] for key in profile_data]
            csv_writer.writerow(row_data)
            print("Data appended to linkedInData_01172024.csv file.")

    """



def proData(driver, df):
    if df.empty:
        print("The DataFrame is empty.")
    else:
        # Filter rows with duplicate names
        duplicates_df = df[df.duplicated('name', keep=False)]

        # Select unique names from the 'name' column
        unique_names = duplicates_df['name'].unique()

        selected_links = duplicates_df['profile_link'].unique()

        for link in selected_links:
            driver.get(link)
            time.sleep(1)
            profile_html = driver.page_source
            profile_page_data(driver, profile_html)

    """
    duplicates_df = df[df.duplicated('profile_link', keep=False)]
    unique_names = duplicates_df['profile_link'].unique()
    if unique_names:
        unique_names_no_duplicates = pd.Series(unique_names).drop_duplicates().tolist()
        # print(f"Name: {name}")
        try:
            for link in unique_names_no_duplicates:
                print("The unique link from dataframe is", link)
                pro_link = link
                driver.get(pro_link)
                time.sleep(1)
                profile_html = driver.page_source
                profile_page_data(driver, profile_html)
        except:
            print("No profile exists in this page")
    """
    # cols = ["name", "profile_link"]
    # for name, group in df.groupby(by = cols):
    #     # Extract unique profile links for each unique name
    #     unique_profile_links = group['profile_link'].unique()
        
    #     # Print or process the unique name and corresponding profile links
    #     print(f"Name: {name}")
    #     for link in unique_profile_links:
    #         pro_link = link
    #         driver.get(pro_link)
    #         time.sleep(1)
    #         profile_html = driver.page_source
    #         profile_page_data(driver, profile_html)

def compTopEmp(driver, comp_people_page):
    print(f"About page link {comp_people_page}")
    key_words = ["manager", "Co-founder","CEO",  "cto", "director"]

    lst_of_emp = []
    for word in key_words:
        people_page = f"{comp_people_page}?keywords={word}"
        driver.get(people_page)
        time.sleep(4)
        people_html = driver.page_source
        # Creating a soup for the people page
        people_html_soup = BeautifulSoup(people_html, 'html.parser')
        time.sleep(1)
        main_div_tag = people_html_soup.find("div", class_="artdeco-card org-people-profile-card__card-spacing org-people__card-margin-bottom")
        if main_div_tag:
            div_emp_tag = main_div_tag.find("ul", class_="display-flex list-style-none flex-wrap")
            emp_list = div_emp_tag.find_all("li", class_="grid grid__col--lg-8 block org-people-profile-card__profile-card-spacing")
            name = profile_link = None
            for emp in emp_list:
                div_tag = emp.find("div", {"class":"artdeco-entity-lockup__image artdeco-entity-lockup__image--type-circle ember-view"})
                prof_link_a_tag = div_tag.find("a")
                name_div_tag = div_tag.find_next_sibling("div", class_="artdeco-entity-lockup__content ember-view")
                div_nam = name_div_tag.find("div", class_="artdeco-entity-lockup__title ember-view")
                pro_name = div_nam.find("div", class_="ember-view lt-line-clamp lt-line-clamp--single-line org-people-profile-card__profile-title t-black")
                
                if pro_name:
                    name = pro_name.text.strip()
                
                if prof_link_a_tag:
                    pro_link = prof_link_a_tag['href']
                    profile_link = pro_link
                dict = {"name":name, "profile_link":profile_link}
                lst_of_emp.append(dict)
    df = pd.DataFrame(lst_of_emp)
    print('df is created moving to next function')
    proData(driver, df)



    """
    lst_of_emp = []
    for comp_ppl_page in comp_people_page_links[:5]:
        key_words = ["manager", "Co-founder","CEO",  "cto", "director"]
        print(comp_ppl_page)
        
        for word in key_words:
            people_page = f"{comp_ppl_page}?keywords={word}"
            driver.get(people_page)
            time.sleep(4)
            people_html = driver.page_source
            # Creating a soup for the people page
            people_html_soup = BeautifulSoup(people_html, 'html.parser')
            time.sleep(1)
            main_div_tag = people_html_soup.find("div", class_="artdeco-card org-people-profile-card__card-spacing org-people__card-margin-bottom")
            if main_div_tag:
                div_emp_tag = main_div_tag.find("ul", class_="display-flex list-style-none flex-wrap")
                emp_list = div_emp_tag.find_all("li", class_="grid grid__col--lg-8 block org-people-profile-card__profile-card-spacing")
                name = profile_link = None
                for emp in emp_list:
                    div_tag = emp.find("div", {"class":"artdeco-entity-lockup__image artdeco-entity-lockup__image--type-circle ember-view"})
                    prof_link_a_tag = div_tag.find("a")
                    name_div_tag = div_tag.find_next_sibling("div", class_="artdeco-entity-lockup__content ember-view")
                    div_nam = name_div_tag.find("div", class_="artdeco-entity-lockup__title ember-view")
                    pro_name = div_nam.find("div", class_="ember-view lt-line-clamp lt-line-clamp--single-line org-people-profile-card__profile-title t-black")
                    
                    if pro_name:
                        name = pro_name.text.strip()
                    
                    if prof_link_a_tag:
                        pro_link = prof_link_a_tag['href']
                        profile_link = pro_link
                    dict = {"name":name, "profile_link":profile_link}
                    lst_of_emp.append(dict)

        df = pd.DataFrame(lst_of_emp)
        # print(df)
        proData(driver, df)
    """