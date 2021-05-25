import requests
from bs4 import BeautifulSoup as BS
#from browser_file import *
#https://us-cert.cisa.gov/ncas/current-activity.xml
def get_rss_feed(stri):
    alert_list = []
    try:
        r = requests.get(stri)
        soup = BS(r.content, features = 'xml')
        alerts = soup.findAll('item')

        for a in alerts:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('pubDate').text
            description = a.find('description').text
            description = description.replace("&lt;", "<")
            description = description.replace("&gt;",">")

            alt = {
                'title': title,
                'link': link,
                'published':published,
                'description': description
            }
            alert_list.append(alt)
        #print("Job success")
        #message = "<html> <br>"
        send_list = {}
        for a in alert_list:
            send_list[a["title"]] = [a["link"], a["description"]]
        return send_list
    except Exception as e:
        print(e)

print("Start scraping")
#get_rss_feed('https://us-cert.cisa.gov/ncas/current-activity.xml')
get_rss_feed('https://us-cert.cisa.gov/ncas/alerts.xml')
#get RSS feed functionr returns a dict. Please feel free to print it out and see how the data is digested in my flask.
