#!/usr/bin/env python
# coding=utf-8
# (c) PHZ Full Stack Oy 
# author: lennart.takanen@phz.fi

from datetime import datetime
import requests
from operator import itemgetter
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import urllib
import json
import csv

PORT_NUMBER = 8888
TOKEN = "PLACE YOUR TOKEN HERE"

headers = {"Accept": "application/json", "STTAuthorization":
           TOKEN, "Content-Type": "application/json"}
url = 'http://www.sports-tracker.com/apiserver/v1/user/feed/combined/?limit=1000'

response = requests.get(url, headers=headers)
response_json = json.loads(response.content)
data = response_json["payload"]

trainee = []


pts = 0
sport_person = ""

dump = []
for entry in data:
    if not 'username' in entry.keys():
        continue
    ts = int(entry["startTime"]) / 1000
    tsd = int(entry["totalTime"]) / 60
    time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    time2 = datetime.utcfromtimestamp(
        ts + (tsd * 60)).strftime('%Y-%m-%d %H:%M:%S')
    if sport_person != entry["username"]:
        pts = 0

    sport_person = entry["username"]
    full_name = entry["fullname"]

    if ts-pts < 15*60:
        continue
    if tsd > 29:
        temp = {}
        temp["starttime"] = time
        temp["endtime"] = time2
        temp["duration"] = tsd
        temp["account"] = sport_person
        temp["fullname"] = full_name
        dump.append(temp)
    pts = ts

datax = json.dumps(dump, indent=2, encoding="UTF-8")

def RetrievePersonActivity(year, month, person):
    persons={}
    if month < 10:
        month = "0" + str(month)
    year_month = str(year) + "-" + month
    print year_month
    for entry in dump: 
        if year_month in entry["starttime"]:
            if entry["fullname"] not in persons:
                temp = {}
                temp["account"] = entry["account"]
                temp["activitycount"] = 1 
                temp["fullname"] = entry["fullname"]
                persons[entry["fullname"]]=temp
            else:
                persons[entry["fullname"]]["activitycount"] += 1
    if person in persons:
        return persons[person]
    else: 
        return persons


# the browser
class myHandler(BaseHTTPRequestHandler):

        # Handler for the GET requests
    def do_GET(self):
        url_params = urlparse.urlparse(self.path)
        url_params = urlparse.parse_qsl(url_params.query)
        params_dict = {key:value for key,value in url_params}
        year = params_dict['year']
        try: 
            csvp = params_dict['csvp']
        except: 
            csvp = False
        try: 
            name = params_dict['name']
        except: 
            name = ""
        month = params_dict['month']
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # Send the html message
        if csvp:
            json_feed = csv.writer(RetrievePersonActivity(year, month, name))
        else:
            json_feed = RetrievePersonActivity(year, month, name)
            r = json.dumps(json_feed)
            self.wfile.write(r)
        return


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ', PORT_NUMBER

    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
