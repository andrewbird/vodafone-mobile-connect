# Looks for the browser icon in the xfce4 custom desktop on the aspire one.
# Inserts the new icon for Vodafone Mobile Connect and resequences the following
# icons to suit. It works well except it strips the comments from the XML file

from xml.etree import ElementTree as ET
import re,sys

source='group-app.xml'
target='group-app.new'

# We are looking for this
# <group>
#  <app sequence="1">/usr/share/applications/linpus-web.desktop</app>
#
tree = ET.parse(source)
for group in tree.getiterator('group'):
    linpus_web_seq=-1
    pos=0
    for kid in group.getchildren():
        if kid.tag == 'app':
            if re.search('.*vmc.desktop',kid.text):
                print 'VMC icon is already present'
                sys.exit()
            if re.search('.*linpus-web.*',kid.text):
                linpus_web_seq=int(kid.get('sequence'))
                linpus_web_pos=pos
        pos+=1
            
    if linpus_web_seq != -1:
        print 'VMC icon is being added'
# add one onto the sequence number of all the elements greater than 'linpus-web'
        for kid in group.getchildren():
            if kid.tag == 'app':
                cur_seq=int(kid.get('sequence'))
                if cur_seq > linpus_web_seq:
                    kid.set('sequence','%d' % (cur_seq + 1))

# now insert this just after linpus-web
        newapp = ET.Element('app', sequence='%d' % (linpus_web_seq+1))
        newapp.text='/usr/share/applications/vmc.desktop'
        group.insert(linpus_web_pos+1,newapp)

tree.write(target)


