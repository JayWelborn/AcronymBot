import praw
# import time imported so I can sleep in between calls to the API once this thing goes live
from itertools import islice
from Scraper import webopedia, netlingo
from io import open

# create instance of Reddit for future actions
reddit = praw.Reddit(client_id='[REDACTED}',
                     client_secret='[REDACTED}',
                     user_agent='Test Script by u/there_there_theramin',
                     username='there_there_theramin',
                     password='[REDACTED}')

# create instance of subreddit for iterating
subreddit = reddit.subreddit('learnprogramming')

# get acronym dictionary from netlingo.com
netlingo_dict = netlingo()
# get acronym dictionary from webopedia.com
webopedia_dict = webopedia()


def main():

    # read log file to load comments already replied to
    with open('comments.txt', 'r') as log:
        comment_history = log.read().splitlines()

    # gets iterable list of submissions in subreddit
    for submission in islice(subreddit.stream.submissions(), 0, 100):
        # prints title of each submission
        print('\n\t\t' + submission.title)
        # parses comments in submission for acronyms
        parse_comments(submission, comment_history)

    # open file to log comments replied to
    with open('comments.txt', 'w') as log:
        for item in comment_history:
            log.write(item + '\n')

    print('finished')


# parse comments looking for instances of internet/chat acronyms
def parse_comments(submission, comment_history):

    # iterate over comments in submission
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():

        words = []

        if comment.id in comment_history:
            print(u'\x1b[6;30;42mComment Already Seen\n\n{}\n\nComment ID ={} \x1b[0m'.format(comment.body, comment.id))
            continue

        else:
            # look for acronyms in dictionary
            for word in comment.body.split():
                for key in netlingo_dict:
                    if key == word:
                        comment_history.append(comment.id)
                        if word not in words:
                            words.append(word)

                for key in webopedia_dict:
                    if key == word:
                        comment_history.append(comment.id)
                        if word not in words:
                            words.append(word)

        if len(words) >= 1:
            reply(words, comment)


def reply(words, comment):

    # bot text opener
    bot_text = u"""
Hello! I am a bot made to detect and explain common chat/internet acronyms.
I have detected one or more acronyms in this comment. If this seems incorrect,
please send me a PM to address the mistake.\n\n"""

    for word in words:
        if word in netlingo_dict:
            bot_text = u'{} The following definition comes from Netlingo.com.\n {}: {}\n'.format(bot_text,
                                                                                                 word,
                                                                                                 netlingo_dict[word])
        if word in webopedia_dict:
            bot_text = u'{} The following definition comes from Webopedia.com.\n {}: {}\n'.format(bot_text,
                                                                                                  word,
                                                                                                  webopedia_dict[word])

    print(comment.body)
    print('\n\n')
    print(u'\x1b[6;30;42m {} \x1b[0m'.format(bot_text))


# execute main
if __name__ == '__main__':
    main()
