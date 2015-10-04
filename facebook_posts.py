import requests
import sys
import datetime
from config import TOKEN
from config import PAGE_ID
from os import getenv
LAST_POST = 0;
my_headers = {'Authorization': 'Bearer ' + TOKEN, 'Host': 'graph.facebook.com'}
count = 0
#get all the posts made by the page on Facebook
r = requests.get('https://graph.facebook.com/' + PAGE_ID + '/posts', headers=my_headers)
info = r.json()
stop = False
while 'next' in info['paging'].keys() and not stop:
  if 'data' in info.keys():
    for post in info['data']:
      if post['id'] == LAST_POST:
        stop = True
        break
      if 'story' not in post.keys() and 'message' in post.keys():
        #insert post into database 
        ''' post['message']
            post['id']
            post['created_time']'''
  info = requests.get(info['paging']['next'], headers=my_headers).json()
  count += 1
  print count
      

