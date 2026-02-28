import requests
import json 
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Database Connection (Apne credentials daal lijiye)
connection = mysql.connector.connect(host='localhost', database='indiamart', user='root', password='Naveen7549@')
cursor = connection.cursor()

headers = {
    'authority': '',
    'accept': '',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', # Added a dummy user agent
    'x-requested-with': '',
    'sec-fetch-site': '',
    'sec-fetch-mode': '',
    'sec-fetch-dest': '',
    'referer': '',
    'accept-language': '',
    'cookie': '',
    'dnt': '',
}

BASE_URL = "https://dir.indiamart.com"
url = "https://dir.indiamart.com/industry/apparel-garments.html"

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, features='lxml')
industry = soup.find('div', {"class": "mid"}).find('h1').text
category_list = soup.find_all('li', {"class": "q_cb"})

startTime = datetime.now()
print("Start Time: ", startTime)

s_count = 0
for category in category_list:
    response = requests.get(BASE_URL + category.find('a')['href'])
    soup = BeautifulSoup(response.text, features='lxml')
    sub_cat_title_list = soup.find_all('li', {"class": "box"})

    for sub_cat_title in sub_cat_title_list:
        cat_name = sub_cat_title.find('a').text
        sub_cat_link_list = sub_cat_title.find_all('a', {"class": "slink"})

        for sub_cat_link in sub_cat_link_list:
            response = requests.get(BASE_URL + sub_cat_link['href'])
            soup = BeautifulSoup(response.text, features='lxml')
            mcatid = soup.find('ul', {"class":"wlm"})
            
            # Error Check: In case 'wlm' class is not found
            if mcatid is None or 'data-click' not in mcatid.attrs:
                continue
                
            mcatid = mcatid['data-click'].split('|')[1]

            i = 0
            while True:
                params = {
                    'mcatId': mcatid,
                    'glid': '104881740',
                    'prod_serv': 'P',
                    'mcatName': '', 
                    'srt': i*28 + 1,
                    'end': i*28 + 28,
                    'ims_flag': '',
                    'cityID': '',
                    'prc_cnt_flg': '1',
                    'fcilp': '0',
                    'spec': '',
                    'pr': '0',
                    'pg': i + 1,
                    'frsc': i*28,
                    'video': ''
                }

                response = requests.get('https://dir.indiamart.com/impcat/next', headers=headers, params=params)
                json_data = json.loads(response.text)
                soup = BeautifulSoup(json_data['content'], features='lxml')
                suppliers_link_list = soup.find_all("a", {"class": "fs18 ptitle"})
                
                company_name = ''
                owner_name = ''
                address = ''
                website = ''
                phone = ''
                product_desc = ''

                if len(suppliers_link_list) > 0:
                    for supplier_link in suppliers_link_list:
                        supplier_page_url = supplier_link['href']
                        
                        try:
                            response = requests.get(supplier_page_url)
                            soup = BeautifulSoup(response.text, features='lxml')
                            seller_contact_details = soup.find('div',{"class": "fs13 color1 pml10"})

                            if seller_contact_details is not None:
                                comp_obj = seller_contact_details.find('div', {"class": "fs15"})
                                if comp_obj and comp_obj.find('a', {"class": "pcmN bo"}):
                                    company_name = comp_obj.find('a', {"class": "pcmN bo"}).string
                                
                                owner_obj = seller_contact_details.find('div', {"class": "pt8 color1"})
                                if owner_obj and owner_obj.find('div', {"id":"supp_nm"}):
                                    owner_name = owner_obj.find('div', {"id":"supp_nm"}).string

                                address_obj = seller_contact_details.find('span', {"class": "color1 dcell verT fs13"})
                                if address_obj:
                                    address = address_obj.get_text()
                                
                                web_obj = seller_contact_details.find('div', {"class": "mt5"})
                                if web_obj and web_obj.find('a', {"class": "color1 utd"}):
                                    website = web_obj.find('a', {"class": "color1 utd"}).string
                                
                                phone_obj = seller_contact_details.find('div', {"class": "pdpmt14"})
                                if phone_obj and phone_obj.find('span', {"class": "duet"}):
                                    phone = phone_obj.find('span', {"class": "duet"}).string

                            # Processing about, descriptions, etc.
                            about = {}
                            product_details = {}
                            product_info = {}
                            
                            # --- FIX: Database Insertion Logic ---
                            # MySQL Query parameterization (Prevents SQL Syntax errors)
                            sql_query = """
                                INSERT INTO apparel 
                                (industry, sub_cat, supplier_url, company_name, owner, address, website, phone, about, product_detail, product_desc, product_info) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
                            
                            # Values tuple
                            values = (
                                str(industry), str(cat_name), str(supplier_page_url), str(company_name), 
                                str(owner_name), str(address), str(website), str(phone), 
                                str(about), str(product_details), str(product_desc), str(product_info)
                            )

                            try:
                                # Execute aur Commit dono Try block ke andar hone chahiye
                                cursor.execute(sql_query, values)
                                connection.commit()
                                s_count = s_count + 1
                            except Error as e:
                                print(f"DB ERROR: {e}")
                                print(f"COMPANY: {company_name}, URL: {supplier_page_url}")
                                
                        except Exception as e:
                            print(f"Scraping Error at {supplier_page_url}: {e}")

                else:
                    print("Category finished")
                    break
                print(f"Page {i} done")
                i = i + 1

print("DONE: ", industry)
print("Start Time: ", startTime)
print("End Time: ", datetime.now() - startTime)
print("Suppliers: ", s_count)

cursor.close()
connection.close()