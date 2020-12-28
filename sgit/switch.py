import argparse
import re
from sh import git
from sh import ErrorReturnCode
import subprocess


def switch(target_branch):
    mark_message = '***mark***'
    try:
        res = git.status()
    except ErrorReturnCode:
        print(get_stderr(res))
        print('失败！该文件夹没有初始化')
        exit(-1)
    is_clean = re.match(".*nothing to commit, working tree clean.*", get_stdout(res), re.S)
    if not is_clean:
        print('工作区不干净，mark提交...')
        git.add('--all')
        git.commit('-a', '-m', mark_message)
    git.switch(target_branch)

    code, output = subprocess.getstatusoutput('git log -1 --pretty=format:"%s" ' + target_branch)
    if code == 0:
        if output == mark_message:
            git.reset('HEAD~')
    else:
        print("查看commit message出错！")
        exit(-1)
    print('切换到%s' % target_branch)


def get_stderr(res):
    return str(res.stderr, encoding='utf-8')


def get_stdout(res):
    return str(res.stdout, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="git switch")
    parser.add_argument("target_branch", type=str, help='branch to be switched')
    args = parser.parse_args()
    switch(args.target_branch)
