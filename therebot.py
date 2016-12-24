import praw
from Scraper import webopedia, netlingo
from io import open


# create instance of Reddit for future actions
reddit = praw.Reddit(client_id='qM505htuaT5pCw',
                     client_secret='i46Ru1rEOdn__MdK3jAkJTQ7u7w',
                     user_agent='Test Script by u/there_there_theramin',
                     username='there_there_theramin',
                     password='qwerQWER1234!@#$')

# get acronym dictionary from netlingo.com
netlingo = netlingo()
# get acronym dictionary from webopedia.com
webopedia = webopedia()


def main():

    # read log file to load comments already replied to
    with open('comments.txt', 'r') as log:
        comment_history = log.read().split('\n')

    # create instance of subreddit for iterating
    subreddit = reddit.subreddit('all')

    # gets iterable list of submissions in subreddit
    for submission in subreddit.hot():

        # prints title of each submission
        print('\n\t' + submission.title)

        # turns MoreComments objects into Comments (see PRAW 4.0 docs)
        submission.comments.replace_more(limit=0)

        # turns submission comments into iterable
        comments = submission.comments.list()

        for comment in comments:
            # searches comments in submission for acronyms
            acronyms = detect_acronyms(comment, comment_history)
            if acronyms:
                reply(acronyms, comment)

    # open file to log comments replied to
    with open('comments.txt', 'w') as log:
        for item in comment_history:
            log.write(item + '\n')

    print(len(comment_history))
    print('finished')


# parse comments looking for instances of internet/chat acronyms
def detect_acronyms(comment, comment_history):

    acronyms = []

    if comment.id in comment_history:
        print(u'\x1b[1;30mComment Already Seen\n\n{}\n\nComment ID ={} \x1b[0m'.format(comment.body, comment.id))
        return acronyms

    elif comment.author == 'there_there_theramin':
        print(u'\x1b[1;30;42mDon\'t reply to yourself\x1b[0m')
        with open('self_comment.txt', 'w') as self:
            self.write(u'FOUND ONE!\n')
        return acronyms

    else:
        # look for acronyms in dictionary
        for word in comment.body.split():
            if word in netlingo:

                # to ensure each acronym is only used once per reply
                if word not in acronyms:
                    acronyms.append(word)
                    # adds comment to log so I don't reply to the same comment again
                    comment_history.append(comment.id)

            if word in webopedia:

                # to ensure each acronym is only used once per reply
                if word not in acronyms:
                    acronyms.append(word)
                    # adds comment to log so I don't reply to the same comment again
                    comment_history.append(comment.id)

        # return list of all acronyms detected
        return acronyms


def reply(acronyms, comment):

    # bot text opener
    bot_text = u"""
Hello! I am a bot made to detect and explain common
chat/internet acronyms/slang.I have detected one or
more such items in this comment. If this seems incorrect,
please send me a PM to address the mistake.\n\n"""

    for acronym in acronyms:
        # adds definition from netlingo to bot text
        if acronym in netlingo:
            bot_text = u'{} The following definition comes from Netlingo.com.\n {}: {}\n'.format(bot_text,
                                                                                                 acronym,
                                                                                                 netlingo[acronym])
            with open('log.txt', 'a') as log:
                log.write(u'{}: {}\n\n-------------------------\n\n'.format(acronym, netlingo[acronym]))
        # adds definition from webopedia to bot text
        if acronym in webopedia:
            bot_text = u'{} The following definition comes from Webopedia.com.\n {}: {}\n'.format(bot_text,
                                                                                                  acronym,
                                                                                                  webopedia[acronym])
            with open('log.txt', 'a') as log:
                log.write(u'{}: {}\n\n-------------------------\n\n'.format(acronym, webopedia[acronym]))

    print(u'\n{}\n{}'.format(comment.author, comment.body))
    print('\n\n')
    print(u'\x1b[6;30;42m {} \x1b[0m'.format(bot_text))
    # comment.reply(bot_text)


# execute main
if __name__ == '__main__':
    main()
