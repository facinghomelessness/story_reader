import os
import os.path
import pyodbc
import requests

# Make sure the cwd is the location of this script -- want to store status.py
# in the same directory.
script_path = os.path.realpath(__file__)
dirname = os.path.dirname(script_path)
os.chdir(dirname)

# Local configuration settings
import config

# Read in the id of the last post we processed.
LAST_POST = 0
try:
  from status import LAST_POST
except:
  pass

# Get all the posts made by the page on Facebook.
my_headers = {'Authorization': 'Bearer ' + config.TOKEN, 'Host': 'graph.facebook.com'}
url = 'https://graph.facebook.com/' + config.PAGE_ID + '/posts'
r = requests.get(url, headers=my_headers)
info = r.json()

new_last_post = LAST_POST
stop = False
num_posts = 0
values_list = []
while not stop:
  if 'data' in info:
    for post in info['data']:
      # The id has the page number, an underscore, and the post number.
      # Remove the page number.
      _x, _y, cleaned_id = post['id'].rpartition('_')
      cleaned_id = long(cleaned_id)
      if cleaned_id == LAST_POST:
        # Here, we just encountered a post we already saw on the last pass.
        stop = True
        break
      else:
        if new_last_post == LAST_POST:
          # Posts are delivered in reverse time order, so the most recent
          # post is first. On the next pass, we want to stop reading when
          # we encounter the first post we read this time. Here, we are at
          # the first post.
          new_last_post = cleaned_id
      # Posts with story are just links to external sites or say that an event
      # was created -- these are not usually informative.
      if 'story' not in post and 'message' in post:
        # Clean up the time string. Format supplied by Facebook is:
        # yyyy-mm-ddThh:mm:ss+zzzz
        cleaned_time, _x, _y = post['created_time'].rpartition('+')
        cleaned_time = cleaned_time.replace('T', ' ')
        # Assemble the VALUES for this post, for the SQL INSERT.
        values = (
          cleaned_id,
          cleaned_time,
          post['message'],
        )
        values_list.append(values)
        num_posts = num_posts + 1
  if not stop and 'paging' in info and 'next' in info['paging']:
    info = requests.get(info['paging']['next'], headers=my_headers).json()
  else:
    break

# Is there anything to write?
if len(values_list) > 0:
  # Write to the database.
  connection_string = 'DRIVER={%s};SERVER={%s};DATABASE={%s};UID={%s};PWD={%s}' % (config.SQL_SERVER_DRIVER, config.SERVER_NAME, config.DATABASE_ID, config.DATABASE_USER_ID, config.DATABASE_USER_PASSWORD)
  cnxn = pyodbc.connect(connection_string)
  cursor = cnxn.cursor()
  # Use either the real or staging table name.
  cursor.executemany("insert into %s(PostID, PostDate, PostText) values (?, ?, ?)" % config.DATABASE_POSTS_TABLE, values_list)
  cnxn.commit()

# Update the last post id.  Do this even if we did not find any posts to write,
# as we may have seen some posts with only links, that we did not upload.
status_file = open("status.py", "w")
status_file.truncate()
status_file.write("LAST_POST = %s\n" % new_last_post)
status_file.close()
