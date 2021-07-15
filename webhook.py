# Version 2 of the RoyalRoad Webhook bot.
# Author: chasewolff
# Interacts with Discord to publish alerts about new chapters.

from discord_webhook import DiscordWebhook
# Init vars
# If you ever see one of these, you did something wrong.
releasedTitle = "Chapter Name Error"
storyTitle = "Story Title Error"
chapterLink = "Chapter Link Error"
roleID = "Role ID Error"
# You can get the webhook url from discord, if you just copy it from the
# Integrations page.
hookURL = "YOUR WEBHOOK URL HERE"
# If you ever see the coverLink image, your bot is failing to find one of
# the fictions' images.
coverLink = "Default Image Here"

class webhook:
    # Constructor
    def __init__(self, releasedTitle, storyTitle, chapterLink, roleID, coverLink):
        self.releasedTitle = releasedTitle
        self.storyTitle = storyTitle
        self.chapterLink = chapterLink
        self.roleID = roleID
        self.coverLink = coverLink

    def makeHook(self):
        # Configure message content
        msg = self.roleID + "\n**" + self.releasedTitle + "** has been released!\n" + self.chapterLink
        #msg = "All Role " + "Placeholder Role" + "\n**" + self.releasedTitle + "** has been released!\n" + self.chapterLink
        hook = DiscordWebhook(url=hookURL, username=self.storyTitle, content=msg, avatar_url=self.coverLink)
        return hook

    # Deploy the webhook.
    def deployHook(self):
        hook = self.makeHook()
        response = hook.execute()
