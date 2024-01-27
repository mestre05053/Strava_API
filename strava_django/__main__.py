import sys
from strava_django.app import User_Data

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    app = User_Data()

if __name__ == '__main__':
    sys.exit(main())