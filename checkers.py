import sys

def check_args(_generator):
    # Receives file path, generator of origin and particle IDs as arguments
    if len(sys.argv) < 5:
        print('Missing arguments')
        print('Syntax: python3 LHE-Proton-Writer.py <path of .lhe file> <generator of origin> <pileup:True/False> <IDs>')
        sys.exit()
    if not _generator == 'madgraph' or _generator == 'superchic':
        print('<<'+_generator+'>> generator unsupported. Only "madgraph" and "superchic" are supported. Exiting.')
        sys.exit()

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

