import subprocess
import argparse
import re


def find_patch(regex, path, table, ddl):
    if not path:
        path = '/home/summus/Work/patches'

    subprocess.run(['svn', 'update', path],stdout=subprocess.PIPE)
    result = subprocess.run(f"grep -i '{regex}' {path}/*", check=True, shell=True,
                            stdout=subprocess.PIPE).stdout.decode(
        'utf-8')
    file_name_list = get_file_path_from_grep_result(result)
    if table:
        filtered_file_name_list = []

        for file_name in file_name_list:
            r = subprocess.run(
                r"grep -i '\([^a-z_]\|[^A-Z_]\|^\)" + table + r"\([^a-z_]\|[^A-Z_]\|$\)' '" + file_name + "'",
                shell=True,
                stdout=subprocess.PIPE)
            if r.returncode == 0:
                result = r.stdout.decode('utf-8')
                filtered_file_name_list.append(file_name)
        file_name_list = filtered_file_name_list

    if ddl:
        filtered_file_name_list = []

        for file_name in file_name_list:
            r = subprocess.run(
                r"grep -i '\([^a-z_]\|[^A-Z_]\|^\)" + ddl + r"\([^a-z_]\|[^A-Z_]\|$\)' '" + file_name + "'",
                shell=True,
                stdout=subprocess.PIPE)
            if r.returncode == 0:
                result = r.stdout.decode('utf-8')
                filtered_file_name_list.append(file_name)
        file_name_list = filtered_file_name_list

    print('\n'.join(file_name_list))


pass


def get_file_path_from_grep_result(grep_result):
    return list(set(re.findall(r"^.*?(/.+?\.sql).*", grep_result, flags=re.M)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="find patch")
    parser.add_argument("regex", type=str, help='regex pattern')
    parser.add_argument("-t", "--table", type=str, help='table name')
    parser.add_argument("-p", "--path", type=str, help="patch folder's path")
    parser.add_argument("-d", "--ddl", type=str, help='ddl type')

    args = parser.parse_args()
    find_patch(args.regex, args.path, args.table, args.ddl)
