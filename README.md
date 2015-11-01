# story_reader

Read Facing Homelessness posts from Facebook and store them in the database.

If needed, install Python 2.7, requests, pyodbc, and the SQL Server driver
appropriate for the operating system this will run on.  The driver is known
to be available for Windows and believed to be available for Linux, both
from Microsoft.  The hunt is still on for driver for Mac OS X.  The driver
must be at least v 11.0.

Clone this repository or copy the files into a directory:
https://github.com/facinghomelessness/story_reader

Copy the file config_template.py to config.py and fill in the required values
for the system this will run on, for the Facebook page, and for the SQL Server
database.

If this has already been running elsewhere, obtain status.py from that site.
This contains the id of the most recent post uploaded to the database -- this
is used to avoid uploading duplicate posts.

Then run facebook_posts.py under Python 2.7.

For preference, this would run as a Scheduler job on Azure.  If not possible,
then it could be run from a system that supports periodic processes, or even
run by hand at intervals from any available system.