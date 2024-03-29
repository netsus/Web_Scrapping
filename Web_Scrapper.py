import pandas as pd
import requests  # URL 가져오는 좋은 라이브러리
from bs4 import BeautifulSoup  # HTML에서 원하는 정보 가져오기 좋은 라이브러리
import csv

def save_to_file(word,jobs):
    with open(f'{word}_jobs.csv',mode='w', encoding='utf-8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["company", "location","link", "job"])
        for job in jobs:
            row = list(job.values())
#             import pdb;pdb.set_trace()
            writer.writerow(row)
    return True

def indeed_get_last_page(URL):
    result = requests.get(URL)

    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find('div', {'class': 'pagination'})
    if pagination:
        links = pagination.find_all('a')

        pages = [int(link.string) for link in links[:-1]]
        max_page = pages[-1]
    else:
        max_page=0

    return max_page


def indeed_extract_job(html):
    title = html.find("h2", {"class": "title"})
    anchor_title = title.find("a")["title"]
    company = html.find("span", {'class': 'company'})
    company_anchor = company.find("a")
    if company_anchor is not None:
        company_name = str(company_anchor.string)
    else:
        company_name = str(company.string)
    company_name = company_name.strip()
    location = html.find("div", {'class': 'recJobLoc'})
    if location is None:
        print(html)
    else:
        location = location['data-rc-loc']
    job_id = html["data-jk"]
    return {
        'title': anchor_title,
        'company': company_name,
        'location': location,
        'link': f"https://www.indeed.com/viewjob?jk={job_id}"
    }


def indeed_extract_jobs(last_page,URL,LIMIT):
    jobs = list()
    for page in range(last_page):
        print(f"Scrapping indeed Page: {page}")
        page_result = requests.get(f"{URL}&start={page*LIMIT}")
        page_soup = BeautifulSoup(page_result.text, 'html5lib')
        job_results = page_soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})
        for job_result in job_results:
            job = indeed_extract_job(job_result)
            jobs.append(job)
    return jobs

def indeed_get_jobs(word):
    LIMIT = 25
    URL = f"https://www.indeed.com/jobs?q={word}&limit={LIMIT}"
    last_page = indeed_get_last_page(URL)
    last_page = 1
    jobs = indeed_extract_jobs(last_page,URL,LIMIT)
    return jobs

import requests  # URL 가져오는 좋은 라이브러리
from bs4 import BeautifulSoup  # HTML에서 원하는 정보 가져오기 좋은 라이브러리

def SO_get_last_page(URL):
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'lxml')
    links = soup.find("div", {'class': 's-pagination'})
    if links:
        links = links.find_all("a")
        last_page = int(links[-2].get_text().strip())
    else:
        last_page = 0
    return last_page

def SO_extract_job(html):
    # title, company, location, link
    title = html.find("h2", {
        "class": "mb4 fc-black-800 fs-body3"
    }).find("a")['title']
    company_tag, location_tag = html.find("h3", {
        'class': 'fc-black-700 fs-body1 mb4'
    }).find_all("span", recursive=False)
    company = company_tag.get_text(strip=True)
    location = location_tag.get_text(strip=True)
    job_id = html['data-jobid']
    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f"https://stackoverflow.com/jobs/{job_id}"
    }

def SO_extract_jobs(last_page,URL):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO Page: {page}")
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, 'lxml')
        results = soup.find_all("div", {'class': '-job'})
        for result in results:
            job = SO_extract_job(result)
            jobs.append(job)
    return jobs

def SO_get_jobs(word):
    URL = f"https://stackoverflow.com/jobs?q={word}&sort=i"
    last_page = SO_get_last_page(URL)
    last_page = 1
    jobs = SO_extract_jobs(last_page,URL)
    return jobs