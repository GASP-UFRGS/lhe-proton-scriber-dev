import random
import numpy as np

def draw():
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
    # Split the second element of the list into parts based on spaces
    second_element = _event[1].split()
    # Convert the first part to an integer, add _i, and update the list
    first_number = int(second_element[0])
    updated_number = first_number + _i
    # Replace the first number with the updated number
    second_element[0] = str(updated_number)
    # Join the modified parts back into a string
    _event[1] = ' '.join(second_element) + '\n'
    return _event

def fill_puprotons(_event,_generator,_pzinip,_pzinim,_m0,_id1,_id2):
    i=0
    _pu_protons = draw()
    _pupos = _event.index('<mgrwt>\n')
    for _xi in _pu_protons[0]:
        if _generator == 'superchic':
            _event.insert(_pupos, ' '*13+f'2212{" "*8}1    0    0    0    0 {0:.9e} {0:.9e} +{(1-_xi)*_pzinip:.9e}  {(1-_xi)*_pzinip:.9e}  {0:.9e} 0. 9.\n')
        if _generator == 'madgraph':
            _event.insert(_pupos,' '*5+f'{_id1}{" "*2}1    0    0    0    0 +{0:.10e} +{0:.10e} +{(1-_xi)*_pzinip:.10e}{" "*1}{(1-_xi)*_pzinip:.10e}{" "*1}{_m0:.10e} {0:.4e} {9:.4e}\n')
    for _xi in _pu_protons[1]:
        if _generator == 'superchic':
            _event.insert(_pupos,' '*13+f'2212{" "*8}1    0    0    0    0 {0:.9e} {0:.9e} -{(1-_xi)*_pzinim:.9e}  {(1-_xi)*_pzinim:.9e}  {0:.9e} 0. 9.\n')
        if _generator == 'madgraph':
            _event.insert(_pupos,' '*5+f'{_id2}{" "*2}1    0    0    0    0 +{0:.10e} +{0:.10e} -{(1-_xi)*_pzinim:.10e}{" "*1}{(1-_xi)*_pzinim:.10e}{" "*1}{_m0:.10e} {0:.4e} {9:.4e}\n')
    _event = update_event(_event, int(len(_pu_protons[0])+len(_pu_protons[1])))
    return _event
