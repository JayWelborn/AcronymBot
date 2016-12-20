import praw
# import time imported so I can sleep in between calls to the API once this thing goes live
from itertools import islice
from Scraper import webopedia, netlingo
from io import open

# create instance of Reddit for future actions
reddit = praw.Reddit(client_id='REDACTED',
                     client_secret='REDACTED',
                     user_agent='REDACTED',
                     username='REDACTED',
                     password='REDACTED')

# create instance of subreddit for iterating
subreddit = reddit.subreddit('askreddit')

# get acronym dictionary from netlingo.com
netlingo_dict = netlingo()
# get acronym dictionary from webopedia.com
webopedia_dict = webopedia()


def main():

    # gets iterable list of submissions in subreddit
    for submission in islice(subreddit.stream.submissions(), 0, 100):
        # prints title of each submission
        print('\n\t\t' + submission.title)
        # parses comments in submission for acronyms
        parse_comments(submission)

    print('finished')


# parse comments looking for instances of internet/chat acronyms
def parse_comments(submission):

    # read log file to load comments already replied to
    with open('comments.txt', 'r') as log:
        comment_history = log.read().splitlines()

    # open file to log comments replied to
    comment_log = open('comments.txt', 'a')

    # iterate over comments in submission
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():

        bot_text = u"""
Hello! I am a bot made to detect and explain common chat/internet acronyms.
I have detected one or more acronyms in this comment. If this seems incorrect,
please send me a PM to address the mistake.\n\n
"""

        start_len = len(bot_text)

        # look for acronyms in dictionary
        for word in comment.body.split():
            for key in netlingo_dict:
                if key == word:
                    comment_history.append(comment.id)
                    comment_log.write(comment.id + '\n')
                    bot_text = u'{} The following definition comes from Netlingo.com.\n {}: {}\n'.format(bot_text,
                                                                                                         key,
                                                                                                         netlingo_dict[
                                                                                                            key])
                    # print(u'\n{}\x1b[6;30;42m\nNetlingo:\n\t{}: {}\x1b[0m'.format(comment.body, key, netlingo_dict[key]))
            for key in webopedia_dict:
                if key == word:
                    comment_history.append(comment.id)
                    comment_log.write(comment.id + '\n')
                    bot_text = u'{} The following definition comes from Webopedia.com.\n {}: {}\n'.format(bot_text,
                                                                                                          key,
                                                                                                          webopedia_dict[
                                                                                                            key])
        if len(bot_text) > start_len:
            print(comment.body)
            print(u'\x1b[6;30;42m' + bot_text + u'\x1b[0m')
            print('comment history =')
            print(comment_history)
    # close file
    comment_log.close()


# execute main
if __name__ == '__main__':
    main()
