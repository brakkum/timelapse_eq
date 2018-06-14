from directory import Dir
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    '--width',
    help='set width of output photos',
    type=int)
parser.add_argument(
    '--start',
    help='set a different starting photo for ev changes',
    action='store_true')
parser.add_argument(
    '--auto_wb',
    help='apply auto white balance to photos',
    action='store_true')

args = parser.parse_args()
print(args)


def main():
    path = input('Enter directory: ')
    Dir(path, args)


if __name__ == '__main__':
    main()
