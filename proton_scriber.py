import sys
import os
from tqdm import tqdm
from ROOT import TLorentzVector 

import fill_pileup
import checkers
import setters

'''
Writes the protons into an LHE file from MadGraph or Superchic 
'''

def write_protons(_event,_sign,_generator):
    if _generator == 'superchic':
        if _sign > 0: _event.insert(i+1, ' '*13+f'2212{" "*8}1    0    0    0    0 {px} {py} +{pzp:.9e}  {ep:.9e}  {m0:.9e} 0. 1.\n')
        else: _event.insert(i+1, ' '*13+f'2212{" "*8}1    0    0    0    0 {px} {py} {pzp:.9e}  {ep:.9e}  {m0:.9e} 0. -1.\n')
    if _generator == 'madgraph':
        if _sign > 0: _event.insert(i+1, ' '*5+f'2212{" "*2}1    0    0    0    0 +{0:.11e} +{0:.11e} +{pzp:.11e}{" "*2}{ep:.11e}{" "*2}{m0:.11e} {0:.4e} {1:.4e}\n')
        else: _event.insert(i+1, ' '*5+f'2212{" "*2}1    0    0    0    0 -{0:.11e} -{0:.11e} {pzp:.11e}{" "*2}{ep:.11e}{" "*2}{m0:.11e} {0:.4e} {-1:.4e}\n')
    # the 6th number is the xi, while px = py = m0 = 0, and spin/helicity = 9 for identification as a pileup proton

if __name__ == "__main__":
    # Set proton mass
    m0 = setters.set_proton_mass()
    # Collect args
    inputfile = sys.argv[1]
    generator = sys.argv[2].lower()
    pileup = sys.argv[3]
    ID = sys.argv[4:]
    # Gather definitions
    outputfile = 'new_'+inputfile
    printinvm = checkers.check_args(generator)
    end,flag0,flag1,header,pzini,eini = setters.set_energy(inputfile,generator)
    # Start event processing
    event = []
    ofile = open(outputfile, 'w')
    with open(inputfile, 'r+') as ifile:
        total_lines = checkers.num_lines(os.path.basename(ifile.name))
        total_events = checkers.count_events_in_lhe(os.path.basename(ifile.name))
        with tqdm(total=total_events, desc="Processing events") as pbar:
            for index, line in enumerate(ifile):
                while line != end:
                    line = ifile.readline()
                    if line == flag0:
                        event.append(line)
                        while line.strip() != flag1.strip():
                            line = ifile.readline()
                            event.append(line)
                        for i in range(len(event)):
                            if event[i].split()[0] in ID and event[i].split()[1] == '-1':
                                # Updating number of particles on header
                                neweventheader = event[1].split()
                                event = checkers.check_header(event,neweventheader,generator)
                                # Creating the 4-momentum vector
                                line = event[i].split()
                                px = f'{-eval(line[6]):.9e}' if -eval(line[6]) < 0 else f'+{-eval(line[6]):.9e}'
                                py = f'{-eval(line[7]):.9e}' if -eval(line[7]) < 0 else f'+{-eval(line[7]):.9e}'
                                pzf = eval(line[8])
                                # Check proton direction via pz sign
                                sign = (pzf/abs(pzf))
                                pzp = pzini*sign - pzf
                                ef = eval(line[9])
                                ep = eini - ef
                                # Add protons to the output file
                                write_protons(event,sign,generator)
                                # Check and adds pileup
                                if (pileup == 'true' or pileup == "True"):
                                    event = fill_pileup.fill_puprotons(i,event,generator,pzini,m0)
                        for nl in event:
                            # Write new event to output file
                            ofile.write(nl)
                        # Clean event list for next iteration
                        event.clear()
                        pbar.update(1)
                    else:
                        # Write line if simple copy
                        ofile.write(line)

# Closing files:
ifile.close()
ofile.close()
print("File "+outputfile+" created")

