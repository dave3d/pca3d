#! /usr/bin/env python


import getopt, sys

def scale_point(pt, scale):
  result = []
  if len(scale) == 1:
    # uniform scale
    s = scale[0]
    result = [s*x for x in pt]
  else:
    # non-uniform scale
    for p, s in zip(pt, scale):
      result.append(p*s);
  return result

def translate_point(pt, translate):
  result = []
  for p, t in zip(pt, translate):
    result.append(p+t)
  return result

def rotate_point(pt, rotation):
  #not yet implemented
  return pt

def rotate_vector(v, rotation):
  #not yet implemented
  return v

#
#  Transform a Wavefront OBJ file.  The input of the function, obj, is a list of strings
#  which are the OBJ file.  The mtllib and material allow the user to add or override
#  a material file or material use in the file.
#
def transform_obj( obj, translate=[0.0,0.0,0.0], scale=[1.0,1.0,1.0], rotate=[0.0,0.0,0.0,0.0], mtllib="",
                   material="" ):

  result = []

  if mtllib != "":
    result.append("mtllib " + mtllib + "\n")
  if material != "":
    result.append("usemtl " + material + "\n")

  for l in obj:
    words = l.split()
#    print (words)

    if len(words) == 0:
      continue


    if words[0] == 'v':
      pt = [ float(words[1]), float(words[2]), float(words[3]) ]
      if len(rotate)==4:
        pt1 = rotate_point(pt, rotate)
      else:
        pt1 = pt
      pt2 = scale_point(pt1, scale)
      pt3 = translate_point(pt2, translate)
      result.append("v {0:.6g} {1:.6g} {2:.6g}\n".format(pt3[0], pt3[1], pt3[2]))


    elif words[0] == 'mtllib':
      if mtllib == "":
        # if the function as given no mtllib, let the file's mtllib pass through.
        # if the function was given a mtllib, the file's mtllib is omitted.
        result.append(l+'\n')

    elif words[0] == 'usemtl':
      if material == "":
        # if the function as given no material, let the file's material pass through.
        # if the function was given a material, the file's material is omitted.
        result.append(l+'\n')

    elif words[0] == 'vn':
      if len(rotate) == 4:
        n = [ float(words[1]), float(words[2]), float(words[3]) ]

        # not really implemented
        n1 = rotate_vector(n, rotate)
        result.append("vn {0:.4g} {1:.4g} {2:.4g}\n".format(n1[0], n1[1], n1[2]))
      else:
        result.append(l+'\n')
    else:
      result.append(l+'\n')

  return result


def transform_obj_file( inname, outname, translate=[0.0,0.0,0.0], scale=[1.0,1.0,1.0], rotate=[0.0,0.0,0.0,0.0], mtllib="",
                        material=""):

  with open(inname, 'r') as f:
    inobj = f.read().splitlines()

  outobj = transform_obj(inobj, translate, scale, rotate, mtllib, material)
  inobj.close()

  outfile = open(outname, 'w')
  for x in outobj:
    outfile.write(x)

  outfile.close()


def usage():
  print("")
  print("transform_obj.py [options] input_file [output_file]")
  print("")
  print(" -t 'x y z'   Translate")
  print(" -s 'x y z'   Scale")
  print(" -r 'x y z a' Rotate")
  print(" -l string    Material library file")
  print(" -m string    Material name")


if __name__ == '__main__':
  inname = 'myobj.obj'
  outname = ""

  tlate = [0., 0., 0.]
  scale = [1., 1., 1.]
  rotate = []

  mtllib = ""
  material = ""


  try:
    opts, args = getopt.getopt( sys.argv[1:], "hl:m:s:t:r:",
            [ "help", "mtllib=", "material=", "translate=", "rotate=", "scale=" ] )
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
    elif o in ("-t", "--translate"):
      words = a.split()
      if len(words) != 3:
        usage()
        sys.exit(1)
      tlate = [float(t) for t in words]

    elif o in ("-s", "--scale"):
      words = a.split()
      if len(words) != 3:
        usage()
        sys.exit(1)
      scale = [float(t) for t in words]

    elif o in ("-r", "--rotate"):
      words = a.split()
      if len(words) != 4:
        usage()
        sys.exit(1)
      rotate = [float(t) for t in words]

    else:
      assert False, "unhandled option"


  if len(args):
    inname = args[0]


  if outname == "":

    inobj = open(inname, 'r')


    out_obj = transform_obj(inobj, tlate, scale, rotate, mtllib, material)

    for l in out_obj:
      print (l, end='')
  else:
    transform_obj_file(inname, outname, tlate, scale, rotate, mtllib, material)

