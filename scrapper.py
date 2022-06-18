import requests
from bs4 import BeautifulSoup

def get_last_page(url):
  result = requests.get(url)
  
  soup = BeautifulSoup(result.text,"html.parser")
  
  pagination = soup.find("div",{"class":"pagination"})
  links = pagination.find_all("a")
  
  pages=[]
  for link in links[0:-1]:
    pages.append(int(link.string))
  last_page = pages[-1]

  return last_page

def extract_job_data(soup):
  title = soup.find("h2",{"class","jobTitle"}).find("span",title=True).string
  company = soup.find("span",{"class":"companyName"})
  company_anchor = company.find("a")
  if company_anchor is not None:
    company = company_anchor.string
  else:
    company = company.string
  location = soup.find("div",{"class":"companyLocation"}).string
  job_id = soup.find("a")["data-jk"]
  return {
  'title':title,
  'company':company,
  'location':location,
  'link': f"https://pk.indeed.com/viewjob?cmp=&jk={job_id}&from=web&vjs=3"
  }

def extract_jobs(last_page,url):
  jobs=[]
  for page in range(last_page):

    # just for my mental health
    print(f"Scrapping page {page}")  
    result = requests.get(f"{url}&start={page*10}")
    soup = BeautifulSoup(result.text,"html.parser")
    results = soup.find_all("td" , {"class" : "resultContent"})
    
    for result in results:
      job = extract_job_data(result)
      jobs.append(job)
    
  return jobs

def get_jobs(word):
  url = f"https://pk.indeed.com/jobs?q={word}&l=Pakistan"
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page,url)
  return jobs