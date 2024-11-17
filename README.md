# Proton Scriber

## Overview

**Proton Scriber** is a Python script designed to process **LHE (Les Houches Event)** files and add pileup protons or modify event properties based on user-specified inputs. It is compatible with event generators like **MadGraph** and **SuperChic** and provides flexibility in configuring input files, options, and output files. The script supports both command-line arguments and a configuration file (e.g. `input.dat`).

---

## Features

- Process LHE files to update event information.
- Add pileup protons to events.
- Specify PDG IDs for kinematic processing.
- Flexible input handling through command-line arguments or a configuration file.

---

## Input Parameters

### Command-line Options

- `-i` or `--inputfile`:  
  Path to the input LHE file (e.g., `./events.lhe`).

- `-mc` or `--generator`:  
  The generator type used to create the LHE file. Supported values: `madgraph` or `superchic`.

- `--tag`:  
  A prefix to be added to the output filename (e.g., `output_prefix`).

- `-pu` or `--pileup`:  
  Option to include pileup protons in the events. Accepts `True` or `False`.

- `--ids`:  
  Space-separated PDG IDs for particles defining the kinematics of scattered protons.  
  Example: `"22 22"`.

### Using a Configuration File (`input.dat`)

You can provide inputs via a `input.dat` file. Example format:

```dat
[input]
inputfile = ./events.lhe
generator = madgraph
tag = output_prefix
pileup = True
ids = 22 22
```

If a configuration file is provided, command-line arguments will take precedence over the values in the file.

### How to Run

#### Option 1: Using Command-line Arguments

Run the script with the required arguments:

```
python3 proton_scriber.py -i ./events.lhe -mc madgraph --tag output_prefix -pu True --ids "22 22"
```

#### Option 2: Using a Configuration File

1.	Create a file, e.g. input.dat,  with the necessary options, as shown in the example above.
2.	Run the script without specifying arguments:

```
python3 proton_scriber.py -c input.dat
```

#### Option 3: Combining Command-line and Configuration File

You can use a combination of command-line arguments and a configuration file. Command-line arguments will override the values specified in the configuration file.

### Dependencies

This script requires the Python libraries list in the requirements.txt:

Install the dependencies using pip:

```
pip install numpy
```

### Notes

1.	Ensure the input LHE file exists at the specified path.
2.	The generator type must be either madgraph or superchic; otherwise, the script will raise an error.
3.	If fewer than six arguments are provided or required arguments are missing, the script will display the syntax guide and exit.

### Syntax Guide

Run the following command to display the syntax guide:

```
python3 proton_scriber.py --help
```

You will see detailed information about all the options and their usage.

### Example Use Cases

#### Example 1: Minimal Input

```
python3 proton_scriber.py -i ./events.lhe -mc madgraph --tag my_output
```

#### Example 2: With Pileup and IDs

```
python3 proton_scriber.py -i ./events.lhe -mc superchic --tag output_with_pileup -pu True --ids "22 22"
```

#### Example 3: Using Configuration File Only

```
python3 proton_scriber.py -c input.dat
```

### License

This project is licensed under the MIT License. See the LICENSE file for details.




