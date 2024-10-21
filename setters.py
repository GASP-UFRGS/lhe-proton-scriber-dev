from scipy.constants import physical_constants, giga, c, eV

def set_energy(_inputfile,_generator):
    # Setting flags according to chosen generator
    if (_generator == 'madgraph'):
        _flag0 = '<event>\n'
        _flag1 = '</event>\n'
        _header = '<init>\n'
        _end = '</LesHouchesEvents>\n'
    if (_generator == 'superchic'):
        _flag0 = ' <event>\n'
        _flag1 = ' </event>\n'
        _header = ' <init>\n'
        _end = ' </LesHouchesEvents>\n'
    # Create list of lines from the LHE file and if needed finding the beginning of events 
    with open(_inputfile, 'r+') as _f:
        _line = _f.readline()
        while _line != _header:
            _line = _f.readline()
        _beamenergy = int(float(_f.readline().split()[2]))
    # Set energies:
    _pzini = _beamenergy    # protons inicial pz 
    _eini = _beamenergy     # protons inicial energy

    return _end,_flag0,_flag1,_header,_pzini,_eini

def set_proton_mass():
    # Get the proton mass in kg
    _proton_mass_kg = physical_constants['proton mass'][0]
    # Convert to GeV using E = mc^2, 1 eV = 1.602176634e-19 Joules
    _proton_mass_GeV = (_proton_mass_kg * c**2) / eV / giga
    print(f"Proton mass in GeV: {_proton_mass_GeV:.6f} GeV")
    return _proton_mass_GeV

