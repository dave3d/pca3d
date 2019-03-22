#! /usr/bin/env python

import sys, os, getopt
import base64
import SimpleITK as sitk

import file2base64

debugFlag = False

def make_checkerboard(size=[128,128], pattern_size=16, stripe_flag=False, url_flag=False, color=[]):

  colorFlag = len(color) == 3

#  print (size, pattern_size)
  img = sitk.Image(size,sitk.sitkUInt8)

  for y in range(size[1]):
    blackflag = int((y/pattern_size)) & 1
    #print (y, blackflag)
    v = 255*blackflag

    if not stripe_flag:
      for x in range(size[0]):
        flipflag = int((x/pattern_size)) & 1
        v = 255 * (blackflag != flipflag)
        img[x,y] = v
    else:
      for x in range(size[0]):
        img[x,y] = v

  if len(color) == 3:
      rimg = sitk.Cast(color[0] * img, sitk.sitkUInt8)
      gimg = sitk.Cast(color[1] * img, sitk.sitkUInt8)
      bimg = sitk.Cast(color[2] * img, sitk.sitkUInt8)
      img = sitk.Compose(rimg, gimg, bimg)


  sitk.WriteImage(img, "checker_tmp.png")

  result = file2base64.file2base64("checker_tmp.png", url_flag)

  if not debugFlag:
    os.remove("checker_tmp.png")

  return result


if __name__  == '__main__':

  stripeFlag = False
  colors = []
  width = 16
  dims = []
  urlFlag = False

  def usage():
    print ("")
    print ("make_checkerboard.py [options]")
    print ("")
    print (" -h, --help    This message")
    print (" -D, --debug   Debug flag")
    print (" -d 'X Y'      Image dimensions")
    print (" -s, --stripes Make horizontal stripes instead of a checkerboard")
    print (" -c \'R G B\'  Color image (colors in [0-1]")
    print (" -w int        Pattern width")
    print (" -u, --url     Include the URL stuff in the output string")
    print ("")

  try:
    opts, args = getopt.getopt( sys.argv[1:], "Dhsc:w:d:u",
            [ "debug", "help", "stripes", "color=", "width=", "dims=", "url" ] )
  except getopt.GetoptError as err:
    print (str(err))
    usage()
    sys.exit(1)


  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
      sys.exit()
    elif o in ("-D", "--debug"):
      debugFlag = True
    elif o in ("-s", "--stripes"):
      stripeFlag = True
    elif o in ("-c", "--color"):
      colors = [float(x) for x in a.split()]
    elif o in ("-d", "--dims"):
      dims = [int(x) for x in a.split()]
    elif o in ("-w", "--width"):
      width = int(a)
    elif o in ("-u", "--url"):
      urlFlag = True
    else:
      assert False, "unhandled option"


  if len(dims) != 2:
    dims = [16, 16]

  s = make_checkerboard( size=dims, pattern_size=width, stripe_flag=stripeFlag, color=colors, url_flag = urlFlag )

  print (s)
