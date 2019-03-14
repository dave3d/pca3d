#! /usr/bin/env python

import sys, getopt
import re

outname = ""
title = "X3Dom test page"

replacement_dict = {}

def usage():
  print ("")
  print ("x3d2html.py [options] input_file1 ... input_fileN")
  print (" -t title    Title of the page")
  print (" -o name     Output file name")
  print (" -r 'string1:string2'  Replace string in input file")
  print (" -d 'replacement dictionary'  Python dictionary with replacement string pairs")
  print (" -h, --help  This help page")
  print ("")


try:
  opts, args = getopt.getopt( sys.argv[1:], "ht:o:r:d:",
            [ "help", "title=", "output=", "replace=", "dict="] )
except getopt.GetoptError as err:
  print (str(err))
  usage()
  sys.exit(1)


for o, a in opts:
  if o in ("-h", "--help"):
    usage()
    sys.exit()
  elif o in ("-t", "--title"):
    title = a
  elif o in ("-o", "--output"):
    outname = a
  elif o in ("-r", "--replace"):
    words = a.split(':')
    if len(words) == 2:
      replacement_dict[words[0]] = words[1]
  elif o in ("-d", "--dict"):
    dict1 = eval(a)
    replacement_dict.update(dict1)
  else:
    assert False, "unhandled option"


if len(sys.argv)<2:
  usage()
  sys.exit(1)


innames = args

firstname = innames[0]

if outname == "":
  if firstname.endswith(".x3d"):
    outname = firstname[:-4] + ".html"
  else:
    outname = firstname + ".html"

print (innames, outname)

print("Replacement dictionary:" + str(replacement_dict))

# https://gist.github.com/bgusach/a967e0587d6e01e889fd1d776c5f3729
substrs = sorted(replacement_dict, key=len, reverse=True)
regexp = re.compile('|'.join(map(re.escape, substrs)))


fout = open(outname, "w")


fout.write("<html>\n")
fout.write("   <head>\n")
fout.write("    <meta http-equiv='X-UA-Compatible' content='IE=edge'/>\n")
fout.write("     <title>" + title + "</title>\n")
fout.write("     <script type='text/javascript' src='https://www.x3dom.org/download/x3dom.js'> </script>\n")
fout.write("     <link rel='stylesheet' type='text/css' href='https://www.x3dom.org/download/x3dom.css'></link>\n")
fout.write("   </head>\n")
fout.write("   <body>\n")
fout.write("     <h1>" + title + "</h1>\n")

fout.write("<x3d width='1000px' height='800px'>\n")


fout.write("<scene>\n")

fout.write("  <background groundColor='.4 .4 .4' skyColor='.6 .6 1'> </background>\n")

fout.write("  <FontStyle DEF='testFontStyle' justify='\"MIDDLE\" \"MIDDLE\"' size='1.5'></FontStyle>\n")


for i in innames:
  print (i)
  fin = open(i, "r")
  for line in fin:
    line1  = regexp.sub(lambda match: replacement_dict[match.group(0)], line)
    fout.write(line1)

  fin.close()

fout.write("  </scene>\n")
fout.write("</x3d>\n")

fout.write("   </body>\n")
fout.write("</html>\n")

