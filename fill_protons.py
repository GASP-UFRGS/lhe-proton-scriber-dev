import random
import numpy as np

def add_signal(_event,_sign,_generator,_id1,_id2,_fourv):
    '''
    Writes the protons into an LHE file from MadGraph or Superchic 
    '''
    # check position reference
    _ppos = _event.index('<mgrwt>\n')
    # insert lines
    if _generator == 'superchic':
        if _sign > 0:
            _event.insert(
                _ppos,
                ' ' * 13 + f'2212{" " * 8}1    0    0    0    0 {_fourv["px"]} {_fourv["py"]} +{_fourv["pzproton"]:.9e}  {_fourv["eproton"]:.9e}  {m0:.9e} 0. 1.\n'
            )
        else:
            _event.insert(
                _ppos,
                ' ' * 13 + f'2212{" " * 8}1    0    0    0    0 {_fourv["px"]} {_fourv["py"]} {_fourv["pzproton"]:.9e}  {_fourv["eproton"]:.9e}  {m0:.9e} 0. -1.\n'
            )
    if _generator == 'madgraph':
        if _sign > 0:
            _event.insert(
                _ppos,
                f'{" " * (9 - len(str(_id1)))}{_id1}{" " * 2}1    0    0    0    0 +{0:.10e} +{0:.10e} +{_fourv["pzproton"]:.10e} {" "}{_fourv["eproton"]:.10e} {" "}{_fourv["mass"]:.10e} {0:.4e} {1:.4e}\n'
            )
        else:
            _event.insert(
                _ppos,
                f'{" " * (9 - len(str(_id2)))}{_id2}{" " * 2}1    0    0    0    0 -{0:.10e} -{0:.10e} {_fourv["pzproton"]:.10e} {" "}{_fourv["eproton"]:.10e} {" "}{_fourv["mass"]:.10e} {0:.4e} {-1:.4e}\n'
            )
    
    # The 6th number is the xi, while px = py = m0 = 0, and spin/helicity = 9 for identification as a pileup proton
    return _event

def draw_protons():
    # introduces pileup protons
    # the fractional momentum loss (xi) of the protons is assumed to follow a f(xi) = 1/xi distribution
    # minimum fractional momentum loss of scattered protons
    _xi_min = 0.015
    # maximum fractional momentum loss of scattered protons
    _xi_max = 0.200
    # mean for the gaussian blur
    _mu = 1
    # standard deviation for the gaussian blur, taken as 2%
    _sigma = 1
    # expected value of pileup events
    _mean_pileup = 5
    # store proton fraction momentum loss in a list
    _xi1_list = list()
    _xi2_list = list()
    # the number of pileup events is assumed to follow a poisson distribution
    _puEvents = np.random.poisson(_mean_pileup)
    for k in range(_puEvents):
        # sign of proton momentum along z axis
        _sign = np.random.uniform(-1,1,size=None)
        # random proton xi
        _randxi = _xi_min*pow(_xi_max/_xi_min, np.random.uniform(0,1,size=None))
        # random gauss probability
        _randgauss = random.gauss(_mu, _sigma)
        # fill proton lists
        _xi1_list.append(_randxi*_randgauss) if _sign < 0 else _xi2_list.append(_randxi*_randgauss)
    return [_xi1_list, _xi2_list]

def update_event(_event, _i):
    # split the second element of the list into parts based on spaces
    second_element = _event[1].split()
    # convert the first part to an integer, add _i, and update the list
    first_number = int(second_element[0])
    updated_number = first_number + _i
    # replace the first number with the updated number
    second_element[0] = str(updated_number)
    # join the modified parts back into a string
    _event[1] = ' '.join(second_element) + '\n'
    return _event

def add_pileup(_event,_generator,_id1,_id2,_pzinip,_pzinim,_m0):
    # get list of pileup protons
    _pu_protons = draw_protons()
    # find proper position to add protons
    _pupos = _event.index('<mgrwt>\n')
    for _xi in _pu_protons[0]:
        if _generator == 'superchic':
            _event.insert(
                _pupos,
                ' '*13+f'2212{" "*8}1    0    0    0    0 {0:.9e} {0:.9e} +{(1-_xi)*_pzinip:.9e}  {(1-_xi)*_pzinip:.9e}  {0:.9e} 0. 9.\n'
            )
        if _generator == 'madgraph':
            _event.insert(
                _pupos,
                f'{" " * (9 - len(str(_id1)))}{_id1}  1    0    0    0    0 +{0:.10e} +{0:.10e} +{(1-_xi)*_pzinip:.10e} {(1-_xi)*_pzinip:.10e} {_m0:.10e} {0:.4e} {9:.4e}\n',
            )
    for _xi in _pu_protons[1]:
        if _generator == 'superchic':
            _event.insert(
                _pupos,
                ' '*13+f'2212{" "*8}1    0    0    0    0 {0:.9e} {0:.9e} -{(1-_xi)*_pzinim:.9e}  {(1-_xi)*_pzinim:.9e}  {0:.9e} 0. 9.\n'
            )
        if _generator == 'madgraph':
            _event.insert(
                _pupos,
                f'{" " * (9 - len(str(_id2)))}{_id2}  1    0    0    0    0 +{0:.10e} +{0:.10e} -{(1-_xi)*_pzinim:.10e} {(1-_xi)*_pzinim:.10e} {_m0:.10e} {0:.4e} {9:.4e}\n',
            )
    _event = update_event(_event, int(len(_pu_protons[0])+len(_pu_protons[1])))

    return _event

