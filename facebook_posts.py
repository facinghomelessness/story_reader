import pyodbc
import requests

# Local configuration settings
import config

# Read in the id of the last post we processed.
LAST_POST = 0
try:
  from status import LAST_POST
except:
  pass

#get all the posts made by the page on Facebook
my_headers = {'Authorization': 'Bearer ' + config.TOKEN, 'Host': 'graph.facebook.com'}
url = 'https://graph.facebook.com/' + config.PAGE_ID + '/posts'
r = requests.get(url, headers=my_headers)
info = r.json()

new_last_post = LAST_POST
stop = False
values_list = ''
while 'next' in info['paging'].keys() and not stop:
  if 'data' in info.keys():
    for post in info['data']:
      if post['id'] == LAST_POST:
        # Here, we just encountered a post we already saw on the last pass.
        stop = True
        break
      else:
        if new_last_post == LAST_POST:
            # Posts are delivered in reverse time order, so the most recent
            # post is first. On the next pass, we want to stop reading when
            # we encounter the first post we read this time. Here, we are at
            # the first post.
            new_last_post = post['id']
      # Posts with story are just links to external sites or say that an event
      # was created -- these are not usually informative.
      if 'story' not in post.keys() and 'message' in post.keys():
        # Clean up the time string. Format supplied by Facebook is:
        # yyyy-mm-ddThh:mm:ss+zzzz
        cleaned_time, _x, _y = post['created_time'].rpartition('+')
        cleaned_time = cleaned_time.replace('T', ' ')
        # Assemble the VALUES for this post, for the SQL INSERT.
        values = (
          post['id'],
          cleaned_time,
          post['message'],
        )
        values_list.append(values)
  info = requests.get(info['paging']['next'], headers=my_headers).json()
      
# Write to the database.
connection_string = 'DRIVER={%s};SERVER={%s.database.windows.net};DATABASE={%s};UID={%s};PWD={%s}' % (config.SQL_SERVER_DRIVER, config.SERVER_NAME, config.DATABASE_ID, config.DATABASE_USER_ID, config.DATABASE_USER_PASSWORD)
cnxn = pyodbc.connect(connection_string)
cursor = cnxn.cursor()
#cursor.execute("insert into Posts(PostID, PostDate, PostText) values ('2015-10-03 12:00:00', 'This is a test')")
cursor.executemany("insert into Posts(PostID, PostDate, PostText) values (?, ?, ?)", values_list)
cnxn.commit()

# Update the last post id.
with open("status.py", "w+") as status_file:
  status_file.write("LAST_POST = %s\n" % LAST_POST)


