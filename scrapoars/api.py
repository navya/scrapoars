#!/usr/bin/env python3
#
# File: scapoars.py
#
# Created: Sunday, July  6 2014 by rejuvyesh <mail@rejuvyesh.com>
# License: GNU GPL 3 <http://www.gnu.org/copyleft/gpl.html>
#

import requests
import re
import pickle
from bs4 import BeautifulSoup
import os
import time
import subprocess
import json


def getSubjectList(url, file='sublist.p', debug=False):
  '''
  Get subject list
  '''
  response = requests.get(url)
  soup = BeautifulSoup(response.content)
  if debug:
    print(soup.prettify)

  regex = re.compile("^[\s]+([A-Z]+[A-Z]*[0-9]+[A-Z0-9]*)[\n]", re.MULTILINE)
  content = regex.findall(soup.prettify())
  if debug:
    print(content)
  with open(file, 'wb') as f:
    pickle.dump(content, f)
  return content


def scrape(preurl, sublist, htmlpath, sleep=3, force=False, debug=False):
  '''
  Scrape
  '''
  for sub in sublist:
    filename = htmlpath + sub + '.html'
    url = preurl + sub
    if os.stat(filename).st_size > 0 or force:
      time.sleep(sleep)
      attempt = 0
      while attempt < 5:
        try:
          oars = requests.get(url, timeout=1)
          break
        except:
          attempt += 1
      soup = BeautifulSoup(oars.content)
      if debug:
        print(soup.prettify)
      with open(filename, 'wt') as ff:
        ff.write(oars.text)
    else:
      print("File exists: {0}".format(filename))
      continue


def check(preurl, sublist, htmlpath, debug=False):
  '''
  Check for inconsistencies
  '''
  for sub in sublist:
    filename = htmlpath + sub + '.html'
    if os.stat(filename).st_size == 0 or 'error' in open(filename, 'r').read():
      scrape(preurl, [sub], htmlpath, force=True)


def dumpTxt(htmlpath, txtpath, sublist, exe='elinks'):
  '''
  dump txt files
  '''
  for sub in sublist:
    try:
      html = htmlpath + sub + '.html'
      txt = txtpath + sub + '.txt'
      txtoutput = subprocess.Popen([exe, " -dump ", html],
                                   stdout=subprocess.PIPE).communicate()[0]
      with open(txt, 'wt') as f:
        f.write(txtoutput)
    except:
      continue


def parse(txtpath, sublist, debug=False):
  '''
  Parse into a dictionary
  '''
  finaldic = []
  for sub in sublist:
    filename = txtpath + sub + '.txt'
    with open(filename, 'r') as f:
      lines = f.readlines()
    # Split at newlines
    j = ''.join(lines).split("\n")
    # Non empty lines
    k = [x for x in j if x != '']
    k = list(map(lambda x: x.strip(), k))

    dic = {}
    for i in ['Course', 'Title', 'Instructor', 'Schedule', 'Units',
              'Pre', 'Department', 'Inst. email']:
      q = next(s for s in k if s.startswith(i))
      if debug:
        print(q)
      p = q.lstrip().split(":", 1)
      if debug:
        print(p)
      try:
        dic[p[0].lstrip()] = p[1].lstrip()
      except:
        dic[p[0].lstrip] = None
    finaldic.append(dic)
  if debug:
    print(finaldic)
  return finaldic


def toJson(dic, jsonpath):
  '''
  Save to json
  '''
  with open(jsonpath) as f:
    json.dump(dic, f, sort_keys=True, indent=4)
