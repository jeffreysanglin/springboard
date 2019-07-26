from os import path, getcwd, chdir
import requests
import json
import csv
from itertools import chain

import pandas as pd
from IPython.display import FileLink

#from utils.jupy_util import display_all

#Create File pathing
LOCAL_DIR = getcwd()
DATA_DIR = path.join(LOCAL_DIR, 'data','scorecard')
DPATH = path.join(DATA_DIR,'cap1_api_data.csv')
DESC_PATH = path.join(DATA_DIR,'cap1_data_desc.csv')
COLUMN_NAMES = path.join(DATA_DIR,'column_names.csv')

API_KEY = <inser_api_key>
#API_URL = 'https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?api_key={api_key}'.format(api_key=API_KEY)


class scorecardApi(object):
    """docstring for scorecardApi"""
    class RateLimitError(Exception):
        """Raised when API rate limit has been reached."""
        pass
    
    class StatusCodeError(Exception):
        """Raised when getting a non-200 status code."""
        pass
    
    def __init__(self, api_key=API_KEY, api_fields=None):
        #format url with api_key paramater
        BASE_URL = 'https://api.data.gov/ed/collegescorecard/v1/schools.json?'
        key_param = 'api_key={api_key}'.format(api_key=api_key)
        formatted_url = ''.join([BASE_URL,key_param])
        #format the url with field paramater
        field_param = 'fields={field_param}'.format(field_param=(','.join(api_fields)))
        formatted_url = '&'.join([formatted_url,field_param])

        self.api_url = formatted_url


    def callAPI(self, items_per_page=100, page=1,verbose=False):        
        #format the url with page size paramater
        per_param = 'per_page={per_page_num}'.format(per_page_num=items_per_page)
        formatted_url = '&'.join([self.api_url,per_param])

        #format the url with page number parameter
        page_param = 'page={page_num}'.format(page_num=page)
        formatted_url = '&'.join([formatted_url,page_param])
        
        #Call the API
        page = requests.get(formatted_url)
        stat_code = page.status_code
        if stat_code != 200:
            #print(dir(page))
            print(page.reason)
            raise self.StatusCodeError(stat_code, page.reason,page_param)
        data = page.json()#['results']
        if data.get("error") != None:
            raise self.RateLimitError(data['error']['code'],": ",data['error']['message'])
        #except KeyError:
        #    print(page.json())
        
        return(data)

    def collectData(self):
        data_list = []
        page_counter = 1
        continue_pagination = True
        i_pp = 100
        
        while continue_pagination:
            try:
                data_page = self.callAPI(items_per_page=i_pp, page=page_counter)
                page_counter +=1
                #print(len(data_page['results']))
            except self.RateLimitError:
                time.sleep(60)
                continue
            
            data_list.append(data_page['results'])

            if len(data_page['results']) < i_pp:
                continue_pagination == False
                break
            
        return(data_list)

api_fields = [
    'id'
    ,'location.lat'
    ,'location.lon'
    ,'school.zip'
    ,'school.under_investigation'
    ,'school.main_campus'
    ,'school.degrees_awarded.highest'
    ,'school.state_fips'
    ,'school.degree_urbanization'
    ,'school.carnegie_basic'
    ,'school.carnegie_undergrad'
    ,'school.minority_serving.historically_black'
    ,'school.minority_serving.predominantly_black'
    ,'school.minority_serving.annh'
    ,'school.minority_serving.tribal'
    ,'school.minority_serving.aanipi'
    ,'school.minority_serving.hispanic'
    ,'school.minority_serving.nant'
    ,'school.men_only'
    ,'school.women_only'
    ,'school.religious_affiliation'
    ,'latest.admissions.admission_rate.overall'
    ,'latest.admissions.sat_scores.midpoint.critical_reading'
    ,'latest.admissions.sat_scores.midpoint.math'
    ,'latest.admissions.sat_scores.midpoint.writing'
    ,'latest.admissions.act_scores.midpoint.cumulative'
    ,'latest.admissions.act_scores.midpoint.english'
    ,'latest.admissions.act_scores.midpoint.math'
    ,'latest.admissions.act_scores.midpoint.writing'
    ,'latest.admissions.sat_scores.average.overall'
    ,'latest.academics.program_percentage.agriculture'
    ,'latest.academics.program_percentage.resources'
    ,'latest.academics.program_percentage.architecture'
    ,'latest.academics.program_percentage.ethnic_cultural_gender'
    ,'latest.academics.program_percentage.communication'
    ,'latest.academics.program_percentage.communications_technology'
    ,'latest.academics.program_percentage.computer'
    ,'latest.academics.program_percentage.personal_culinary'
    ,'latest.academics.program_percentage.education'
    ,'latest.academics.program_percentage.engineering'
    ,'latest.academics.program_percentage.engineering_technology'
    ,'latest.academics.program_percentage.language'
    ,'latest.academics.program_percentage.family_consumer_science'
    ,'latest.academics.program_percentage.legal'
    ,'latest.academics.program_percentage.english'
    ,'latest.academics.program_percentage.humanities'
    ,'latest.academics.program_percentage.library'
    ,'latest.academics.program_percentage.biological'
    ,'latest.academics.program_percentage.mathematics'
    ,'latest.academics.program_percentage.military'
    ,'latest.academics.program_percentage.multidiscipline'
    ,'latest.academics.program_percentage.parks_recreation_fitness'
    ,'latest.academics.program_percentage.philosophy_religious'
    ,'latest.academics.program_percentage.theology_religious_vocation'
    ,'latest.academics.program_percentage.physical_science'
    ,'latest.academics.program_percentage.science_technology'
    ,'latest.academics.program_percentage.psychology'
    ,'latest.academics.program_percentage.security_law_enforcement'
    ,'latest.academics.program_percentage.public_administration_social_service'
    ,'latest.academics.program_percentage.social_science'
    ,'latest.academics.program_percentage.construction'
    ,'latest.academics.program_percentage.mechanic_repair_technology'
    ,'latest.academics.program_percentage.precision_production'
    ,'latest.academics.program_percentage.transportation'
    ,'latest.academics.program_percentage.visual_performing'
    ,'latest.academics.program_percentage.health'
    ,'latest.academics.program_percentage.business_marketing'
    ,'latest.academics.program_percentage.history'
    ,'school.online_only'
    ,'latest.cost.avg_net_price.public'
    ,'latest.cost.avg_net_price.private'
    ,'school.faculty_salary'
    ,'latest.completion.completion_rate_4yr_150nt'
    ,'latest.student.retention_rate.four_year.full_time'
    ,'latest.repayment.repayment_cohort.1_year_declining_balance'
    ,'latest.student.share_lowincome.0_30000'
    ,'latest.student.share_independent_students'
    ,'latest.student.share_firstgeneration'
    ,'latest.student.share_firstgeneration_parents.middleschool'
    ,'latest.student.share_firstgeneration_parents.highschool'
    ,'latest.student.share_firstgeneration_parents.somecollege'
    ,'latest.aid.loan_principal'
    ,'latest.aid.median_debt.completers.overall'
    ,'latest.aid.median_debt.noncompleters'
    ,'latest.aid.median_debt.female_students'
    ,'latest.aid.median_debt.male_students'
    ,'latest.aid.median_debt.first_generation_students'
    ,'latest.aid.median_debt.non_first_generation_students'
    ,'latest.student.family_income.overall'
    ,'latest.student.family_income.dependent_students'
    ,'latest.student.family_income.independent_students'
    ,'latest.student.demographics.poverty_rate'
    ,'latest.student.demographics.unemployment'
    ,'latest.earnings.6_yrs_after_entry.median'
    ,'latest.earnings.7_yrs_after_entry.mean_earnings'
]

#scorecard_data = scorecardApi(api_fields=api_fields)
scorecard_data = scorecardApi(api_fields=api_fields)
data = scorecard_data.collectData()

#data = scorecardApi(fields=api_fields,page=2,per_page=10)
#display(data)
df_list = []

for i in data:
    df = pd.DataFrame(i)
    df_list.append(df)

#df = pd.DataFrame(data)
df = pd.concat(df_list)
print(df.shape)
#display_all(df.head())
#display(df.loc[:,'latest.earnings.6_yrs_after_entry.median'].head())

df.to_csv(DPATH,index=False)

df_desc = df.describe()
print(df_desc.shape)
df_desc.loc['null',:] = df_desc.loc['count','id'] - df_desc.loc['count',:]

df_desc.to_csv(DESC_PATH)
#display(FileLink('./cap1_data_describe.csv'))