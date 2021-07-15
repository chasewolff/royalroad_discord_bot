# Version 2 of the RoyalRoad Webhook bot.
# Author: chasewolff
# Interacts with RSS feeds on RoyalRoad to determine updates.
# Saves the latest version chapter to a file so starting the bot is quick and easy.

from webhook import webhook
import feedparser
import time

# Set how often the bot refreshes the page to check for updates.
# Keep in mind, the RSS feed updates every 15 minutes, so having the bot check
# more often than that is kind of pointless.
refreshrate = 900

# This is a dictionary of role ID's. Follow steps in README to get them.
# The bot uses these ID's to ping users because it can't just @RoleName.

roles = {
    1 : "<@&##################>"
    }

# Cover image links. This is what the bot will use to change its discord profile
# photo. It changes it's look and name for each book.
# The ##### is the fiction ID, and the "story-title-here" is the fiction name.
covers = {
    1 : "https://www.royalroadcdn.com/public/covers-full/#####-story-title-here.jpg",
}
# Story titles. It's what the bot uses for its name when it posts.
titles = {
    1 : "Story Title Here"
}
# The actual links to the syndication pages (the RSS feed).
# The ##### is the fiction ID. You can copy-paste it from the fiction page.
links = {
    1 : "https://www.royalroad.com/fiction/syndication/#####"
}
# Latest Chapter Files. Its where the bot stores the latest chapter it's seen.
# You can set this manually by going to the txt file and changing it to whatever
# the last entry on the RSS feed is.
# I've numbered them, but you can name them whatever you want.
lastChaps = {
    1 : "001.txt"
}

# Called to create txt files. Only call it on the first run to make the notepads.
def makeFiles():
    i = 1
    for story in titles:
        f = open(lastChaps[i], 'w')
        f.close()
        i+=1


# Fetch the RSS page of a specific story.
def readRSS(storyLink):
    chapter_list = []
    try:
        d = feedparser.parse(storyLink)
        chapters = d['entries']

        for a in chapters:
            title = a['title']
            link = a['link']
            published = a['published']

            chapter = {
                'title' : title,
                'link' : link
            }
            chapter_list.append(chapter)

        return chapter_list
    except Exception as e:
        print("Error. See exception.")
        print(e)

# Save the latest chapter to a text file.
def saveRecent(storyVal, chap_list):
    with open(lastChaps[storyVal], 'w') as f:
        f.write(chap_list[0]['title'])
    f.close()

# This formats the webhook with required information and calls the objects deployHook function.
def deployWebhook(storyVal, chapter):
    hook = webhook(chapter['title'], titles[storyVal], chapter['link'], roles[storyVal], covers[storyVal])
    hook.deployHook()

# Compare the latest chapter to the text file.
def checkForUpdate(storyVal):
    f = open(lastChaps[storyVal],'r')
    chap_list = readRSS(links[i])
    chapter = chap_list[0]
    if chapter['title'] != f.read():
        f.close()
        print("******************************************")
        print("New update for " + titles[storyVal] + "!")
        print("Link: " + chapter['link'])
        print("******************************************\n")
        saveRecent(storyVal, chap_list)
        deployWebhook(storyVal, chapter)
    else:
        f.close()
        print("No new updates for " + titles[storyVal])

# Main Script
while True:
    # Bot will log to the console the current time so you can walk away
    # and when you come back, you'll know it's been working, or when it
    # saw an update.
    t = time.strftime("%H:%M:%S", time.localtime())
    print("\n" + t + " Checking for updates...")
    # The below loop checks each fiction for updates individually.
    i = 1
    for story in titles:
        checkForUpdate(i)
        i+=1
    time.sleep(refreshrate)
