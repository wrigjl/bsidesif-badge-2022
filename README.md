# bsidesif-badge-2022
All the badge things

For WIFI credentials, the current code expects a secrets.py file with at least two lines for the SSID and PASSWORD variables (case sensitive)
However secrets.py is in .gitignore so you shouldn't accidentally commit your own creds back to the repo... Don't do this!

# Uploading Code

If it's the first time uploading code to the badge, uncomment the line for `tokens.json` in push.sh

sh push.sh

Comment the line for `tokens.json` and keep it commented for future pushes.

# Example secrets.py file contents:
#Modify me with values for your network...</br>
SSID = 'SSID_Value'</br>
PASSWORD = 'Password_Value'

