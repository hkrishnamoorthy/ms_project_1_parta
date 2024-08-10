# import necessary modules
from bs4 import BeautifulSoup
from lxml import etree as et
from csv import writer
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# initialize Chrome webdriver using ChromeDriverManager
#create an instance of the Service object
service = Service(executable_path=ChromeDriverManager().install())
#start Chrome using the service keyword
driver = webdriver.Chrome(service=service)
# open initial URL
BaseUrl ='https://www.naukri.com/data-engineer-jobs?k=data%20engineer'
Urlpagination='https://www.naukri.com/data-engineer-jobs-{}?k=data+engineer'
columns = ['job_title','job_link','company_name','experience','skills','salary','location']

def get_job_data_one_page(url,columns):
    
    #initialize the driver to use chorme from sellenium
    driver.get(url)
    page_content = driver.page_source
    product_soup = BeautifulSoup(page_content, 'html.parser')
    #Initialise the datframe
    df = pd.DataFrame(columns=columns)
    
    
    #Scroll List of all the Jobs in one page 
    job_title_list = list(product_soup.find_all('div',class_=" row1"))
    company_name_list = list(product_soup.find_all('span', class_='comp-dtls-wrap'))
    print("job_title_list is",job_title_list)   
    experience_list = list(product_soup.find_all('span', class_='exp-wrap'))
    skills_list = list(product_soup.find_all('div', class_='row5'))
    salary_list = list(product_soup.find_all('span', class_='sal-wrap ver-line'))
    location_list = list(product_soup.find_all('span', class_='loc-wrap ver-line'))
    
    
    
    #No of Jobs to scroll in a page
    loop_len= len(job_title_list)

    #Get All the columns for each job on that page
    for i in range(loop_len):
            job_title = job_title_list[i].text.strip()
            anchor_tag = job_title_list[i].find('a', class_='title')
            job_link = anchor_tag['href']
            company_name= company_name_list[i].text.strip()
            experience=experience_list[i].text.strip()
            skills= skills_list[i].text.strip()
            salary= salary_list[i].text.strip()
            location= location_list[i].text.strip()
            df2= pd.DataFrame([[job_title,job_link,company_name,experience,skills,salary,location]],columns=columns)
            df = df.concat(df,df2)
            print(df.info())
    return df

driver.get(BaseUrl)
page_content = driver.page_source
product_soup = BeautifulSoup(page_content, 'html.parser')
#Initialise the datframe
df = pd.DataFrame(columns=columns)

print(page_content)

#Scroll List of all the Jobs in one page 
job_title_list = list(product_soup.find_all('div',class_=" row1"))
company_name_list = list(product_soup.find_all('span', class_='comp-dtls-wrap'))
print("job_title_list is",job_title_list)   
experience_list = list(product_soup.find_all('span', class_='exp-wrap'))
skills_list = list(product_soup.find_all('div', class_='row5'))
salary_list = list(product_soup.find_all('span', class_='sal-wrap ver-line'))
location_list = list(product_soup.find_all('span', class_='loc-wrap ver-line'))


df_full = pd.DataFrame(columns=columns)

for page in range(1,2):
    if page==1:
        #page_content for BaseURL
        df_base_url = get_job_data_one_page(BaseUrl,columns)
        df_full=pd.concat([df_full ,df_base_url])
        
        #page_content for other pages     
    else:
        url = Urlpagination.format(page)
        print(url)
        time.sleep(2)
        df_pagination_url = get_job_data_one_page(url,columns)
        df_full=pd.concat([df_full ,df_pagination_url])


print(df.info())
