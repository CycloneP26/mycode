#! /usr/bin/env python3

import os
import requests

def main():
        print(os.listdir("/data/feedback"))
        reviews = os.listdir("/data/feedback")
        RevDict = {}
        i = 0
        for review in reviews:
                with open("/data/feedback/" + review) as rev:
#                       print(rev.readlines())
                        LinesList = rev.readlines()
                        print(LinesList[0])
                        RevDict["title"] = LinesList[0]
                        RevDict["name"] = LinesList[1]
                        RevDict["date"] = LinesList[2]
                        RevDict["review"] = LinesList[3]
                        response = requests.post("http://34.68.254.168/feedback")
                        print(response.status_code)

main()


                        response = requests.post("http://34.123.145.74/feedback", data = p)
({}).format(LinesList[0])
