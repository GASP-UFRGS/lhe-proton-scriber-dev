def write_protons(_event,_sign,_generator,_id1,_id2,_px,_py,_pzp,_en,_mass):
    '''
    Writes the protons into an LHE file from MadGraph or Superchic 
    '''
    # check position reference
    _ppos = _event.index('<mgrwt>\n')
    # inser lines
    if _generator == 'superchic':
        if _sign > 0: _event.insert(_ppos, ' '*13+f'2212{" "*8}1    0    0    0    0 {_px} {_py} +{_pzp:.9e}  {ep:.9e}  {m0:.9e} 0. 1.\n')
        else: _event.insert(_ppos, ' '*13+f'{2212}{" "*8}1    0    0    0    0 {_px} {_py} {_pzp:.9e}  {ep:.9e}  {m0:.9e} 0. -1.\n')
    if _generator == 'madgraph':
        if _sign > 0: _event.insert(_ppos, ' '*5+f'{_id1}{" "*2}1    0    0    0    0 +{0:.10e} +{0:.10e} +{_pzp:.10e}{" "*1}{_en:.10e}{" "*1}{_mass:.10e} {0:.4e} {1:.4e}\n')
        else: _event.insert(_ppos, ' '*5+f'{_id2}{" "*2}1    0    0    0    0 -{0:.10e} -{0:.10e} {_pzp:.10e}{" "*1}{_en:.10e}{" "*1}{_mass:.10e} {0:.4e} {-1:.4e}\n')
    # the 6th number is the xi, while px = py = m0 = 0, and spin/helicity = 9 for identification as a pileup proton
    return _event
