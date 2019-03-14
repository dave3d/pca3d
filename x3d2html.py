#! /usr/bin/env python

import sys, getopt

outname = ""
title = "X3Dom test page"

def usage():
  print ("")
  print ("x3d2html.py [options] input_file1 ... input_fileN")
  print (" -t title    Title of the page")
  print (" -o name     Output file name")
  print (" -h, --help  This help page")
  print ("")


try:
  opts, args = getopt.getopt( sys.argv[1:], "ht:o:",
            [ "help", "title=", "output=", ] )
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
    fout.write(line)

  fin.close()

fout.write("  </scene>\n")
fout.write("</x3d>\n")

fout.write("   </body>\n")
fout.write("</html>\n")

