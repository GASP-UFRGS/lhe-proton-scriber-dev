import sys
import os

def check_args():
    # Receives file path, generator of origin and particle IDs as arguments
    if len(sys.argv) < 6:
        print('Missing arguments')
        syntax()
        sys.exit()
    _generator = sys.argv[2]
    if not _generator == 'madgraph' or _generator == 'superchic':
        print('<<'+_generator+'>> generator unsupported. Only "madgraph" and "superchic" are supported. Exiting.')
        sys.exit()
    return collect(sys.argv)

def collect(_args):
    return {
            "inputfile": os.path.basename(_args[1]),
            "generator": _args[2].lower(),
            "tag"      : _args[3],
            "pileup"   : _args[4],
            "ids"      : _args[5:],
           }

def syntax():
    print('Syntax: python3 proton-scriber.py <path of .lhe file> <generator> <tag> <pileup> <IDs>')
    print("")
    print(  "<path of .lhe file> -- path to LHE input file")
    print(  "<generator> -- only madgraph or superchic options supported")
    print(  "<tag> -- prefix to be added to the output filename")
    print(  "<pileup> -- True or False for adding pileup protons")
    print(  "<IDs> -- PDG ID of particles for kinematics of scattered proton, e.g., '22 22' ")
    print("") 

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

