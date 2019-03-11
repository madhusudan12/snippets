import datetime
import os
import argparse
today = datetime.datetime.today()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output-folder",
                        dest="output_folder",
                        default="/duta/server/dutaweb/content/{0}/{1}/{2}/".format(today.year, today.month, today.day),
                        help="Folder to which we have to write article markdown files")
    args = parser.parse_args()
    print(args.output_folder)

    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)
        print("created directory")




if __name__ == '__main__':
    t=datetime.datetime.today()
    print(t.month)
    print(t.year)
    print(t.day)
    main()