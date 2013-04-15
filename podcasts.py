import re
import sys
import time
import urllib2
import xmldict
from pprint import pprint as pp

reload(sys) 
sys.setdefaultencoding('utf-8') 

class Podcasts:

    def __init__(self, **kwargs):
        self.opt = kwargs


    def getFeed(self):
        data = []

        for podcast in self.opt['podcasts']:
            get = urllib2.urlopen(podcast).read()
            xml = xmldict.xml_to_dict(get)
            data += xml['rss']['channel']['item']

        return data


    def getItems(self):
        data = []

        for i in self.getFeed():
            i['pubDate'] = ' '.join(i['pubDate'].split()[:-1]) + ' +0000'
            i['pubDate'] = time.strftime("%s", time.strptime(i['pubDate'], '%a, %d %b %Y %H:%M:%S +0000'))
            data.append(i)


        arranged = sorted(data, key=lambda x: x['pubDate'])[::-1]
        data = []

        for j in arranged:
            j['pubDate'] = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(int(j['pubDate'])))
            data.append(j)

        return data


    def makeXML(self, arr):
        resp = u""
        for k, v in arr.iteritems():
            if '{http://www.w3.org/2005/Atom/}' in k:
                k = k.replace('{http://www.w3.org/2005/Atom/}', 'atom:')
            if '{http://www.itunes.com/dtds/podcast-1.0.dtd}' in k:
                k = k.replace('{http://www.itunes.com/dtds/podcast-1.0.dtd}', 'itunes:')
            if '{http://purl.org/rss/1.0/modules/content/}' in k:
                k = k.replace('{http://purl.org/rss/1.0/modules/content/}', 'content:')


            if type(v) == dict:
                temp = u'<'+k+' '
                for i,j in v.iteritems():
                    temp += u''+i.lstrip('@') + '="' + j + '" '
                temp += u"/>\n"
                resp += u''+temp
            else:
                if type(v) != list and v != None:
                    try:
                        resp += u"<%s>%s</%s>\n" % (k, v.encode('utf-8', 'ignore'), k)
                    except:
                        print k,v.encode('utf-8', 'ignore')
        return resp


    def makeFeed(self):
        data = self.getItems()

        ret = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:sy="http://purl.org/rss/1.0/modules/syndication/" xmlns:admin="http://webns.net/mvcb/" xmlns:atom="http://www.w3.org/2005/Atom/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>5by5 Master Audio Feed</title>
    <link>http://5by5.tv/</link>
    <pubDate>Sun, 14 Apr 2013 05:00:00 GMT</pubDate>
    <description>5by5 - All Audio Broadcasts</description>
    <language>en-us</language>
    <itunes:new-feed-url>http://feeds.5by5.tv/master</itunes:new-feed-url>
    <itunes:subtitle>5by5 - All Audio Broadcasts</itunes:subtitle>
    <itunes:author>5by5 and Dan Benjamin</itunes:author>
    <itunes:summary>5by5 is an internet broadcast studio making podcasts for people like you.</itunes:summary>
    <itunes:image href="http://5by5.tv/assets/5by5-itunes.jpg"/>
    <itunes:keywords>5by5, 5x5, 5 by 5, five by five</itunes:keywords>
    <itunes:explicit>no</itunes:explicit>
    <itunes:owner>
      <itunes:name>5by5 Studios and Dan Benjamin</itunes:name>
      <itunes:email>itunes@5by5.tv</itunes:email>
    </itunes:owner>
    <itunes:category text="Technology">
      <itunes:category text="Tech News"/>
    </itunes:category>'''
        for i in data:
            ret += '<item>'+self.makeXML(i)+'</item>'

        ret += '''</item>
  </channel>
</rss>'''

        return ret
        xml = {'rss': {'channel' : {'description' : "Kartik's Feeds", 'item' : data,
 'language': 'en-us',
                     'link': 'http://5by5.tv/',
                     'pubDate': 'Fri, 12 Apr 2013 19:30:00 GMT',
                     'title': '5by5 Master Audio Feed',
                     '{http://www.itunes.com/dtds/podcast-1.0.dtd}author': '5by5 and Dan Benjamin',
                     '{http://www.itunes.com/dtds/podcast-1.0.dtd}category': {'{http://www.itunes.com/dtds/podcast-1.0.dtd}category': {'@text': 'Tech News'}},
                     '{http://www.itunes.com/dtds/podcast-1.0.dtd}explicit': 'no',
                     '{http://www.itunes.com/dtds/podcast-1.0.dtd}image': {'@href': 'http://5by5.tv/assets/5by5-itunes.jpg'},
                     '{http://www.itunes.com/dtds/podcast-1.0.dtd}keywords': '5by5, 5x5, 5 by 5, five by five',
                     '{http://www.itunes.com/dtds/podcast-1.0.dtd}new-feed-url': 'http://feeds.5by5.tv/master',
                     '{http://www.itunes.com/dtds/podcast-1.0.dtd}owner': {'{http://www.itunes.com/dtds/podcast-1.0.dtd}email': 'itunes@5by5.tv',
                                                                           '{http://www.itunes.com/dtds/podcast-1.0.dtd}name': '5by5 Studios and Dan Benjamin'},
                     '{http://www.itunes.com/dtds/podcast-1.0.dtd}subtitle': '5by5 - All Audio Broadcasts',
                     '{http://www.itunes.com/dtds/podcast-1.0.dtd}summary': '5by5 is an internet broadcast studio making podcasts for people like you.'
}}}

        resp = '<?xml version="1.0" encoding="UTF-8"?>'


urls = ['http://5by5.tv/rss', 'http://feeds.feedburner.com/tedtalks_video', 'http://www.merriam-webster.com/word/index.xml',
        'http://www.scientificamerican.com/podcast/sciam_podcast_i_psych.xml', 'http://feeds.feedburner.com/freakonomicsradio']
pod = Podcasts(podcasts=urls)
rss = pod.makeFeed()

print rss
