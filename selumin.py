import tweepy
import urllib
import xml.etree.ElementTree as ET
import time

def user_timeline(user_id):
  twits = []
  ''' prevent too many requests temporary
  for status in tweepy.Cursor(tweepy.api.user_timeline, id = user_id).items():
    twit  = {}
    twit['text']      = status.text
    twit['date']      = status.created_at
    twit['rt_count']  = status.retweet_count
    
    twits.append(twit)
  '''
  statuses  = tweepy.api.user_timeline(id = user_id)
  if statuses:
    for status in statuses:
      twit  = {}
      twit['text']      = status.text
      twit['date']      = status.created_at
      twit['rt_count']  = status.retweet_count

      twits.append(twit)
    
  return twits
  
def user_total_posts_me2(user_id):
  xml = ET.fromstring(urllib.urlopen('http://me2day.net/api/get_person/%s.xml' % (user_id)).read())
  return int(xml.find('totalPosts').text)
  
def user_timeline_me2(user_id):
  total_posts = user_total_posts_me2(user_id)
  print total_posts
  
  twits = []
  
  offset  = 0
  count   = 50 if total_posts > 50 else total_posts
    
  while True:
    url = 'http://me2day.net/api/get_posts/%s.xml?offset=%d&count=%d' % (user_id, offset, count)
    
    print url
    res = urllib.urlopen(url)
    
    xml = ET.fromstring(res.read())
  
    for post in xml.findall('post'):
      twit  = {}
      twit['text']      = post.find('textBody').text
      twit['date']      = time.strptime(post.find('pubDate').text, '%Y-%m-%dT%H:%M:%S+0900')
      twit['me2_count']  = post.find('metooCount').text
    
      twits.append(twit)
    
    if offset + count == total_posts:  break;
    
    offset  += count
    count   = 50 if total_posts - offset > 50 else total_posts - offset
    
  return twits
  
def split(l, n):
  chunk_size  = len(l) / n
  for i in range(0, chunk_size if chunk_size * n >= len(l) else chunk_size + 1):
    yield l[i * n:i * n + n]