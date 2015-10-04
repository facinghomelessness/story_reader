# This file holds site- and system-specific configuration information that
# should not be stored in the GitHub repository.  For each item, replace the
# string xxxxx with the correct information.

# Add the Facebook app token and page id for accessing the Facebook page.
# Facebook app token (not the secret):
TOKEN = "xxxxx"
# Page id of Facebook page to read from.  To find the page id:
# To find Page ID:  On your page, click Settings, then Page Info.
# Toward the bottom of the Page Info, look for Facebook Page ID.
PAGE_ID = "xxxxx"

# Add the name of the SQL Server driver in use on this system.  To find this
# on a Windows machine:
# Control Panel -> Administrative Tools -> Data Sources (ODBC) -> Drivers
# Some examples:
# SQL_SERVER_DRIVER = "SQL Server Native Client 11.0"
# SQL_SERVER_DRIVER = "SQL Server"
SQL_SERVER_DRIVER = "xxxxx"

# Add the connection information for the SQL Server database.
# Server name:
SQL_SERVER_NAME = "xxxxx.database.windows.net"
# Database ID:
DATABASE_ID = "xxxxx"
# The database user requires external write access to the database.  The name
# of a user with write permission typically ends in _ExternalWriter.
# Database user ID (UID):
DATABASE_USER_ID = "xxxxx"
# Database user password:
DATABASE_USER_PASSWORD = "xxxxx"