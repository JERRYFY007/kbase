# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:ai1.py
# @time:2017/7/3 0003 10:50
import requests

parameters = {"input": "天气"}
resp = requests.get('http://39.108.135.114:8001/simpleMobile/getResponce.sc?', params=parameters)
# Set up the parameters we want to pass to the API.
# This is the latitude and longitude of New York City.
parameters = {"lat": 40.71, "lon": -74}

# Make a get request with the parameters.
response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)

# Print the content of the response (the data the server returned)
print(response.content)

# This gets the same data as the command above
response = requests.get("http://api.open-notify.org/iss-pass.json?lat=40.71&lon=-74")
print(response.content)
