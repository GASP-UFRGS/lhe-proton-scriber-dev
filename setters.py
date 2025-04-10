from scipy.constants import physical_constants, giga, c, eV
import re

def set_energy(_inputfile, _generator):
    # Setting flags according to chosen generator
    if _generator == 'madgraph':
        _flag0 = '<event>\n'
        _flag1 = '</event>\n'
        _header = '<init>\n'
        _end = '</LesHouchesEvents>\n'
    elif _generator == 'superchic':
        _flag0 = ' <event>\n'
        _flag1 = ' </event>\n'
        _header = ' <init>\n'
        _end = ' </LesHouchesEvents>\n'
    else:
        raise ValueError("Unsupported generator type")

    with open(_inputfile, 'r') as _f:
        _lines = _f.readlines()
        _index = _lines.index(_header)
        _line = _lines[_index + 1].split()
        _ebeam_plus = float(_line[2])
        _ebeam_minus = float(_line[3])

        _idp1, _idp2 = None, None

        if _generator == "madgraph":
            # Proton-ion detection via MadGraph tags
            if any("nb_proton" in line for line in _lines):
                _zion1 = int([line for line in _lines if "nb_proton1" in line][0].split()[0])
                _zion2 = int([line for line in _lines if "nb_proton2" in line][0].split()[0])
                _idp1 = 2212 if _zion1 == 1 else 92212
                _idp2 = 2212 if _zion2 == 1 else 92212
                if _zion1 > 1 or _zion2 > 1:
                    print("This is a proton-ion collision")
                if _zion1 > 1 and _zion2 > 1:
                    print("This is an ion-ion collision")
            else:
                # lpp1/lpp2 style detection
                beam_type_map = {
                    1:    (2212, "proton"),
                    -1:   (-2212, "antiproton"),
                    2:    (22, "elastic photon"),
                    3:    (11, "electron"),
                    -3:   (-11, "positron"),
                    4:    (13, "muon"),
                    -4:   (-13, "antimuon"),
                    5:    (9000001, "elastic scalar"),
                    0:    (0, "no beam / external")
                }

                _idbeam1, _idbeam2 = None, None
                pattern = re.compile(r"^\s*(\-?\d+)\s*=\s*(lpp1|lpp2)")

                for line in _lines:
                    match = pattern.match(line)
                    if match:
                        value = int(match.group(1))
                        beam = match.group(2)
                        if beam == "lpp1":
                            _idbeam1 = value
                        elif beam == "lpp2":
                            _idbeam2 = value

                if _idbeam1 is None or _idbeam2 is None:
                    raise ValueError("No incoming particles found in the input file!")

                if _idbeam1 in beam_type_map:
                    _idp1 = beam_type_map[_idbeam1][0]
                if _idbeam2 in beam_type_map:
                    _idp2 = beam_type_map[_idbeam2][0]

                if _idbeam1 in beam_type_map and _idbeam2 in beam_type_map:
                    name1 = beam_type_map[_idbeam1][1]
                    name2 = beam_type_map[_idbeam2][1]
                    print(f"This is a {name1}-{name2} collision")

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
    _proton_mass_kg = physical_constants['proton mass'][0]
    _proton_mass_GeV = (_proton_mass_kg * c**2) / eV / giga
    print(f"Proton mass in GeV: {_proton_mass_GeV:.6f} GeV")
    return _proton_mass_GeV
