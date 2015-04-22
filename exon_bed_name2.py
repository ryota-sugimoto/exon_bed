#!/usr/bin/env python

def spliter(s):
  return [ int(ss) for ss in filter(lambda x:x, s.split(",")) ]

def parse_input(f):
  fields = [("bin",int),
            ("name",str),
            ("chrom",str),
            ("strand",str),
            ("txStart",int),
            ("txEnd",int),
            ("cdsStart",int),
            ("cdsEnd",int),
            ("exonCount",int),
            ("exonStarts",spliter),
            ("exonEnds",spliter),
            ("score",int),
            ("name2",str),
            ("cdsStartStat",str),
            ("cdsEndStat",str),
            ("exonFrames",spliter),]
  for s in f:
    if s[0] != "#":
      l = s.strip().split()
      yield { key:const(value) for (key,const),value in zip(fields,l) }

def split_exome(d):
  start_end = zip(d["exonStarts"], d["exonEnds"])
  for count,(start,end) in enumerate(start_end):
    dd = { "chrom": d["chrom"],
           "chromStart": start,
           "chromEnd": end,
           "name": d["name"] + "_" + str(count),
           "score": d["score"],
           "strand": d["strand"],
           "thickStart": start,
           "thickEnd": end,
           "itemRgb": 0,
           "blockCount": 1,
           "blockSizes": end-start,
           "blockStarts": start,
           "name2": d["name2"] }
    yield dd

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("input",
                      type=argparse.FileType("r"))
  args = parser.parse_args()
  out_fields = ["chrom", 
                "chromStart",
                "chromEnd",
                "name",
                "score",
                "strand",
                "thickStart",
                "thickEnd",
                "itemRgb",
                "blockCount",
                "blockSizes",
                "blockStarts",
                "name2"]
  for exome_d in parse_input(args.input):
    for exon_d in split_exome(exome_d):
      print "\t".join(map(lambda s: "{"+s+"}",out_fields)).format(**exon_d)
