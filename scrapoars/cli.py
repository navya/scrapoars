#!/usr/bin/env python3
#
# File: cli.py
#
# Created: Sunday, July  6 2014 by rejuvyesh <mail@rejuvyesh.com>
# License: GNU GPL 3 <http://www.gnu.org/copyleft/gpl.html>
#

from scrapoars import (__version__, getSubjectList, scrape,
                       check, dumpTxt, parse, toJson)

import argparse
import os
import pickle
import shutil


def scrapoars():
  parser = argparse.ArgumentParser(prog='scrapoars',
                                   description='Scrape the crappy iit-k OARS website',
                                   epilog='Suggestions and bug reports are greatly appreciated at: ',
                                   add_help=False)
  
  # trouble shooting
  troubleshooting_group = parser.add_argument_group('troubleshooting')
  troubleshooting_group.add_argument('--debug', action='store_true', help='debug output')
  troubleshooting_group.add_argument('-v', '--version', action='version', version=__version__)
  troubleshooting_group.add_argument('-h', '--help', action='help', help='show this help message and exit')

  # external program
  ext_group = parser.add_argument_group('external')
  ext_group.add_argument('-e', '--exe', default='elinks', help='External program to use for html2text conversion')
  
  # output
  output_group = parser.add_argument_group('output')
  output_group.add_argument('-s', '--sublist', help='save subject list')
  output_group.add_argument('-m', '--html_dir', help='save htmls in this directory')
  output_group.add_argument('-t', '--txt_dir', help='save txts in this directory')
  output_group.add_argument('-j', '--json', help='save list')
  
  args = parser.parse_args()

  if os.path.exists(args.sublist):
    with open(args.sublist, 'rb') as f:
      sublist = pickle.load(f)
  
  else:
    suburl = 'http://172.26.142.75:4040/Common/CourseListing.asp'
    sublist = getSubjectList(suburl, args.sublist, args.debug)

  preurl = "http://172.26.142.75:4040/Utils/CourseInfoPopup2.asp?Course="
  scrape(preurl, sublist, args.html_dir, args.debug)

  check(preurl, sublist, args.html_dir, args.debug)

  dumpTxt(args.html_dir, args.txt_path, sublist, args.debug)

  if not shutil.which(args.exe) is None:
    dic = parse(args.txt_dir, sublist, args.debug)
  else:
    raise Exception("Specified exe not found")
    exit(1)

  toJson(dic, args.json)
  print("Done!")
