#!/usr/bin/env python

import sys

def bed_file(fields,file):
 for l in file:
    zipped = zip(fields, l.strip().split())
    try:
      yield dict(map(lambda z: (z[0][0], z[0][1](z[1])), zipped))
    except ValueError:
      print >> sys.stderr, "WARN Unexpected format:",l
  
import copy
def block_bed(d):
  zipped = zip(d["blockSizes"], d["blockStarts"])
  for z in enumerate(zipped):
    new_d = copy.deepcopy(d)
    new_d["name"] = new_d["name"] + "_" + str(z[0])
    new_d["chromStart"] = new_d["chromStart"] + z[1][1]
    new_d["chromEnd"] = new_d["chromStart"] + z[1][0]
    new_d["blockCount"] = 0
    new_d["blockSizes"] = []
    new_d["blockStarts"] = []
    yield new_d

def block(s):
  return map(int, filter(None, s.split(",")))

if __name__ == "__main__":
  fields = [ ("chrom", str),
             ("chromStart", int),
             ("chromEnd", int),
             ("name", str),
             ("score", int),
             ("strand", str),
             ("thickStart", int),
             ("thickEnd", int),
             ("itemRgb", int),
             ("blockCount", int),
             ("blockSizes", block),
             ("blockStarts", block)]

  f = "\t".join(map(lambda t: "{"+t[0]+"}", fields))
  for d in bed_file(fields, open(sys.argv[1])):
    for exon_d in block_bed(d):
      print f.format(**exon_d)
