import sys

from strava_django.app import test

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    app = test()

if __name__ == '__main__':
    sys.exit(main())