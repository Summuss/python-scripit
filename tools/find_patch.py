import subprocess
import argparse


def find_patch(regex, path, table, dll):
    if path:
        path = '/home/summus/Work/patches'

    if dll:
        regex = f'{dll}.*{regex}'

    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="find patch")
    parser.add_argument("regex", type=str, help='regex pattern')
    parser.add_argument("-t", "--table", type=str, help='table name')
    parser.add_argument("-p", "--path", type=str, help="patch folder's path")
    parser.add_argument("-d", "--ddl", type=str, help='ddl type')

    args = parser.parse_args()
    find_patch(args.regex, args.path, args.table, args.ddl)
