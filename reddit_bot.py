import praw
import config
import time
import os

# Made by reddit user /u/Stronger1088
# Following this tutorial https://youtu.be/krTUf7BpTc0
# This is my first bot so I hope its good enough! I tried to rule out all of the bugs possible but there might still be some. Feel free to message me! Ty!


def authentication():
	print ("Authenticating...")
	reddit = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = "Stronger1088's ratings bot for a /r/requestABot user.")
	print ("Authenticated as {}".format(reddit.user.me()))
	time.sleep(2)
	return reddit


def run_bot(reddit, posts_replied_to, exclude_comments, safe_posts):
	time.sleep(1)
	print ("Scanning posts\n==============")
	me = reddit.user.me()
	for contributor in reddit.subreddit(config.subreddit).contributor():
		if contributor not in contributors:
			print ("Found new approved submitter, {}. Adding to list.".format(contributor))
			contributors.append(contributor)
			with open ("contributors.txt", "a") as s:
				s.write(str(contributor) + "\n")
	for post in reddit.subreddit(config.subreddit).new(limit=config.scanAmount):
		if post.id not in list(posts_replied_to) and config.templateMessage and not None and post.author not in contributors:
			print ("Commenting on: \"" + post.title + "\" \"" + post.id + "\" by: \"" + post.author.name + "\"\n")
			post.reply(config.templateMessage).mod.distinguish(sticky=True)
			posts_replied_to.append(post.id)
			with open ("posts_replied_to.txt", "a") as f:
				f.write(post.id + "\n")

	for comment in me.comments.new(limit=config.scanAmount + 10):
		if comment.banned_by is not None:
			print (comment.banned_by + " removed my comment on post \"" + comment.submission.title + "\". Adding to whitelist.")
			comment.delete()
		elif comment.id not in list(safe_posts) and comment.id not in list(exclude_comments) and comment.score <= config.threshold:
			print ("Post \"" + comment.submission.title + "\" reached delete threshold. Deleting...")
			exclude_comments.append(comment.id)
			with open ("exclude_comments.txt", "a") as s:
				s.write(comment.id + "\n")
			mail_body = config.template_mail_body.format(url=comment.submission.url)
			comment.submission.author.message(config.templateMailSubject, mail_body)
			comment.submission.mod.remove()
			comment.delete()
		elif comment.score >= config.thresholdSelfDelete and config.thresholdSelfDelete != 0 and comment.submission.id not in list(safe_posts):
			print ("Post \"" + comment.submission.title + "\" reached SAFE threshold. Deleting bot comment...")
			comment.delete()
			safe_posts.append(comment.submission.id)
			with open ("safe_posts.txt", "a") as s:
				s.write(comment.submission.id + "\n")
		elif comment.id not in list(exclude_comments):
				print ( "\"" + comment.submission.title + "\" - " + str(comment.score))


	print ("==============\n\nSleeping for " + str(config.scanFrequency) + " seconds...\n")
	time.sleep(config.scanFrequency)

def get_saved_posts(): #Posts that the bot has already commented on and doesnt need to comment on again. This will be a very populated file as it doesnt delete anything just for the sake of not spamming posts
	if not os.path.isfile("posts_replied_to.txt"): #Only thing that uses os so that you dont have to create the file.
		posts_replied_to = []
	else:
		with open("posts_replied_to.txt", "r") as f:
			posts_replied_to = f.read()
			posts_replied_to = posts_replied_to.split("\n")
			posts_replied_to = filter(None, posts_replied_to)

	return posts_replied_to


def exclude_comments(): #This is for posts that have already been removed. Called comments because we dont want the bot watching its own comments if its already been deleted.
	if not os.path.isfile("exclude_comments.txt"): #Only thing that uses os so that you dont have to create the file.
		exclude_comments = []
	else:
		with open("exclude_comments.txt", "r") as f:
			exclude_comments = f.read()
			exclude_comments = exclude_comments.split("\n")
			exclude_comments = filter(None, exclude_comments)

	return exclude_comments	


def safe_posts(): #This is for post that have been "accepted" by the subreddit. refer to "thresholdSelfDelete" in config.py
	if not os.path.isfile("safe_posts.txt"): #Only thing that uses os so that you dont have to create the file.
		safe_posts = []
	else:
		with open("safe_posts.txt", "r") as f:
			safe_posts = f.read()
			safe_posts = safe_posts.split("\n")
			safe_posts = filter(None, safe_posts)

	return safe_posts	

def contributors(): 
	if not os.path.isfile("contributors.txt"): 
		contributors = []
	else:
		with open("contributors.txt", "r") as f:
			contributors = f.read()
			contributors = contributors.split("\n")
			contributors = filter(None, contributors)

	return contributors	


#Boot Info

reddit = authentication()
safe_posts = list(safe_posts())
print ("Safe Posts: " + str(safe_posts))
exclude_comments = list(exclude_comments())
print ("Excluded Comments: " + str(exclude_comments))
posts_replied_to = list(get_saved_posts())
print ("Commented Posts: " + str(posts_replied_to) + "\n")
contributors = list(contributors())

while True:
	run_bot(reddit, posts_replied_to, exclude_comments, safe_posts)