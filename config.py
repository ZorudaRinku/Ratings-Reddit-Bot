username = ""
password = ""
client_id = ""
client_secret = ""

#Subreddit
subreddit = ""

#Number of posts to scan at a time (Suggested = 15)
scanAmount = 15

#How long it should wait between each scan in seconds (More posts should make this number way less, although, faster pc = handle more posts and scans than a slower one) (Suggested = 30)
scanFrequency = 30

#The threshold to delete posts at (Suggested = -4) (Testing = 0)
threshold = -4

#The threshold to delete the "I am a bot" comment to remove clutter (set to 0 if you dont want it to delete) (Suggested = 10) (Testing = 2)
thresholdSelfDelete = 10

#The message to comment on posts. If you dont want to to post this each time make the string empty (but leave the variable there)
templateMessage = "Upvote this comment if you feel this submission is characteristic of our subreddit. Downvote this if you feel that it is not. If this comment's score falls below a certain number, this submission will be automatically removed."

#The message to send once their comment gets deleted
templateMailSubject = "Post was removed"
template_mail_body = "Your [post]({url}) at /r/" + subreddit + ", was deleted because it reached below a threshold. If you think this was a mistake message us [here](https://www.reddit.com/message/compose?to=%2Fr%2F" + subreddit + "&subject=&message=)"