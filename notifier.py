#
#   --------------------------------
#      reddit-new-post-notify  
#      notifier.py
#   -------------------------------- 
#
#        Author: Jacob Causon            
#                July 2014 
#
#   Licensed under the Apache License, Version 2.0 (the "License"); 
#    you may not use this file except in compliance with the License. 
#    You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software distributed
#    under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#    CONDITIONS OF ANY KIND, either express or implied. See the License for the
#    specific language governing permissions and limitations under the License.
#
#
import urllib.request
import http.client, os
import json
import re
import time

sub = os.getenv('SUBREDDIT')       # Which sub to check
delay = int(os.getenv('UPDATE_INTERVAL'))         # How often to do check (in seconds)

# Function defining what to do when there is a new post
def on_new_post(postDataJson, post_time_utc):
    message = postDataJson['title'] + "\n" + postDataJson['url']
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": os.getenv('PUSHOVER_TOKEN'),
        "user": os.getenv('PUSHOVER_USER_KEY'),
        "message": message,
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

url = "https://www.reddit.com/r/"+sub+"/new.json?sort=new"
lastPost = 0
req = urllib.request.Request(url, headers={"User-Agent": "reddit-new-post-notifier"})
while True:
    response = urllib.request.urlopen(req)
    parsedJson = json.loads(response.read())
    latestPost = lastPost
    for post in parsedJson['data']['children']:
        timeStr = str(post['data']['created_utc'])
        timeInt = int(post['data']['created_utc'])
        title = post['data']['title']
        url = post['data']['url']
        if latestPost == 0:
            latestPost = timeInt
            print("First run! Assigning last post time to: " + timeStr)
            print("Skipping loop")
            break
        if timeInt > lastPost:
            print("Sending post " + title)
            on_new_post(post['data'], timeInt)
            if timeInt > latestPost:
                latestPost = timeInt
    if latestPost != lastPost:
        print("Setting lastPost to " + str(latestPost))
    lastPost = latestPost
    time.sleep(delay)


