#! /usr/bin/python
import sys
import csv

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$Apr 24, 2014"

def usage():
    print """
        python filter_omim.py [omim.txt]
        """

def filter(omim_db):
    l = omim_db.readline()
    f = open("filtered_omim.txt", "w")
    keep_going = 0
    #rudimentary version of loading the data file, the point is that it can be loaded in whichever way we need
    while l:
        parts = l.split(' ')
        if parts[0] == '*FIELD*':
            if parts[1] == 'AV\n':
                keep_going = 1
            else:
                keep_going = 0
        if keep_going == 1:
            f.write(l)
        l = omim_db.readline()
    f.close()

if len(sys.argv)!= 2:
    usage()
    sys.exit(2)

try:
    omim_db = file(sys.argv[1],"r")
    filter(omim_db)

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)

