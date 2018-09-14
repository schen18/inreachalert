from flask import Flask, jsonify, request
import feedparser
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/inreach/riverflow')
def checkriver():
	# Go to https://water.weather.gov/ahps/rss/alerts.php, select By Gauge RSS for State of interest to drill down, replace feedsource with respective Alerts RSS for Gauges of interest
    feedsource=['http://water.weather.gov/ahps2/rss/alert/plfa3.rss','http://water.weather.gov/ahps2/rss/alert/lcca3.rss']
    result=[]

    for rssource in feedsource:
        feed = feedparser.parse(rssource)
        title = feed.entries[0].title
        rawsummary = feed.entries[0].summary
        gaugedata = rawsummary.split('<h2>Gauge Data</h2>')
        soup = BeautifulSoup(gaugedata[1], 'lxml')
        content = soup.findAll('div')
        observed = content[1].text[7:].strip()
        flow = content[2].text[30:].strip()
        observedtime = content[3].text[12:].strip()
        forecast = content[5].text[17:].strip()
        forecasttime = content[7].text[17:].strip()
        result.append(title + '\n' + observed + flow + '\n' + observedtime + '\n' + forecast)

    riverstring = '\n\n'.join(result)
    return riverstring

@app.route('/inreach/upriverflow')
def checkupriver():
	# Go to https://water.weather.gov/ahps/rss/alerts.php, select By Gauge RSS for State of interest to drill down, replace feedsource with respective Alerts RSS for Gauges of interest
    feedsource=['http://water.weather.gov/ahps2/rss/alert/paku1.rss','http://water.weather.gov/ahps2/rss/alert/lcwa3.rss']
    result=[]

    for rssource in feedsource:
        feed = feedparser.parse(rssource)
        title = feed.entries[0].title
        rawsummary = feed.entries[0].summary
        gaugedata = rawsummary.split('<h2>Gauge Data</h2>')
        soup = BeautifulSoup(gaugedata[1], 'lxml')
        content = soup.findAll('div')
        observed = content[1].text[7:].strip()
        flow = content[2].text[30:].strip()
        observedtime = content[3].text[12:].strip()
        forecast = content[5].text[17:].strip()
        forecasttime = content[7].text[17:].strip()
        result.append(title + '\n' + observed + flow + '\n' + observedtime + '\n' + forecast)

    riverstring = '\n\n'.join(result)
    return riverstring

@app.route('/inreach/riverflood')
def checkflood():
    feed = feedparser.parse('https://alerts.weather.gov/cap/us.php?x=0')
    # enter names of county, river, area etc. to narrow down in National Alerts feed
    floodcheck=['Coconino','Paria','Page','Grand Canyon','Glen Canyon']
    result=[]

    for entry in feed.entries:
        article_title = entry.title
        article_summary = entry.summary
        article_event = entry.cap_event
        article_location = entry.cap_areadesc
        if 'Flood' in article_event and any([word in article_location for word in floodcheck]):
            result.append('{}[{}]'.format(article_title, article_summary))

    if not result:
        result.append('Currently No Warnings')

    riverstring = '\n\n'.join(result)
    return riverstring

@app.route('/inreach/alerts')
def checkalert():
	# Go to https://alerts.weather.gov, select the Zone/County list for the State of interest, and replace feedsource list with corresponding ATOM feed urls
    feedsource=['https://alerts.weather.gov/cap/wwaatmget.php?x=AZC005&y=0','https://alerts.weather.gov/cap/wwaatmget.php?x=UTC025&y=0','https://alerts.weather.gov/cap/wwaatmget.php?x=UTC037&y=0']
    result=[]

    for rssource in feedsource:
        feed = feedparser.parse(rssource)
        for entry in feed.entries:
            if 'summary' in entry:
                article_title = entry.title
                #article_event = entry.cap_event
                article_location = entry.cap_areadesc
                article_summary = entry.summary
                result.append('{}[{}]\n{}'.format(article_title, article_location, article_summary))

    if not result:
        result.append('Currently No Alerts')

    warnstring = '\n\n'.join(result)
    return warnstring


