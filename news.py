#!/usr/bin/env python

import nntplib
import sys
import subprocess

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
                group_news.insert(0, (id, subject))
        news.append((grp, group_news))
    return news

def rofi_format(news):
    s = ""
    for name, grp in news:
        #s += "\0urgent\x1f<b>{}</b>\n".format(groups[i])
        for n, header in grp:
            s += "({}-{})\t{}\n".format(n, name[name.find('.')+1:]
                    , header)
    return s

def parse_line(line):
    t = line.find('\t')
    header = line[t+1:]
    line = (line[:t]).split('-')
    n = line[0][1:]
    group = line[1][:-1]
    return (n, group, header)

def open_news(line, news, connection, width):
    (n, group, header) = parse_line(line)
    for grp in groups:
        if group in grp:
            group = grp
            break
    connection.group(group)
    body = connection.body(n)[1][2]
    print(format_text([e.decode() for e in body], width))
    #subprocess.call(['alacritty', '-e',
    #    "echo \"**{}\n\n{}\" | less".format(header, body)])

def format_text(t, width):
    s = ""
    # -1 to include the \n
    width -= 1
    for line in t:
        if line == '':
            s += '\n \n'
        elif len(line) > width:
            s += line[:width] + '-\n'
            s += line[width:]
        else:
            s += line
        s += '\n'
    return s

def main(args):
    connection = connect(url)
    # news = [(grpName, [(msgNbr, header))]]
    news = get_news(connection)
    if len(args) > 1 and args[1] in 'polybar':
        # what's printed on polybar
        print(news[0][1][0][1])
    elif len(args) == 2:
        # rofi mode
        print(rofi_format(news))
    elif len(args) == 3:
        #when an entry is selectionned in rofi
        open_news(args[2], news, connection, int(args[1]))
    return 0

main(sys.argv)
