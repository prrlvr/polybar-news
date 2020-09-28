#!/usr/bin/env python

import nntplib

url = 'news.epita.fr'
groups = ["assistants.news"]

def connect(url):
    connection = nntplib.NNTP(url)
    return connection

def main():
    connection = connect(url)
    news = []
    for grp in groups:
        _, _, first, last, name = connection.group(grp)
        resp, overview = connection.over((last-9, last))
        for id, over in overview:
            subject = nntplib.decode_header(over['subject'])
            if not 'NETIQUETTE' in subject:
                news.append(subject)
    print(news[-1])
main()
