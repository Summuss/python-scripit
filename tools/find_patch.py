import subprocess
import argparse
import re


def find_patch(regex, path, table, ddl, edit_flag):
    if not path:
        path = '/home/summus/Work/patches'

    subprocess.run(['svn', 'update', path])
    code, result = subprocess.getstatusoutput(f"grep -i '{regex}' {path}/*")
    if code != 0:
        print("not found")
        exit(-1)
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
    if len(file_name_list) == 0:
        print("not found")
        exit(-1)

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

    if len(file_name_list) == 0:
        print("not found")
        exit(-1)

    print('\n############################################################\n')
    for i, v in enumerate(file_name_list):
        print(f"{i + 1}:{v}")
    print('\n############################################################\n')

    if edit_flag:
        for file_name in file_name_list:
            subprocess.run(['gedit', file_name])
    else:
        while True:
            num = int(input(f"input the sequence number of file to be edited(0~{len(file_name_list)}):"))
            if num == 0:
                break
            elif 0 < num <= len(file_name_list):
                subprocess.run(['gedit', file_name_list[num - 1]])
                print('\n############################################################\n')
                for i, v in enumerate(file_name_list):
                    print(f"{i + 1}:{v}")
                print('\n############################################################\n')

            else:
                print("输入不合法")
                print('\n############################################################\n')
                for i, v in enumerate(file_name_list):
                    print(f"{i + 1}:{v}")
                print('\n############################################################\n')


def get_file_path_from_grep_result(grep_result):
    return list(set(re.findall(r"^.*?(/.+?\.sql).*", grep_result, flags=re.M)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="find patch")
    parser.add_argument("regex", type=str, help='regex pattern')
    parser.add_argument("-t", "--table", type=str, help='table name')
    parser.add_argument("-p", "--path", type=str, help="patch folder's path")
    parser.add_argument("-d", "--ddl", type=str, help='ddl type')
    parser.add_argument("-e", "--edit", action="store_true")

    args = parser.parse_args()
    find_patch(args.regex, args.path, args.table, args.ddl, args.edit)
