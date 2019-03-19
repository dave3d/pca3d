#! /usr/bin/env python


#
#  Script to convert a PCA spreadsheet (in CSV format) to a 3d scatterplot
#  graph in X3D format.
#
#  The 'field_map' shows how the script maps columns in the spreadsheet
#  to the parameters of the scatter plot.
#
#  Each plot in the graph has X-Y-Z position, R for radius, C for color,
#  T for texture (to be implemented), and 'shape' for glyph type.
#

import sys, re, getopt
import pandas as pd

inname = 'pcoa_binomial.csv'
outname = 'output.x3d'

no_text = False
wrl_flag = False

def usage():
  print ("")
  print ("pca2x3d.py [options] input_file")
  print ("  -t       No text labels")
  print ("  -o name  Output file name")
  print ("  -v, --vrml  VRML output")
  print ("")


try:
  opts, args = getopt.getopt( sys.argv[1:], "ho:tv",
            [ "help", "output=", "vrml" ] )
except getopt.GetoptError as err:
  print (str(err))
  usage()
  sys.exit(1)


for o, a in opts:
  if o in ("-h", "--help"):
    usage()
    sys.exit()
  elif o in ("-o", "--output"):
    outname = a
  elif o in ("-t"):
    no_text = True
  elif o in ("-v", "--vrml"):
    wrl_flag = True
  else:
    assert False, "unhandled option"


if len(sys.argv)<2:
  usage()
  sys.exit(1)


innames = args


df = pd.read_csv(innames[0])
print (df)

import matplotlib.pyplot as plt
import matplotlib.colors as colors

cmap = plt.get_cmap('coolwarm')

#print(cmap)

range_init = [1e32, -1e32]
field_map = { 'x': 'PCo1', 'y': 'PCo2', 'z': 'PCo3', 'r': 'PCo4', 'c': 'PCo5', 't': 'PCo6', 'shape': 'TreatmentGroup', 'name': 'SampleID' }
ranges = {}
for k, v in field_map.items():
  ranges[k] = (list(range_init))

rscale = 5.0

shape_map = {'C.accolens': 'Sphere', 'Unassociated': 'Box', '': 'Cylinder' }


def output_sample( fout, name, pos,size, color, shape='Sphere' ):
  if wrl_flag:
    fout.write("Transform {\n")
    fout.write("  translation {0:.4g} {1:.4g} {2:.4g}\n".format(pos[0], pos[1], pos[2]))
    fout.write("  scale {0:.3g} {0:.3g} {0:.3g}\n".format(size))
    fout.write("  children [\n")
    fout.write("    Shape {\n")
    fout.write("      appearance Appearance {\n")
    fout.write("        material Material {\n")
    fout.write("          diffuseColor {0:.3g} {1:.3g} {2:.3g}\n".format(color[0], color[1], color[2]))
    fout.write("        }\n")
    fout.write("      }\n")
    fout.write("      geometry " + shape + " {\n")
    fout.write("      }\n")
    fout.write("    }\n")
  else:
    tform = "<Transform translation=\'{0:.4g} {1:.4g} {2:.4g}\' scale=\'{3:.3g} {3:.3g} {3:.3g}\'>\n".format(pos[0], pos[1], pos[2], size)
    fout.write(tform)
    fout.write("  <Shape>\n")
    mat = "    <Appearance> <Material diffuseColor=\'{0:.3g} {1:.3g} {2:.3g}\'/> </Appearance>\n".format(color[0], color[1], color[2])
    fout.write(mat)
    fout.write("    <"+shape+"/>\n")
    fout.write("  </Shape>\n")

  if not no_text:
    if wrl_flag:
      fout.write("    Transform {\n")
      fout.write("      translation 0 -2 0\n")
      fout.write("      children [\n")
      fout.write("        Shape {\n")
      fout.write("          geometry Text {\n")
      fout.write("            string \"" + name + "\"\n")
      fout.write("          }\n")
      fout.write("        }\n")
      fout.write("      ]\n")
      fout.write("    }\n")

    else:
      fout.write("  <Transform translation=\'0 -2 0\'>\n")
      fout.write("    <Shape>\n")
      textstring = "      <Text string=\'{0}\' solid=\'false\'> <FontStyle USE=\'testFontStyle\'></FontStyle> </Text>\n".format(name)
      fout.write(textstring)
      fout.write("    </Shape>\n")
      fout.write("  </Transform>\n")

  if wrl_flag:
    fout.write("  ]\n")
    fout.write("}\n")
  else:
    fout.write("</Transform>\n")



fout = open(outname, "w")


if wrl_flag:
  fout.write("#VRML V2.0 utf8\n")
  fout.write("# Generated by script {0} on CSV file {1}\n".format(__file__, inname))
else:
  fout.write("\n<!-- Generated by script {0} on CSV file {1} -->\n".format(__file__, inname))


# Get the data ranges
for index, row in df.iterrows():
  for k, v in field_map.items():
    val = row[v]
    if type(val)==int or type(val)==float:
      vrange = ranges[k]
      if val<vrange[0]:
        vrange[0] = val
      if val>vrange[1]:
        vrange[1] = val



print ("\nData ranges")
for k, v in ranges.items():
  print( k, ":", v[0], v[1] )


c_range = ranges['c']
cnorm = colors.Normalize(vmin=c_range[0], vmax=c_range[1])

print ("\nColor mappings")
print ( cnorm(c_range[0]), cmap(cnorm(c_range[0])) )
print ( cnorm(c_range[1]), cmap(cnorm(c_range[1])) )
print ( cnorm(0.0), cmap(cnorm(0.0)) )

r_range = ranges['r']
rnorm = colors.Normalize(vmin=r_range[0], vmax=r_range[1])

for index, row in df.iterrows():
  name = row[field_map['name']]
  x = row[field_map['x']]
  y = row[field_map['y']]
  z = row[field_map['z']]
  r = rscale*rnorm(row[field_map['r']]) + 1.0
  c = row[field_map['c']]
  shape = row[field_map['shape']]

  if shape in shape_map:
    myshape = shape_map[shape]
  else:
    myshape = 'Sphere'
  output_sample( fout, name, [x,y,z], r, cmap(cnorm(c)), myshape )

fout.close()

print ("")
