from timelapse_eq.directory import Directory
from timelapse_eq.timelapse import TimeLapse
from colorama import Fore
import argparse
import sys
import os


parser = argparse.ArgumentParser()

parser.add_argument("directory")
parser.add_argument(
    "--width",
    help="set width of output photos",
    type=int
)
parser.add_argument(
    "--start",
    help="set a different starting photo for ev changes",
    action="store_true"
)
parser.add_argument(
    "--auto_wb",
    help="apply auto white balance to photos",
    action="store_true"
)

args = parser.parse_args()


def main():
    chosen_directory = os.path.abspath(args.directory)
    directory = Directory(chosen_directory)

    if not directory.exists():
        print(
            Fore.GREEN + chosen_directory + Fore.WHITE + " is " +
            Fore.RED + "not" + Fore.WHITE + " a valid directory."
        )
        sys.exit(0)

    directory.find_photos()
    directory.sort_photos()

    if not directory.has_valid_photos():
        print(
            "Directory " + Fore.GREEN + chosen_directory + Fore.WHITE + " does " +
            Fore.RED + "not" + Fore.WHITE + " have any valid photos."
        )
        sys.exit(0)

    directory.make_output_dir()

    timelapse = TimeLapse(directory.valid_photos)
    timelapse.make_photos()

    timelapse.determine_exposure_change_points(args.start)
    timelapse.determine_necessary_exposure_changes()
    timelapse.update_photos()
    timelapse.save_photos(args)


if __name__ == "__main__":
    main()
