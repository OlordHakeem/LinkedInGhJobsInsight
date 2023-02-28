import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

'''
API_KEY = '4a824624-dfe7-4626-992b-e6ee39c067b1'

def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url
'''


class RemoteSpider(scrapy.Spider):
    name = 'remote'
    api_url ='https://gh.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=&location=Ghana&locationId=&geoId=105769538&f_TPR=&f_WT=2&position=1&pageNum=0&start='
    

    def start_requests(self):

        first_profile_on_page = 0
        first_url = self.api_url + str(first_profile_on_page)
        yield SeleniumRequest(url=first_url, callback = self.parse_job_profile, meta={'first_profile_on_page' : first_profile_on_page}, wait_time=20, dont_filter = True)


    def parse_job_profile(self,response):
        first_profile_on_page = response.meta['first_profile_on_page']

        remote_jobs = response.xpath("//li")

        num_jobs_returned = len(remote_jobs)

        for jobs in remote_jobs:

            job_profiles = jobs.xpath('.//a/@href').get(default = 'Not Found').strip()
            job_date = jobs.xpath(".//time/@datetime").get(default = 'Non Found').strip()
            
            yield job_profiles
             
          #  job_item = jobs.xpath('.//a/@href').get(default = 'Not Found').strip()
            yield SeleniumRequest(url = job_profiles, callback = self.parse_job_profile,meta = {'first_profile_on_page' : first_profile_on_page, 'job_date' : job_date}, wait_time=20,)

             
          
            

        if num_jobs_returned > 0:
            first_profile_on_page = int(first_profile_on_page) + 25
            next_url = self.api_url + str(first_profile_on_page)
        
            yield SeleniumRequest(url = next_url, callback = self.parse_job_profile,meta = {'first_profile_on_page' : first_profile_on_page, 'job_date' : job_date} , wait_time = 20)
            

    def parse_remote_job(self,response):
        
        job_date = response.meta['job_date']
        
        job_title = response.xpath(".//h1 [@class = 'top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title']/text()").get(default= 'Not Found').strip()
        hiring_company = response.xpath(".//a/@title").get(default= 'Not Found').strip()
        total_number_of_applicants = response.xpath("//div[@class = 'topcard__flavor-row']/span[@class='num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet']/text()").get(default = 'Not Found').strip()
        level = response.xpath("(//span[@class = 'description__job-criteria-text description__job-criteria-text--criteria'])[1]/text()").get(default = 'Not Found').strip()
        emp_type = response.xpath("(//span[@class = 'description__job-criteria-text description__job-criteria-text--criteria'])[2]/text()").get(default = 'Not Found').strip()
        function = response.xpath("(//span[@class = 'description__job-criteria-text description__job-criteria-text--criteria'])[3]/text()").get(default = 'Not Found').strip()
        industries = response.xpath("(//span[@class = 'description__job-criteria-text description__job-criteria-text--criteria'])[4]/text()").get(default = 'Not Found').strip()
        total_number_of_aplicants_2 = response.xpath("//figcaption [@class= 'num-applicants__caption']/text()").get(default = 'Not Found').strip()
        

        job_details={
                'Date' : job_date,
                'Job Title' : job_title,
                'Hiring Company' : hiring_company,
                'Total Applicants' : total_number_of_applicants,
                'T_Apps2' :total_number_of_aplicants_2,
                'Level' : level,
                'Type' : emp_type,
                'Function' : function,
                'Industries' : industries

                }

        yield job_details
        
