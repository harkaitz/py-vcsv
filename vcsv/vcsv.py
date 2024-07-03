"""
Usage: vcsv OPTIONS... KEY

Extract data from a "Vertical CSV file (VCSV)". A vertical CSV has keys
in it's first columns and values in the rest.

  -h           : Print this help.
  -s SKEY      : A "KEY" is a section delimeter.
  -e IKEY      : When in a section this key finishes it.
  -n COL       : Select a column.
  -N KEY=VAL   : Select a column finding a "KEY", "VAL" row.
  -D DELIMETER : Set output delimeter.
  -P OPT=VAL   : Parsing options: DELIMETER, QUOTECHAR

Copyright (C) 2024 Harkaitz Agirre, harkaitz.aguirre@gmail.com
"""
import os
import sys
import getopt
import csv

def vcsv_exec(arguments, inp=sys.stdin, out=sys.stdout):
    ## Variables
    SectionStarts = []
    SectionEnds = []
    Column = -1
    ColumnKey = None
    ColumnVal = None
    CSVDelimeter = ","
    CSVQuotechar = '"'
    Delimeter = "	"
    ROWS = None
    ## Parse arguments
    opts, args = getopt.getopt(arguments, "s:e:n:N:D:P:")
    for optopt, optarg in opts:
        if optopt == "-s":
            SectionStarts.append(optarg)
            SectionEnds.append(optarg)
        elif optopt == "-e":
            SectionEnds.append(optarg)
        elif optopt == "-n":
            Column = int(optarg)
        elif optopt == "-N":
            ColumnKey, ColumnVal = optarg.split("=", 1)
        elif optopt == "-D":
            Delimeter = optarg
        elif optopt == "-P":
            key, val = optarg.split("=", 1)
            if key == "DELIMETER":
                CSVDelimeter = val
            elif key == "QUOTECHAR":
                CSVQuotechar = val
            else:
                raise Exception("Invalid option: " + key)
    if len(args) > 0:
        Key = args[0]
    else:
        raise Exception("Key not provided")
    ## Parse CSV
    ROWS = csv.reader(inp, delimiter=CSVDelimeter, quotechar=CSVQuotechar)
    ## Fetch rows and column when needed.
    ColumnFound = (ColumnKey is None)
    FoundRows = []
    InsideSection = False
    for row in ROWS:
        if ColumnFound == False:
            if row[0] != ColumnKey:
                pass
            elif ColumnVal in row[1:]:
                Column = row[1:].index(ColumnVal) + 1
                ColumnFound = True
            else:
                raise Exception("Column value not found: " + ColumnVal)
        elif Key is None:
            FoundRows.append(row[Column])
        elif InsideSection and (row[0] in SectionEnds or row[0] in SectionStarts):
            InsideSection = False
        elif Key == row[0] and row[0] in SectionStarts:
            InsideSection = True
        elif Key == row[0] or InsideSection:
            FoundRows.append(row)
    if ColumnFound == False:
        raise Exception("Column key not found: " + ColumnKey)
    if len(FoundRows) == 0:
        raise Exception("Key not found: " + Key)
    ## Print values.
    for row in FoundRows:
        if Column == -1:
            out.write(Delimeter.join(row))
        else:
            out.write(row[Column])
        out.write("\n")


def vcsv_main():
    if len(sys.argv) <= 1 or sys.argv[1] in ["-h", "--help"]:
        sys.stdout.write(__doc__.strip()+"\n")
        sys.exit(0)
    elif os.getenv("DEBUG") is None:
        try:
            vcsv_exec(sys.argv[1:])
        except Exception as err:
            sys.stderr.write("vcsv_get: error: "+str(err)+"\n")
            sys.exit(2)
    else:
        vcsv_exec(sys.argv[1:])
