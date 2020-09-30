#!/usr/bin/env python

import nntplib
import sys

url = 'news.epita.fr'
groups = ["assistants.news", "assistants.piscine", "announcement.ing1"]

def connect(url):
    connection = nntplib.NNTP(url)
    return connection

def get_news(connection):
    news = []
    for grp in groups:
        group_news = []
        _, _, first, last, name = connection.group(grp)
        resp, overview = connection.over((last-9, last))
        for id, over in overview:
            subject = nntplib.decode_header(over['subject'])
            if not 'NETIQUETTE' in subject:
                # remove response about the netiquette
                group_news.append((id, subject))
        news.append(group_news)
    return news

def rofi_format(news):
    s = "\0prompt\x1ftest\n"
    for i in range(len(news)):
        # s += "\0urgent\x1f<b>{}</b>\n".format(groups[i])
        for n, header in news[i]:
            #s += "\0({})\x1f{}\x1f<it>{}</it>\n".format(id, header, groups[i])
            s += "{}\n".format(header)
    #print(s, file=sys.stderr)
    return s

def main(args):
    #print(args, file=sys.stderr)
    connection = connect(url)
    news = get_news(connection)
    if len(args) == 1:
        # rofi mode
        print(rofi_format(news))
    if len(args) > 1 and args[1] in 'polybar':
        # what's printed on polybar
        print(news[0][-1][1])
    else:
        #rofi action
        return 0
    return 0

main(sys.argv)
