#]Libraries  
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Main Class
class RemoteJob:

    #Data Import
    def dataset(self):

        data = pd.read_json('LinkedIn_Ghana_Remote_Jobs.json')
        return data
    

    #Data Cleaning
    def clean_data(self):
        
        data_frame = self.dataset().copy()
        data_frame['Date'] = pd.to_datetime(data_frame['Date'])
        data_frame.set_index('Date',inplace=True)
        data_frame.sort_values('Date',inplace = True)
        data_frame['Count'] = 1
        data_frame['amount'].replace('Not Found',np.nan,inplace = True)

        data_frame.to_excel('Clean Remote Job.xlsx', index = False)
        return data_frame



    #Top10 Hot Jobs
    def top10_jobs(self):

        hot_jobs = self.clean_data().copy()
        hot_jobs = hot_jobs.groupby('job_title').count()
        hot_jobs = hot_jobs.sort_values('amount',ascending = False).iloc[0:10]

        hot_jobs.to_excel('top10Jobs.xlsx', index = False)
        
        #Plotting
        plt.figure()
        plt.bar(hot_jobs.index, hot_jobs['hiring_status'])
        plt.xticks(rotation = 70)
        #plt.show()

        #hot_jobs.to_json('Top10 Most Demanding Remote Jobs.json',index = False)
        return hot_jobs 

    
    #Growth Of Remote Jobs Over the Year
    def growth(self):
        no_jobs = self.clean_data().copy()
        no_jobs = no_jobs.groupby(no_jobs.index).count()
        
        #Plotting
        plt.figure()
        plt.plot(no_jobs.index,no_jobs['count'])
        #plt.show()
        
        no_jobs.to_excel('growth.xlsx',index = False)



        return no_jobs
        
    def price(self):

        payment = self.clean_data().copy()
        payment = payment.loc[payment['amount'].notnull()]['amount']
        return payment

        
        
    
class EntryJobs:

    #Entry Job Dataset Import
    def entry_dataset(self):

        entry_dataframe = pd.read_json('LinkedIn_Ghana_Entry_Remote_Jobs.json')
        return entry_dataframe
    

    #Data Cleaning
    def cleaned_entry(self):
        
        clean_entry = self.entry_dataset().copy()
        clean_entry['date'] = pd.to_datetime(clean_entry['date'])
        clean_entry.set_index('date',inplace=True)
        clean_entry.sort_values('date',inplace = True)
        clean_entry['count'] = 1
        clean_entry['amount'].replace('Not Found',np.nan,inplace = True)
        clean_entry.to_excel('entry remote jobs.xlsx',index = False)
        return clean_entry

    #Top10 Hot Entry Jobs
    def top10_entry_jobs(self):

        hot_entry_jobs = self.cleaned_entry().copy()
        hot_entry_jobs = hot_entry_jobs.groupby('job_title').count()
        hot_entry_jobs = hot_entry_jobs.sort_values('amount',ascending = False).iloc[0:10]


        hot_entry_jobs.to_excel('entry top10 jobs.xlsx',index = False)

        #Plotting
      #  plt.figure()
      #  plt.bar(hot_entry_jobs.index, hot_entry_jobs['job_title'])
        plt.xticks(rotation = 70)
        #plt.show()

        #hot_jobs.to_json('Top10 Most Demanding Remote Jobs.json',index = False)
        return hot_entry_jobs 

    
    #Growth Of Remote Jobs Over the Year
    def entry_growth(self):
        no_entry_jobs = self.cleaned_entry().copy()
        no_entry_jobs = no_entry_jobs.groupby(no_entry_jobs.index).count()
        
        #Plotting
        plt.figure()
        plt.plot(no_entry_jobs.index,no_entry_jobs['count'])
       # plt.show()

        no_entry_jobs.to_excel('entry growth.xlsx',index = False)

        return no_entry_jobs
        
    def entry_price(self):

        entry_pay = self.cleaned_entry().copy()
        entry_pay = entry_pay.loc[entry_pay['amount'].notnull()]['amount']
        return entry_pay



'''' First Class (Full Remote Jobs) '''

#Unclean Json File
raw_df=RemoteJob().dataset()

#Clean Json File
clean_df = RemoteJob().clean_data()

#Top10 Hot Jobs
hot = RemoteJob().top10_jobs()

#Growth of Remote Jobs
jobs = RemoteJob().growth()

price = RemoteJob().price()

''' Second Class (Entry Remote Jobs)'''

#Remote Entry Jobs Cleaned
entry_df = EntryJobs().cleaned_entry()

#Top10 Hot Jobs
entry_hot = EntryJobs().top10_entry_jobs()   

#Growth Of Remote Jobs
entry_growth = EntryJobs().entry_growth()

e_price = EntryJobs().entry_price()
