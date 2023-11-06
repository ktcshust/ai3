#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from codecs import open
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

"""
CS 188 Local Submission Autograder
Written by the CS 188 Staff

==============================================================================
   _____ _              _ 
  / ____| |            | |
 | (___ | |_ ___  _ __ | |
  \___ \| __/ _ \| '_ \| |
  ____) | || (_) | |_) |_|
 |_____/ \__\___/| .__/(_)
                 | |      
                 |_|      

Modifying or tampering with this file is a violation of course policy.
If you're having trouble running the autograder, please contact the staff.
==============================================================================
"""
import bz2, base64
exec(bz2.decompress(base64.b64decode('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')))

