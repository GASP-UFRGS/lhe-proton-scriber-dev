def write_protons(_event,_sign,_generator,_id1,_id2,_fourv):
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
