#!/usr/bin/env python
'''
StreamBBTwitter : StreamListener
@euthor: Cristina Muntean (cristina.muntean@isti.cnr.it)
@date: 9/22/16
-----------------------------

https://apps.twitter.com/app/12870923

Bounding boxes do not act as filters for other filter parameters. For example track=twitter&locations=-122.75,36.8,-121.75,37.8
would match any tweets containing the term Twitter (even non-geo tweets) OR coming from the San Francisco area.

!!!!
Each account may create only one standing connection to the public endpoints, and connecting to a public stream more
than once with the same account credentials will cause the oldest connection to be disconnected.

Clients which make excessive connection attempts (both successful and unsuccessful) run the risk of having their IP
automatically banned.


'''
import logging
import oauth2 as oauth
import time
from twython import TwythonRateLimitError
from MyStreamer import MyStreamer

PISA = '10.345376,43.67402,10.445381,43.739481'
#LUCCA = '10.385155,43.768703,10.559524,43.930716'

CONSUMER_KEY = 'FIXME'
CONSUMER_SECRET = 'FIXME'
ACCESS_TOKEN = 'FIXME'
ACCESS_TOKEN_SECRET = 'FIXME'

# Minimal time accepted between two Rate Limit Errors
TOO_SOON = 10
# Time to wait if we receive a Rate Limit Error too soon after a previous one
WAIT_SOME_MORE = 60

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def oauth_req(url, http_method="GET"):
    """
    Usage:
    # home_timeline = oauth_req('https://stream.twitter.com/1.1/statuses/filter.json?track=pitt')
    # print home_timeline

    :param url: twitter endpoint
    :param http_method: GET
    :return: content
    """

    #Setup KEYS
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(key=ACCESS_TOKEN, secret=ACCESS_TOKEN_SECRET)

    # Create the client
    client = oauth.Client(consumer, token)
    resp, content = client.request(url, method=http_method)  # i can add params: parameters=params - a dict


    return content


def log(msg, id=None):
    if id is not None:
        logger.info('%s: %s' % (id, msg))
    else:
        logger.info('%s' % msg)

def filter():
    start = time.time()

    stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET,
                        ACCESS_TOKEN, ACCESS_TOKEN_SECRET, retry_in=3600)  # retry_in - n seconds
    try:
        # FILTER
        stream.statuses.filter(track='#IF2016', locations=PISA)
    except TwythonRateLimitError as e:
        # If this error is received after only few calls (10 seconds of calls) wait just a minute
        if time.time() - start < TOO_SOON:
            log('Waiting %s seconds more for resuming download after recurrent rate limit error ...'
                % WAIT_SOME_MORE)
            time.sleep(WAIT_SOME_MORE)
        else:
            log(e, id)
            log('Waiting %s seconds for resuming download after rate limit error ...')
            time.sleep(60)


def main():
    filter()


if __name__ == '__main__':
    main()
