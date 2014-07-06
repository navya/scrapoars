#!/usr/bin/env python3
#
# File: __init__.py
#
# Created: Sunday, July  6 2014 by rejuvyesh <mail@rejuvyesh.com>
# License: GNU GPL 3 <http://www.gnu.org/copyleft/gpl.html>
#

__title__ = 'scrapoars'
__version__ = '0.1.0'
__author__ = 'rejuvyesh'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2014, rejuvyesh'

from .api import getSubjectList, scrape, check, dumpTxt, parse, toJson
