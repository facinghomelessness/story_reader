import requests
import datetime
from config import TOKEN
from config import PAGE_ID
my_headers = {'Authorization': 'Bearer ' + TOKEN, 'Host': 'graph.facebook.com'}
count = 0
r = requests.get('https://graph.facebook.com/' + PAGE_ID + '/feed', headers=my_headers)

r = requests.get('https://graph.facebook.com/' + PAGE_ID + '/feed', headers=my_headers)
info = r.json()
while 'next' in info['paging'].keys():
  print info
  if 'data' in info.keys():
    for post in info['data']:
      #print post['id']
      #print  post['created_time']
      if 'story' not in post.keys() and 'message' in post.keys():
        a=1
        #print post['message']
  info = requests.get(info['paging']['next'], headers=my_headers).json()
  count += 1
  print count
      


  
