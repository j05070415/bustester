# -*- coding: utf-8 -*-
"""
Created on Tue Apr 09 15:26:30 2019

@author: shiweijun
@E-mail: 824044645@qq.com
"""
import sys

# Version number typically updated by running `invoke set_version <version>`.
# Run `invoke --help set_version` or see tasks.py for details.
VERSION = '1.0.0'


def get_version():
    return VERSION


def get_full_version(program=None):
    version = '%s %s (Python %s on %s)' % (program or '',
                                       get_version(),
                                       sys.version.split()[0],
                                       sys.platform)
    return version.strip()

if __name__ == "__main__":
    print get_full_version()
    print get_version(True)
