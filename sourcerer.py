import praw
import urllib
import urllib2
from bs4 import BeautifulSoup
from textblob import Word

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
# remove space as a most common word
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

def get_synset(word):
    wn = Word(word)
    BEGIN = 8 
    synonyms = []

    for syn in wn.synsets:
        end = str(syn).find('.', BEGIN)
        # get synonym str from synset object
        s = str(syn)[BEGIN:end]

        if s not in synonyms:
            synonyms.append(s)

    return synonyms

def get_synsets(words):
    synsets = []

    for word in words:
        synsets.append(get_synset(word))

    return synsets

def get_cross_ref_words(synsets):
    words = []

    for synset in synsets:
        for syn in synset:
            if syn in sorted_words and syn not in words:
                words.append(syn)
    
    return words

# get list of synonyms for words in title
title_synsets = get_synsets(submission.title.split()) 
title_syn_search = "+".join(get_cross_ref_words(title_synsets))

# get list of synonyms of words in search words
user_search_synsets = get_synsets(user_search_list)
user_syn_search = "+".join(get_cross_ref_words(user_search_synsets))

    
yt_playlist = "http://www.youtube.com/watch_videos?video_ids="
yt_playlist += (get_first_link(title) + ',')
# yt_playlist += (get_first_link(title + "+" + top_5) + ',')
yt_playlist += (get_first_link(top_5) + ',')
yt_playlist += (get_first_link(user_search_list) + ',')
yt_playlist += (get_first_link(title_syn_search) + ',')
yt_playlist += get_first_link(user_syn_search)

print yt_playlist
