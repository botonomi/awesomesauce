import feedparser
import re
import requests
import string
import sys
import os
import github3

link = ""
owner = os.environ['GITHUB_ACTOR']
owner = 'botonomi'


xml = open("feed.xml", "w")

feed = 'https://github.com/ripienaar/free-for-dev/commits/master.atom'
raw = feedparser.parse(feed)

xml.write('<?xml version="1.0" encoding="UTF-8" ?>')
xml.write("\n")
xml.write('<rss version="2.0">')
xml.write('<channel>\n<title>New Free-For-Dev</title>\n<description>New Free Resources</description>\n<link>')
xml.write(link)
xml.write("</link>\n")

for entry in raw.entries:
    if not re.search('Merge\Wpull\Wrequest', entry.title):
        xml.write("<item>\n\t<title>")
        xml.write(entry.title)
        xml.write("</title>\n\t<link>")
        xml.write(entry.link)
        xml.write('</link><description><![CDATA[')

        patch = requests.get(entry.link + '.patch')

        for line in patch.text.split("\n"):
            try:
                lead = list(line)[0]

                if list(line)[0] == "+" and list(line)[1] != "+":
                    line = line[1:]

                    w = re.search("\[(.*)\]\((.*)\)", line)
                    name = w.group(1)
                    url = w.group(2)

                    desclink = '<a href="' + name + '">' + url + '</a>'
                    desctext = ' '.join(line.split()[3:])
                    #print(desc)

                    #xml.write(line)
                    xml.write(desclink)
                    xml.write(" - ")
                    xml.write(desctext)
                    xml.write("<br>\n")

            except Exception:
                continue

        xml.write(' ]]></description>')
        xml.write("\n</item>\n")

xml.write("\n</channel>\n</rss>\n")

xml.close()
