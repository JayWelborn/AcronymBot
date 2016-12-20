import urllib2
from bs4 import BeautifulSoup
from string import ascii_letters


def main():
    webopedia()
    netlingo()


# check to see if string has letters
def string_contains_alpha(s):
    ascii_set = set(ascii_letters)
    union = ascii_set & set(s)
    if len(union) == 0:
        return False
    else:
        return True


def webopedia():
    # open page for reading
    page = urllib2.urlopen('http://www.webopedia.com/quick_ref/textmessageabbreviations.asp')

    # use lxml to parse page into navigable BeautifulSoup object
    soup = BeautifulSoup(page, 'lxml')

    # find all td with valign 'top'
    acronyms = soup.find_all('td', valign='top')

    # find <p> tags within each <td>
    for index, td in enumerate(acronyms):
        acronyms[index] = td.find_all('p')

    # extract text from each paragraph
    for index, result in enumerate(acronyms):
        for paragraph in result:
            acronyms[index] = paragraph.text

    # get rid of unwanted text from webopedia
    for index, item in enumerate(acronyms):

        # gets rid of random add paragraphs
        if item:
            if len(item.split()) > 24:
                acronyms.pop(index)
                continue
            else:
                continue
        # gets rid of empty paragraphs
        else:
            acronyms.pop(index)

    # reference
    for item in acronyms:
        print(item)

    # set up empty dictionary to add acronyms
    webopedia_dict = {}

    # iterate through list putting contents into dictionary
    for index, item in enumerate(acronyms):

        # add alphabetical acronyms to dictionary
        if item.isupper():
            webopedia_dict[item] = acronyms[index + 1]

            # corner case. RT has more than one definition
            if item == 'RT':
                webopedia_dict[item] = webopedia_dict[item] + ' -OR- ' + acronyms[index + 2]
            # corner case. KOS has more than one definition, and the next item is blank
            if item == 'KOS':
                webopedia_dict[item] = webopedia_dict[item] + ' -OR- ' + acronyms[index + 3]

        # add non alphabet acronyms to dictionary
        elif not string_contains_alpha(item) and acronyms[index + 1] != 'Kill on sight':
            webopedia_dict[item] = acronyms[index + 1]

            # corner case. <3 has two definitions
            if item == '<3':
                webopedia_dict[item] = webopedia_dict[item] + ' -OR- ' + acronyms[index + 2]
            continue


    # reference
    for key in sorted(webopedia_dict):
        print(u'{}: {}'.format(key, webopedia_dict[key]))

    return webopedia_dict


def netlingo():
    # open page for reading
    page = urllib2.urlopen('http://www.netlingo.com/acronyms.php')

    # use lxml to parse page into navigable BeautifulSoup object
    soup = BeautifulSoup(page, 'lxml')

    # find all divs with class 'list_box3'
    acronym_div = soup.find_all('div', class_='list_box3')

    # get an array of acronyms, then an array of their explanation
    acronyms = acronym_div[0].find_all('a')
    acronym_list = acronym_div[0].find_all('li')

    # set up empty dictionary to add acronyms
    netlingo_dict = {}

    # iterate through arrays printing their contents for reference
    for index, item in enumerate(acronym_list):
        acronym = acronyms[index].text
        item = item.text
        item = item.replace(acronym, '')
        netlingo_dict[acronym] = item

    for key in sorted(netlingo_dict):
        print(u'\x1b[6;30;42m{}: {}\x1b[0m'.format(key, netlingo_dict[key]))

    return netlingo_dict

if __name__ == '__main__':
    main()
