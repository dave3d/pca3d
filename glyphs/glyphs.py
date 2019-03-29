#! /usr/bin/env python


glyphs = {}

glyph_dir = '/Users/dchen/pca3d/glyphs'

def load_glyphs():

  with open(glyph_dir + "/cube.obj", 'r') as box_file:
    box_obj = box_file.read().splitlines()

  print(box_obj)

  glyphs['Box'] = box_obj

  with open(glyph_dir + "/sphere-tex.obj", 'r') as sphere_file:
    sphere_obj = sphere_file.read().splitlines()

  glyphs['Sphere'] = sphere_obj

def get_glyph(name):
  if name in glyphs:
    return glyphs[name]
  else:
    return None
