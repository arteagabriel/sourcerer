import praw
import urllib
import urllib2
from bs4 import BeautifulSoup

# must have a user agent string
r = praw.Reddit("user agent for sourcerer project")

# assume link is valid for now
link = raw_input("Enter Reddit URL: ")
submission = r.get_submission(url=link)

# get description from user to search in YouTube
user_search = raw_input("Enter GIF description: ")
user_search_list = "+".join(user_search.split())

# gets comments in an unordered list 
# submission.replace_more_comments()
comments = praw.helpers.flatten_tree(submission.comments)

# program is currently ignoring MoreComments comments for 
# speed purposes

# get users search words
for comment in comments:
    if isinstance(comment, praw.objects.MoreComments):
        comments.remove(comment)

# initialize empty dictionary (key/value)
word_count = {} 
for comment in comments:
    # get words in a comment
    if not isinstance(comment, praw.objects.MoreComments):
        words = comment.body.split()

    for word in words:
        word = word.lower()
        # strip non alphanumeric characters
        word = ''.join(c for c in word if word.isalnum())
        # if word is in word count increment it else add it to list
        word_count[word] = word_count[word] + 1 if word in word_count else 1

# create list with most used words at the beginning
sorted_words = sorted(word_count, word_count.get)
sorted_words.remove(sorted_words[0])

# print words in list for testing purposes
# for word in sorted_words:
#     print word

# put top 10 most common words in a list
# top_10 = "+".join(sorted_words[:10])

# put top 5 most common words in a list
top_5 = "+".join(sorted_words[:5])

# put title words into a list
title = "+".join(submission.title.split())

def get_first_link(search_words):
    yt_search = "https://www.youtube.com/results?search_query="
    response = urllib2.urlopen(yt_search + search_words)
    soup = BeautifulSoup(response.read())
    url = soup.find(attrs={'class':'yt-uix-tile-link'})['href']

    return url[url.find('=') + 1:]

yt_playlist = "http://www.youtube.com/watch_videos?video_ids="
yt_playlist += (get_first_link(title) + ',')
# yt_playlist += (get_first_link(title + "+" + top_5) + ',')
yt_playlist += (get_first_link(top_5) + ',')
yt_playlist += get_first_link(user_search_list)

print yt_playlist
