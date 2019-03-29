#! /usr/bin/env python


glyphs = {}

glyph_dir = '/Users/dchen/pca3d/glyphs'

def load_glyphs():
  box_obj = open(glyph_dir + "/cube.obj", 'r')

  glyphs['Box'] = box_obj

  sphere_obj = open(glyph_dir + "/sphere-tex.obj", 'r')

  glyphs['Sphere'] = sphere_obj

def get_glyph(name):
  if name in glyphs:
    return glyphs[name]
  else:
    return None
