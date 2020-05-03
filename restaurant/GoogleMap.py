"""
Create Date , 
@author: 
"""
import json
import urllib.request

def geocode(addr_list):
    addresses = [addr.replace(" ", "+") for addr in addr_list]
    api_key = "AIzaSyAWMOWfy7Sxeh4Q-NV-pSEg3wPmxCQCUFQ"
    url_base = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}"
    lat = []
    lng = []
    res = []
    for addr in addresses:
        url = url_base.format(addr, api_key)
        wp = urllib.request.urlopen(url)

        pw = wp.read()
        data = json.loads(pw)
        res.append([data["results"][0]["geometry"]["location"]['lat'],
                   data["results"][0]["geometry"]["location"]['lng']])
    return res