# Photogrammetry (CIVE6397): Lab #1

## Description
Command line interface (CLI) application to determine the parameters necessary to transform image comparator measurements into the fidcial system. Similarity, affine, and projective transformations are supported

## Installation
- Clone this repository: `git clone git@github.com:pjhartzell/photo-class.git` or `git clone https://github.com/pjhartzell/photo-class.git`. Note that this is the entire repo for the class, not just each lab assignment ()
I use Conda for my Python environments. Use the gpiv.yml file to create a new environment with all the required dependencies: conda env create -f gpiv.yml.
Run pip install . from within the gpiv directory to install GPIV.
Type gpiv --help to see available commands and options. Type gpiv piv --help for PIV arguments and options and gpiv pivshow --help for arguments and options for plotting the PIV results.