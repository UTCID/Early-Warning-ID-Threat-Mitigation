from scarper import get_rss_feed
def write_message(message, title, date, link, description):
    message = message + "title: " + title +"<br>" + "date: "+ date + "<br>" + "link" + link + "<br>" + "Message:" + description + "<br>"
    return message

def end_file(message):
    import webbrowser
    import os
    f = open('helloworld.html','w')
    message += "</html>"
    f.write(message)
    f.close()
    #Change path to reflect file location
    filename = 'file:///'+os.getcwd()+'/' + 'helloworld.html'
    webbrowser.open_new_tab(filename)
    return
ans = get_rss_feed('https://us-cert.cisa.gov/ncas/alerts.xml')
for a in ans:
    m ="<html>"
    #b = ans[a][1]
    #b.replace("&lt;", "<")
    #b.replace("&gt;",">")
    #b = ans[a][1].replace("&lt;", "<")
    #b = b.replace("&gt;",">")
    #print(b)
    m += write_message(m, a, "1/1/2021", ans[a][0], ans[a][1])
end_file(m)
