from lxml import etree as et
from bz2file import BZ2File
import time
import os

path = "enwiki.xml.bz2"

savefile = "enwiki_p1"
savefileindex = "enwiki_index_p1"

i = 0
text_list = []
index_list = []
with BZ2File(path) as xml_file:
    parser = et.iterparse(xml_file, events=('end',))
    for events, elem in parser:

        #If we hit a page, analyze it a determine if it should be included
        if elem.tag == "{http://www.mediawiki.org/xml/export-0.10/}page":
            ns = elem.find('{http://www.mediawiki.org/xml/export-0.10/}ns').text

            if ns == "0":
                text = elem.find("{http://www.mediawiki.org/xml/export-0.10/}revision") \
                      .find("{http://www.mediawiki.org/xml/export-0.10/}text").text
                if len(text) >= 9:
                    if text[:9] != "#REDIRECT":

                        title = elem.find("{http://www.mediawiki.org/xml/export-0.10/}title").text
                        idz = elem.find("{http://www.mediawiki.org/xml/export-0.10/}id").text
                        text = text.lower().replace("\n", " ")
                        index_list.append("{}, {}".format(idz, title.lower()))
                        text_list.append(text)

                        #If the list grows too large, save it to file
                        if len(index_list) >= 1000:
                            with open(savefile, 'a') as sfile:
                                sfile.write("\n".join(text_list))
                            with open(savefileindex, 'a') as sindex:
                                sindex.write("\n".join(index_list))

                            #If file is over 2GB, create a new
                            if os.stat(savefile).st_size >= 2e9:
                                savefile = savefile[:8] + str(int(savefile[8:])+1)
                                savefileindex = savefileindex[:14] + str(int(savefileindex[14:])+1)
                            index_list = []
                            text_list = []
                        
                    #Print progress of script
                    i += 1
                    if (i % 1000) == 0:
                        print(i)

        ## Do some cleaning
        # Get rid of that element   
            elem.clear()

        # Also eliminate now-empty references from the root node to node        
            while elem.getprevious() is not None:
                del elem.getparent()[0]
