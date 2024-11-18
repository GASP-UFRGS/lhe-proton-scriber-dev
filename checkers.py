import sys
import os
import configparse
import argparse

def syntax():
    print("Syntax: python3 proton-scriber.py -i <path of .lhe file> -mc <generator> --tag <tag> -pu <pileup> --ids <IDs>")
    print("")
    print("  -c, --config: configuration file for input parameters")
    print("  -i, --inputfile: Path to LHE input file")
    print("  -mc, --generator: Generator type (madgraph or superchic)")
    print("  --tag: Prefix to be added to the output filename")
    print("  -pu, --pileup: Add pileup protons (True/False)")
    print("  --ids: PDG IDs of particles, separated by space, e.g., '22 22'")
    print("")

def parse_config():
    config = configparser.ConfigParser()
    config.read(config_file)
    return {
        "inputfile": config.get("SETTINGS", "inputfile", fallback=None),
        "generator": config.get("SETTINGS", "generator", fallback=None),
        "tag": config.get("SETTINGS", "tag", fallback=None),
        "pileup": config.get("SETTINGS", "pileup", fallback=None),
        "ids": config.get("SETTINGS", "ids", fallback=None)
    }

def parse_args():
    # define the argument parser
    parser = argparse.ArgumentParser(
        description="Proton-scriber script for handling .lhe files.",
        usage="python3 proton-scriber.py -i <path of .lhe file> -mc <generator> --tag <tag> -pu <pileup> --ids <IDs>"
    )
 
    # required positional arguments
    parser.add_argument("-c", "--config", help="Path to configuration file")
    parser.add_argument("-i", "--inputfile", help="Path to LHE input file")
    parser.add_argument("-mc", "--generator", choices=["madgraph", "superchic"], help="Generator type (madgraph or superchic)")
    parser.add_argument("--tag", help="Prefix to be added to the output filename", default="NEW_")
    parser.add_argument("-pu", "--pileup", choices=["True", "False"], help="Add pileup protons (True/False)", default=False)
    parser.add_argument("--ids", help="PDG IDs of particles, separated by space, e.g., \"22 22\"", default="0")

    # parse arguments
    args = parser.parse_args()

    # check if a configuration file is provided
    config_args = {}
    if args.config:
        config_args = parse_config(args.config)

    # combine arguments from both command-line and config file
    _inputfile = os.path.basename(args.inputfile) if args.inputfile else os.path.basename(config_args.get("inputfile", ""))
    _generator = args.generator or config_args.get("generator")
    _tag = args.tag or config_args.get("tag")
    _pileup = args.pileup or config_args.get("pileup")
    _ids = args.ids or config_args.get("ids")

    # validate required arguments
    if not all([_inputfile, _generator]) or len(sys.argv) == 1:
        print("Error: Missing required arguments.")
        syntax()
        sys.exit(1)

    # parse PDG IDs as a list
    _ids_list = args.ids.split()

    return {
            "inputfile": _inputfile,
            "generator": _generator,
            "tag"      : _tag,
            "pileup"   : _pileup,
            "ids"      : _ids_list
           }

def check_header(_event,_newheader,_generator):
    if _generator == 'superchic':
        _newheader[0] = ' '+str(int(_newheader[0])+1)
        _event.pop(1)
        _event.insert(1, '    '.join(_newheader)+'\n')
    if _generator == 'madgraph':
        _newheader[0] = ' '+str(int(_newheader[0])+1)+'     '
        _event.pop(1)
        _event.insert(1, ' '.join(_newheader)+'\n')
    return _event

def num_lines(_file):
    with open(_file, 'r') as _f:
        _num_lines = sum(1 for line in _f)
    return _num_lines

def count_events_in_lhe(_file):
    _event_count = 0
    with open(_file, 'r') as _f:
        for _line in _f:
            if "<event>" in _line:
                _event_count += 1
    return _event_count

