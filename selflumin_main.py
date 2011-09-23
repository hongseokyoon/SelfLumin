# -*- coding: utf-8 -*-

import cgi
import selumin
import codecs
import xml.dom.minidom

PostData = cgi.FieldStorage()
TwitList = selumin.user_timeline(PostData['getid'].value)
#XmlImpl = xml.dom.minidom.getDOMImplementation()
#newdoc = XmlImpl.createDocument(None, 'some_tag', None)
#top_element = newdoc.documentElement
#text = newdoc.createTextNode('Some textual content.')
#top_element.appendChild(text)
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

for twit in TwitList:
  TwitDate = str(twit['date'])
  TwitText = twit['text'].encode('cp949')
  print '<div class="box">'
  print '    <b class="b1f"></b>'
  print '    <b class="b2f"></b>'
  print '    <b class="b3f"></b>'
  print '    <b class="b4f"></b>'
  print '    <div class="content">'
  print TwitDate
  print '<br>'
  print TwitText
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
print '</body>'
print '</html>'

thefile = open('test.txt', 'w')
newdoc.writexml(thefile, indent='  ', addindent='  ', newl='\n')
thefile.close()
