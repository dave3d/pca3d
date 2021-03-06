#! /usr/bin/env python

#
#  Dave's utility to add polar coordinate texture coordinates to a OBJ mesh.
#
#  I wrote it to add texture coordinates to a sphere model, but it'll actually
#  do it to anything.
#

import math
import cmath
import sys, getopt

inname = 'sphere.obj'
outname = ""

mtllib = 'stripe16.mtl'
material = 'material0'


urange = [1e32, -1e32]
vrange = [1e32, -1e32]

def usage():
  print ("")
  print ("polartex.py [options] [infile [outfile]]")
  print ("")
  print (" -h, --help           This message.  Helpful, eh?\n")
  print (" -l, --mtllib file    Material library file\n")
  print (" -m, --material name  Material name\n")
  print ("")


try:
  opts, args = getopt.getopt( sys.argv[1:], "hl:m:",
            [ "help", "mtllib=", "material=" ] )
except getopt.GetoptError as err:
  print (str(err))
  usage()
  sys.exit(1)


for o, a in opts:
  if o in ("-h", "--help"):
    usage()
    sys.exit()
  elif o in ("-l", "--mtllib"):
    mtllib = a
  elif o in ("-m", "--material"):
    material = a
  else:
    assert False, "unhandled option"


if len(args):
  inname = args[0]

if len(args)>1:
  outname = args[1]
else:
  suffix = '.obj'
  text = inname
  text = text if not text.endswith(suffix) or len(suffix) == 0 else text[:-len(suffix)]

  outname = text + "-tex.obj"

print("")
print("Input file:", inname)
print("Output file:", outname)

infile = open(inname, 'r')
outfile = open(outname, 'w')

outfile.write("# Create by Dave's polartex.py script\n")
outfile.write("#\n")
outfile.write("mtllib {0}\n".format(mtllib))
outfile.write("usemtl {0}\n".format(material))

vcount = 0
fcount = 0

for l in infile:

  words = l.split()
  if len(words) == 0:
    continue


  if words[0] == 'v':
#    print (words)
    x = float(words[1])
    y = float(words[2])
    z = float(words[3])

    c = complex(x,y)

    p = cmath.polar(c)

    theta = p[1]
    u = 0.5*theta/math.pi + 0.5

    if u<urange[0]:
      urange[0] = u
    if u>urange[1]:
      urange[1] = u

    if z<0:
      sign = -1.0
    else:
      sign = 1.0

    phi = math.asin(z)

    v =  phi/math.pi + 0.5
#    print (x, ",", y, ":", u)
#    print (z, ":", v)
#    print ("")

    if v<vrange[0]:
      vrange[0] = v
    if v>vrange[1]:
      vrange[1] = v

    outfile.write(l)
    outfile.write("vt {0:.4g} {1:.4g}\n".format(u,v))
    vcount = vcount + 1

  elif words[0] == 'vt':
    # incoming vertex texture lines are omitted
    continue
  elif words[0] == 'f':
#    print (l)
    outfile.write("f ")
    for vert in words[1:]:
      links = vert.split('/')
#      print (links)
      if not len(links):
        print ("Bad face line: ", l)
        break
      outfile.write("{0}/{0}".format(links[0]))
      if len(links) == 3:
        outfile.write("/{0}".format(links[2]))
      if vert != words[-1]:
        outfile.write(" ")

    outfile.write("\n")
    fcount = fcount + 1

  else:
    outfile.write(l)


print (vcount, "vertices,", fcount, "faces")
print ("U range: ", urange)
print ("V range: ", vrange)
print("")

infile.close()
outfile.close()
