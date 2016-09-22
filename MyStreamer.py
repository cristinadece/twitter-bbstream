#!/usr/bin/env python
'''
StreamBBTwitter : MyStreamer
@euthor: Cristina Muntean (cristina.muntean@isti.cnr.it)
@date: 9/22/16
-----------------------------


'''
import json
from datetime import date
from twython import TwythonStreamer

currentDate = date.today()
DUMP_DIR = 'FIX ME'
currentFile = open(DUMP_DIR + "/pisa-IF2016-tweets-" + str(currentDate) + ".json", "w")

class MyStreamer(TwythonStreamer):

    def on_success(self, data):
        global currentDate, currentFile

        if data['user']['screen_name'] != 'hesbringsmejoy':
            if self.is_current_date():
                currentFile.write(json.dumps(data)+'\n')
            else:
                currentFile.close()
                currentDate = date.today()
                currentFile = open("pisa-IF2016-tweets-" + str(currentDate) + ".json", "w")
                currentFile.write(json.dumps(data)+'\n')

            # if 'text' in data:
            #     print data['text'].encode('utf-8')
            #     print data['place']
            #     print data['coordinates']

    def on_error(self, status_code, data):
        print status_code

    @staticmethod
    def is_current_date():
        return date.today() == currentDate

