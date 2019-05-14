import argparse








if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '-d',
        '--day',
        dest='day',
        action="store",
        default=None,
        help='day for which more counts updation needs to run')
    parser.add_argument(
        '-f',
        '--full run',
        dest="flag",
        action="store_true",
        default=False,
        help='run updating table also if this is set true'
    )
    args = parser.parse_args()
    print(args.day)
    print(args.flag)