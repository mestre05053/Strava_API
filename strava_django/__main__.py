import sys

from strava_django.app import run

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    app = run()

if __name__ == '__main__':
    sys.exit(main())