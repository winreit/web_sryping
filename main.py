
import random
import time
import json
import re
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

PATTERN = re.compile(r"\d+")
def gen_headers():
    browser = random.choices(["chrome", "firefox", "opera"])[0]
    os = random.choices(["win", "mac", "lin"])[0]
    headers = Headers(browser=browser, os=os)
    return headers.generate()

url_adress = 'https://spb.hh.ru/search/vacancy?text=python+django+flask&salary=&ored_clusters=true&area=1&area=2&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line'
response = requests.get(url=url_adress, headers=gen_headers())
print(response.status_code)
html_data = response.text


soup = BeautifulSoup(html_data, 'lxml')
article_list_tag = soup.findAll(class_='vacancy-serp-item__layout')

vacancie = []

for tags in article_list_tag:

    link = tags.find('a')['href']
    salary = tags.find( 'span', "bloko-header-section-2", "vacancy-salary-compensation-type-gross")
    if salary:
        salary = PATTERN.findall(salary.text.strip())
    else:
        salary = 'Не указана'
    company = tags.find('a', class_='bloko-link bloko-link_kind-tertiary').text
    city = tags.find('div',{'data-qa':'vacancy-serp__vacancy-address'}).text




    vacancie.append({
            'Зарплата': salary,
            'Компания': company,
            'Город': city,
            'Сылка': link
    })
    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(vacancie, file, ensure_ascii=False, indent=4)

print(vacancie)



    # print(tags)
    # print('---' * 10)
    # print(link)
    # print('---' * 10)
    # print(salary)
    # print('---' * 10)
    # print(company)
    # print('---' * 10)
    # print(city)
    # # print(link_absolute)

