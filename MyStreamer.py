#!/usr/bin/env python
'''
StreamBBTwitter : MyStreamer
@euthor: Cristina Muntean (cristina.muntean@isti.cnr.it)
@date: 9/22/16
-----------------------------
 or here: http://www.kalisch.biz/2013/10/harvesting-twitter-with-python/

'''

import json
from datetime import date
from twython import TwythonStreamer

currentDate = date.today()
DUMP_DIR = '/data/tweets/rome-tweets'
currentFile = open(DUMP_DIR + "/rome-tweets-" + str(currentDate) + ".json", "w")

class MyStreamer(TwythonStreamer):

    def on_success(self, data):
        global currentDate, currentFile


        if self.is_current_date():
            currentFile.write(json.dumps(data)+'\n')
        else:
            currentFile.close()
            currentDate = date.today()
            currentFile = open(DUMP_DIR + "/rome-tweets-" + str(currentDate) + ".json", "w")
            currentFile.write(json.dumps(data)+'\n')

    def on_error(self, status_code, data):
        print status_code

    @staticmethod
    def is_current_date():
        return date.today() == currentDate

