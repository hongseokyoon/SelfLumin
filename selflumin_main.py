# -*- coding: utf-8 -*-

import cgi
import xml.dom.minidom
import selumin
import zipfile
import os

PostData = cgi.FieldStorage()
PlatformType = PostData['platformtype'].value
UserID = PostData['getid'].value
TwitList = []
if PlatformType == 'me2':
  TwitList = selumin.user_timeline_me2(UserID)
elif PlatformType == 'twitter'
  TwitList = selumin.user_timeline(UserID)
newdoc = xml.dom.minidom.Document()  
TopNode = newdoc.createElement('twits')
newdoc.appendChild(TopNode)

print 'Content-Type text/html\n\n'
print '<html>'
print '<head>'
print '<title>selflumin main</title>'
print '<style type="text/css">'
print '.box {width: 500px;padding: 10px;}'
print '.b1f, .b2f, .b3f, .b4f{height:1px;font-size:1px;overflow:hidden;display:block;background:#ddd;}' 
print '.b1f {margin:0 5px;}' 
print '.b2f {margin:0 3px;}' 
print '.b3f {margin:0 2px;}' 
print '.b4f {margin:0 1px;}' 
print '.content {padding: 10px;background: #ddd;}' 
print '</style>'
print '</head>'
print '<body>'
print '<a href=./Download/' + UserID + '.zip>파일 다운로드</a>'
RTCount = 0
Me2Count = 0
for twit in TwitList:
  TwitDate = str(twit['date'])
  TwitText = twit['text'].encode('cp949')
  if PlatformType == 'me2':
    Me2Count = twit['me2_count']
  elif PlatformType == 'twitter'
    RTCount = str(twit['rt_count'])
  print '<div class="box">'
  print '    <b class="b1f"></b>'
  print '    <b class="b2f"></b>'
  print '    <b class="b3f"></b>'
  print '    <b class="b4f"></b>'
  print '    <div class="content">'
  print TwitDate
  print '<br>'
  print TwitText
  print '<br>'  
  if PlatformType == 'me2':
    print 'Me2 Count : ' + Me2Count
  elif PlatformType == 'twitter'
    print 'RT Count : ' + RTCount
  print '    </div>'
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
  elif PlatformType == 'twitter'
    CountText = RTCount
  NewCount = newdoc.createTextNode(CountText)
  CountNode.appendChild(NewCount)
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