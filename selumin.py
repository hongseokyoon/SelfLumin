import tweepy

def user_timeline(user_id):
  ret   = []
  
  page  = 1
  twits  = tweepy.api.user_timeline(id = user_id, page = page)
  while len(twits) > 0:
    for twit in twits:
      ret.append({'text':twit.text, 'date':twit.created_at})
    
    page  += 1
    twits = tweepy.api.user_timeline(id = user_id, page = page)
    
  return ret