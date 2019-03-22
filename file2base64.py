#! /usr/bin/env python

import sys, os, getopt
import base64


def file2base64(filename, url_flag=False):
  file_buffer = open(filename, 'rb').read()

  b64_buffer = base64.b64encode(file_buffer).decode("utf-8")

  if url_flag:
    result = "url=\'data:image/png;base64," + str(b64_buffer) + "\'"
  else:
    result = b64_buffer

  return result


if __name__ == '__main__':

  if len(sys.argv)>1:
    for fname in sys.argv[1:]:
      print(fname, file2base64(fname))

