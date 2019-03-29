#! /usr/bin/env python


#
#  Script to convert a PCA spreadsheet (in CSV format) to a 3d scatterplot
#  graph in OBJ format.
#
#  The 'field_map' shows how the script maps columns in the spreadsheet
#  to the parameters of the scatter plot.
#
#  Each plot in the graph has X-Y-Z position, R for radius, C for color,
#  T for texture (to be implemented), and 'shape' for glyph type.
#

import sys, re, getopt
import pandas as pd
from datetime import datetime


inname = 'pcoa_binomial.csv'

no_text = False
wrl_flag = False

def usage():
  print ("")
  print ("pca2obj.py [options] input_file")
  print ("  -t       No text labels")
  print ("  -o name  Output file name")
  print ("")


# process command line options
#
try:
  opts, args = getopt.getopt( sys.argv[1:], "ho:t",
            [ "help", "output=", ] )
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
  else:
    assert False, "unhandled option"


if len(sys.argv)<2:
  usage()
  sys.exit(1)


innames = args


#
# Load PCA data
#
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


from glyphs import glyphs

glyphs.load_glyphs()

print (glyphs.glyphs)

import transform_obj
import mtllib


def output_sample( name, pos,size, color, shape='Sphere' ):
  print(name, shape)
  glyph_model = glyphs.get_glyph(shape)
  if glyph_model == None:
    printf("Error: Unknown glyph ", shape)
    return

  print("Glyph size: ", len(glyph_model) )

  obj_name = name + ".obj"
  mtl_name = name + ".mtl"
  material_name = name +"MTL"

  obj = transform_obj.transform_obj( glyph_model, translate=pos, scale=[size,size,size], mtllib=mtl_name, material=material_name )
  print("Tranformed glyph size: ", len(obj) )


  fout = open(obj_name, 'w')
  for x in obj:
    fout.write(x)
  fout.close()
  mtllib.make_mtllib( mtl_name, material_name, color=color )



# Get the data ranges
#
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


#
#  Create the samples
#
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
  output_sample( name, [x,y,z], r, cmap(cnorm(c)), myshape )

