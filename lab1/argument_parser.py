import argparse

def get_arguments():
    # Set up an argument parser to collect input from the command line
    parser =argparse.ArgumentParser(description="Solve the transformation "
        "between given and measured fiducial marks")

    # User must enter a transformation type
    parser.add_argument(
        "transform",
        choices={"s", "a", "p"},
        help="type of transform: similarity = 's', affine = 'a', "
            "projective = 'p'"
    )

    # User must enter text file locations for known and observed coordinates
    parser.add_argument(
        "known",
        type=str,
        help="text file of known fiducial coordinates"
    )
    parser.add_argument(
        "observed",
        type=str,
        help="text file of observed fiducial coordinates"
    )

    return parser.parse_args()