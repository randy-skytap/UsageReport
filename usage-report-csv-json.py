#! python3 
# Create a report for SVMs in both CSV and JSON formats
# 
# NOTES:  Does not handle pagination in this evolution.

import json
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from io import StringIO
import time

now = datetime.now()
end_date = now.isoformat()
start_date = now - timedelta(days=7)
start_date = start_date.isoformat()
reporting_data = {}
header_api = {'content-type': 'application/json', 'accept': 'application/json'}
uri_skytap = 'https://cloud.skytap.com/'
usr_skytap = '<Skytap Username>'
pwd_skytap = '<Skytap API Token>'
auth_skytap = (usr_skytap, pwd_skytap)

def skytap(pth,action=None,json_data=None):
    """
    Essential Skytap API calls with url path, action, and JSON data as needed.  
    """
    url_path = pth if uri_skytap in pth else uri_skytap + pth
    
    if action == None and '.csv' in pth:
        request_out = requests.get(url_path, stream= True, auth=auth_skytap, headers = header_api)
        return request_out
    elif action == None and '.csv' not in pth:
        request_out = requests.get(url_path, auth=auth_skytap, headers=header_api)
    elif action == 'POST':
        copy_json = json.dumps(json_data)
        print(copy_json)
        # Send the request
        request_out = requests.post(url_path, auth=auth_skytap, headers=header_api, data=copy_json)
    # Print the response status code and response content
    if request_out.status_code == 200:
        print(request_out.status_code)
        print(request_out)
        print(request_out.json())
        return request_out.json()
        


for reporttype in ['csv','json']:
    report_req = {
        "start_date": start_date,
        "end_date": end_date,
        "resource_type": "svms",
        "group_by": "raw",
        "aggregate_by": "none",
        "results_format": reporttype,
        "time_zone": "UTC",
        "notify_by_email": "True"
    }
    json.dumps(report_req)

    send_report = skytap("v2/reports.json",action="POST",json_data= report_req)
    print("Send off for report", send_report)

    i = 0
    status_report = skytap(f"reports/{send_report['id']}.json")
    while i > 3 and status_report['ready'] == False:
        i += 1
        time.sleep(15)
        status_report = skytap(f"reports/{send_report['id']}.json")
        print("Is the report ready? ", status_report['ready'], "report id ", status_report['id'])

    
    if reporttype == 'csv' and status_report['ready'] == True:
        print("inside", reporttype, "status is", status_report['ready'])
        data_report = skytap(send_report['url'])
        print("data report", data_report.text)
        data_stream = StringIO(data_report.text)
        print(data_stream)
        data = pandas.read_csv(data_stream)
        reporting_data[reporttype] = data
    if reporttype == 'json':
        reporting_data[reporttype] = status_report



print(reporting_data)

reporting_data['json']['results']['items']
reporting_data['csv']

