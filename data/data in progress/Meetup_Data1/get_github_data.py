'''
Created on Jun 6, 2015

@author: hlamba
'''

import os
import sys
import json
import httplib2
import array


key="2a791a234d451a7d1051c13753157a"

def request(key,request_params):
    base_url='https://api.meetup.com/2/open_events?key='+str(key)
    http = httplib2.Http()
    
    url=base_url
    for key in request_params.keys():
        value=request_params[key]
        url = url+"&"+str(key)+"="+str(value)
        
    print url
    
    headers = {}
    content = http.request(url,'GET', headers=headers)
    
    #print content
    #print len(content)
    #print content[0]
    #print content[1]
    content=content[1]
    #print content
    return content


def make_request():
    request_params={}
    request_params['country']="us"
    request_params['city']="Chicago"
    request_params['state']="IL"
    request_params["category"]=34
    request_params["time"]="-1m,"
    request_params["status"]="past"
    request_params["sign"]="true"
    
    content=request(key,request_params)
    json_obj=json.loads(content)
    print len(json_obj['results'])
    return json_obj
    
def request_url(url):
    http = httplib2.Http()
    headers = {}
    content = http.request(url,'GET', headers=headers)
    content = content[1]
    return content
    
    
def make_cascading_requests(output_file):
    #first request
    json_obj=make_request()
    meta_json=json_obj['meta']
    next_req_url=meta_json['next']
    
    fw=open(output_file,"w")
    
    while(len(next_req_url)>0):
        json.dump(json_obj['results'],fw,ensure_ascii=True)
        content=request_url(next_req_url)
        json_obj=json.loads(content)
        print len(json_obj['results'])
        meta_json=json_obj['meta']
        next_req_url=meta_json['next']
        
    print "closing file"
    fw.close()
    
make_cascading_requests("MeetUp_Data.txt")


