import os
from tqdm import tqdm

import fill_protons
import checkers
import setters

if __name__ == "__main__":
    # Gather input info
    inputs = checkers.parse_args()
    # Set proton mass
    m0 = setters.set_proton_mass()
    # Set info
    outputfile = inputs["tag"]+"_"+inputs["inputfile"]
    kinematics = setters.set_energy(inputs["inputfile"],inputs["generator"])
    # Start event processing
    event = []
    ofile = open(outputfile, 'w')
    with open(inputs["inputfile"], 'r+') as ifile:
        total_lines = checkers.num_lines(os.path.basename(ifile.name))
        total_events = checkers.count_events_in_lhe(os.path.basename(ifile.name))
        with tqdm(total=total_events, desc="Processing events") as pbar:
            for index, line in enumerate(ifile):
                while line != kinematics["endfile"]:
                    line = ifile.readline()
                    if line == kinematics["evi"]:
                        event.append(line)
                        while line.strip() != kinematics["evf"].strip():
                            line = ifile.readline()
                            event.append(line)
                        for i in range(len(event)):
                            if event[i].split()[0] in inputs["ids"] and event[i].split()[1] == '-1':
                                # Updating number of particles on header
                                neweventheader = event[1].split()
                                event = checkers.check_header(event,neweventheader,inputs["generator"])
                                # Creating the 4-momentum vector
                                line = event[i].split()
                                fourv = {}
                                fourv["mass"] = m0
                                fourv["px"] = f'{-eval(line[6]):.9e}' if -eval(line[6]) < 0 else f'+{-eval(line[6]):.9e}'
                                fourv["py"] = f'{-eval(line[7]):.9e}' if -eval(line[7]) < 0 else f'+{-eval(line[7]):.9e}'
                                pzf = eval(line[8])
                                ef = eval(line[9])
                                # Check proton direction via pz sign
                                sign = (pzf/abs(pzf))
                                if sign > 0:
                                    fourv["pzproton"] = kinematics["pzini_plus"]*sign - pzf
                                    fourv["eproton"] = kinematics["ebeam_plus"] - ef
                                else:
                                    fourv["pzproton"] = kinematics["pzini_minus"]*sign - pzf
                                    fourv["eproton"] = kinematics["ebeam_minus"] - ef
                                # Add protons to the output file if IDs given
                                event = fill_protons.add_signal(
                                                                event,
                                                                sign,
                                                                inputs["generator"],
                                                                kinematics["idp1"],
                                                                kinematics["idp2"],
                                                                fourv,
                                                               )
                        # Check and adds pileup
                        if (inputs["pileup"] == 'true' or inputs["pileup"] == "True"):
                            event = fill_protons.add_pileup(
                                                            event,
                                                            inputs["generator"],
                                                            kinematics["idp1"],
                                                            kinematics["idp2"],
                                                            kinematics["pzini_plus"],
                                                            kinematics["pzini_minus"],
                                                            m0
                                                           )
                        for newline in event:
                            # Write new event to output file
                            ofile.write(newline)
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

