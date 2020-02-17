# Photogrammetry (CIVE6397): Lab #1

## Description
Command line interface (CLI) application for determining the parameters necessary to transform image comparator measurements into the fiducial system. Similarity, affine, and projective transformations are supported.

## Installation
- Clone this repository with `git clone git@github.com:pjhartzell/photo-lab1.git`.
- Use the `lab1.yml` file to create a new environment with all the required dependencies: `conda env create -f lab1.yml.`
- Install the CLI with `pip install .` from within the `photo-lab1` directory.

## Usage
- The CLI application is called `transform`. It will print parameters and residuals to the terminal and will plot the residuals.
- There are three required positional arguments
    1. Type of transform: 's' for similarity, 'a' for affine, 'p' for projective
    2. File of known fiducial coordinates
    3. File of measured (observed) fiducial coordinates
- Example: `transform 'a' .\data\dec_1_027-known.txt .\data\dec_1_027-observed.txt`

## Lab Report
See [report.md](./report/report.md) in the [report](./report) directory.