import tweepy

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