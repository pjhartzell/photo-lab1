from .argument_parser import get_arguments
from .transform import Transform

def main():
    # Get arguments from command line; use -h for help
    args = get_arguments()

    # Create a Transform object
    my_transform = Transform()

    # Import known and observed fiducial coordinates
    my_transform.import_known(args.known)
    my_transform.import_observed(args.observed)

    # Apply user defined transformation
    my_transform.transform(args.transform)

    # Print results to command line
    my_transform.print_results()

    # Show quiver plot of residuals
    my_transform.show_quiver()