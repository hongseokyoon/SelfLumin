# -*- coding: utf-8 -*-

import cgi
import xml.dom.minidom
import zipfile
import os
import selumin

PostData = cgi.FieldStorage()
PlatformType = PostData['platformtype'].value
UserID = PostData['getid'].value
TwitList = []

if PlatformType == 'me2':
  TwitList = selumin.user_timeline_me2(UserID)
elif PlatformType == 'twitter':
  TwitList = selumin.user_timeline(UserID)  
  
newdoc = xml.dom.minidom.Document()  
TopNode = newdoc.createElement('twits')
newdoc.appendChild(TopNode)

def IndexSplit(List, n):
  IndexLength = len(List) - 1
  Interval = ((IndexLength) / n)
  retList = []
  for i in range(n * 2):
    Index = i * Interval
    IndexNode = {}
    if Index >= IndexLength or (IndexLength - Index) < (Interval / 2):
      Twit = List[IndexLength]      
      IndexNode[str(IndexLength)] = str(Twit['date'])
      retList.append(IndexNode)
      break
    Twit = List[Index]      
    IndexNode[str(Index)] = str(Twit['date'])
    retList.append(IndexNode)
  return retList

IndexList = IndexSplit(TwitList, 4)

print 'Content-Type text/html\n\n'
print '<html>'
print '<head>'
print '<title>selflumin main</title>'
print '<style type="text/css">'
print '.box {width: 500px;padding: 10px;}'
print '.b1f, .b2f, .b3f, .b4f{height:1px;font-size:1px;overflow:hidden;display:block;background:#B3C5F3;}' 
print '.b1f {margin:0 5px;}' 
print '.b2f {margin:0 3px;}' 
print '.b3f {margin:0 2px;}' 
print '.b4f {margin:0 1px;}' 
print '.content {padding: 10px;background: #B3C5F3;}' 
print '</style>'
print '<script language="JavaScript">'
print '</script>'
print '</head>'
print '<body>'
print '<a href=./Download/' + UserID + '.zip>파일 다운로드</a><br>'
for IndexNode in IndexList:
  for Index, Date in IndexNode.iteritems():
    print '<a href=#' + Index + '>[' + ' ' + Date + ']</a>'
RTCount = 0
Me2Count = 0
PhotoUrl = None
Index = 0;

print '<table>'
print '<tr>'
print '<td>'
for twit in TwitList:
  TwitDate = str(twit['date'])
  try:
    TwitText = twit['text'].encode('cp949')
  except:
    Index += 1
    continue
  if PlatformType == 'me2':
    Me2Count = twit['me2_count']
  elif PlatformType == 'twitter':
    RTCount = str(twit['rt_count'])
  print '<div class="box">'
  print '    <b class="b1f"></b>'
  print '    <b class="b2f"></b>'
  print '    <b class="b3f"></b>'
  print '    <b class="b4f"></b>'
  print '    <div class="content"><a name=' + str(Index) + '>'
  print TwitDate
  print '<br>'
  if PlatformType == 'me2':
    if not twit['photo_url'] == '':
      PhotoUrl = twit['photo_url']
      print '<a href="' + PhotoUrl + '?type=w500"  target="_blank"><img src="' + PhotoUrl + '?type=s44"></a>'
  print TwitText
  print '<br>'  
  if PlatformType == 'me2':
    print 'Me2 Count : ' + Me2Count
  elif PlatformType == 'twitter':
    print 'RT Count : ' + RTCount
  print '    </a><br><a href=#top>[Top]</a></div>'
  print '    <b class="b4f"></b>'
  print '    <b class="b3f"></b>'
  print '    <b class="b2f"></b>'
  print '    <b class="b1f"></b>'
  print '</div>'
  TwitNode = newdoc.createElement('twit')
  TopNode.appendChild(TwitNode)  

  DateNode = newdoc.createElement('date')
  TwitNode.appendChild(DateNode)
  NewDate = newdoc.createTextNode(TwitDate)
  DateNode.appendChild(NewDate)

  TextNode = newdoc.createElement('text')
  TwitNode.appendChild(TextNode)
  NewText = newdoc.createTextNode(TwitText)
  TextNode.appendChild(NewText)
  
  CountNode = newdoc.createElement('count')
  TwitNode.appendChild(CountNode)
  CountText = 0
  if PlatformType == 'me2':
    CountText = Me2Count
  elif PlatformType == 'twitter':
    CountText = RTCount
  NewCount = newdoc.createTextNode(CountText)
  CountNode.appendChild(NewCount)
  
  if PlatformType == 'me2':
    if not PhotoUrl == '' and not PhotoUrl == None:
      PhotoNode = newdoc.createElement('photourl')
      TwitNode.appendChild(PhotoNode)
      NewUrl = newdoc.createTextNode(PhotoUrl)
      PhotoNode.appendChild(NewUrl)
  Index += 1
print '</td>'
print '</tr>'
print '</table>'
print '</body>'
print '</html>'

if not os.path.isdir('./Download'):
  os.mkdir('./Download')  
FileName = './Download/' + UserID + '.txt'
thefile = open(FileName, 'w')
newdoc.writexml(thefile, indent='  ', addindent='  ', newl='\n')
thefile.close()
ZipFileName = './Download/' + UserID + '.zip'
if os.path.isfile(ZipFileName):
  os.remove(ZipFileName)
thezipfile = zipfile.ZipFile(ZipFileName, 'w')
thezipfile.write(FileName, os.path.basename(FileName), zipfile.ZIP_DEFLATED)
thezipfile.close()
if os.path.isfile(FileName):
  os.remove(FileName)