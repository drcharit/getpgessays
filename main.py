import feedparser
import requests
from bs4 import BeautifulSoup
import pdfkit
import re
import os
import calendar

feed_url = "http://www.aaronsw.com/2002/feeds/pgessays.rss"
sFileSavePath = ""

feed = feedparser.parse(feed_url)

for entry in feed.entries:
    title = re.sub(r'[^\w\s]', '', entry.title)

    from glob import glob
    if glob(sFileSavePath + "*" + title + "*.*"):
        print(f'Title "{title}" exists')
    else:
        print(f'downloading essay with title{title}')
        response = requests.get(entry.link)
        soup = BeautifulSoup(response.text, 'html.parser')
        main_body = soup.find('td', attrs={'width': '435'})
        main_body_str = str(main_body)

        try:
            # Search for the full month name within the HTML content
            month = None
            year = None

            for name, number in enumerate(calendar.month_name):
                if name and number in main_body_str:
                    month = number
                    break
            year_match = re.search(r'\b(\d{4})\b', main_body_str)
            if year_match:
                year = year_match.group(1)

            if month and year:
                filename = f"{title} {month} {year}"
            elif year:
                filename = f"{title} {year}"
            else:
                raise ValueError("Month or year not found")

        except Exception as e:
            print(f"Error while processing the title {title}: {str(e)}")
            filename = title

        print(f"Saving: {filename}")

        sFilenameWithPath = sFileSavePath + filename + ".pdf"

        if os.path.isfile(sFilenameWithPath):
            print("file exists. Skipping")
        else:
            main_body_str = str(main_body)
            try:
                pdfkit.from_string(main_body_str, sFilenameWithPath)
                print(f"Saved: {filename}.pdf")
            except Exception as e:
                print(f"Error processing: {filename}. Error: {str(e)}")
#        endif
#    endif fileexists
#endfor
