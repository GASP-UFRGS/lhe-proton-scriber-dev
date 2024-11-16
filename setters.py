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
        _lines = _f.readlines()
        _index = _lines.index(_header)
        _line = _lines[_index+1].split()
        _ebeam_plus  = float(_line[2])
        _ebeam_minus = float(_line[3])
        if _generator == "madgraph":
            _ionline1 = [_ion1 for _ion1 in _lines if "nb_proton1" in _ion1]
            _zion1 = _ionline1[0].split()[0]
            _ionline2 = [_ion2 for _ion2 in _lines if "nb_proton2" in _ion2]
            _zion2 = _ionline2[0].split()[0]
            _idp1 = 2212 if int(_zion1) == 1 else 92212
            _idp2 = 2212 if int(_zion2) == 1 else 92212
            if int(_zion1) > 1 or int(_zion2) > 1:
                print("This is a proton-ion collision")
            if int(_zion1) >1 and int(_zion2) > 1:
                print("This is a ion-ion collision")

    return {
            "endfile": _end,
            "evi": _flag0,
            "evf": _flag1,
            "ebeam_plus": _ebeam_plus,
            "ebeam_minus": _ebeam_minus,
            "pzini_plus": _ebeam_plus,
            "pzini_minus": _ebeam_minus,
            "idp1": _idp1,
            "idp2": _idp2
           }

def set_proton_mass():
    # Get the proton mass in kg
    _proton_mass_kg = physical_constants['proton mass'][0]
    # Convert to GeV using E = mc^2, 1 eV = 1.602176634e-19 Joules
    _proton_mass_GeV = (_proton_mass_kg * c**2) / eV / giga
    print(f"Proton mass in GeV: {_proton_mass_GeV:.6f} GeV")
    return _proton_mass_GeV

