import argparse
import re
import sh
from sh import git
from sh import ErrorReturnCode
import subprocess


def push(remote_name, remote_branch, to_be_pushed_branch, commit_hash_list):
    git.status()
    current_branch = get_stdout(git('symbolic-ref', '--short', '-q', 'HEAD'))[0:-1]
    mark_message = '***mark***'

    # 校验是否tag已存在
    tag_name = f"merging({current_branch}-->{remote_name}/{remote_branch})"
    code, output = subprocess.getstatusoutput(f"git tag | grep '^{tag_name}$'")
    if code == 0:
        print(f"错误，tag:{tag_name} 已存在")
        exit(-1)

    # 校验远程分支是否存在
    code, output = subprocess.getstatusoutput('git fetch')
    if code != 0:
        print(output)
        print("fetch 失败")
        exit(-1)

    code, output = subprocess.getstatusoutput(
        f"git branch -r | cat | grep '^ *{remote_name}/{remote_branch}'")
    if code != 0:
        print("错误，远程分支%s不存在" % remote_branch)
        exit(-1)

    # 如果工作区不干净，mark提交
    res = git.status()
    is_clean = re.match(".*nothing to commit, working tree clean.*", get_stdout(res), re.S)
    if not is_clean:
        print('工作区不干净，mark提交...')
        git.add('--all')
        git.commit('-a', '-m', mark_message)

    # 检出到远程临时分支
    tmp_branch = f'tmp/local_{remote_name}_{remote_branch}'
    print(f'检出到远程临时分支"{tmp_branch}"...')
    git.checkout('-b', tmp_branch, f'{remote_name}/{remote_branch}')

    # cherry-pick
    try:
        print('开始cherry-pick...')
        res = git('cherry-pick', commit_hash_list)
    except sh.ErrorReturnCode_1:
        print(get_stderr(res))
        print("请解决冲突,然后选择后续操作...")
        while True:
            operation = input('请输入处理方式')
            if operation == 0:
                print('execute: git cherry-pick --continue...')
                code, output = subprocess.getstatusoutput('git cherry-pick --continue')
                print(output)
                if code != 0:
                    continue
                else:
                    print('解决冲突成功')
                    break
            elif operation == 1:
                print('退出，停在当前位置')
                git('check-pick', '--abort')
                exit(-1)
            elif operation == 2:
                print('撤销，回到起点...')
                git('check-pick', '--abort')
                # 切换会原来的分支，并去掉mark提交
                git.switch(current_branch)
                git.branch('-D', tmp_branch)
                de_mark_commit(current_branch, mark_message)
                exit(-1)
            else:
                print('输入不合法，请重新输入')
    except ErrorReturnCode:
        print(get_stderr(res))
        exit(-1)

    print('推送中...')
    git.push('-f', remote_name, f'HEAD:{to_be_pushed_branch}')

    # 切换会原来的分支，并去掉mark提交
    print('切换会原来的分支，并去掉mark提交')
    git.switch(current_branch)
    git.branch('-D', tmp_branch)
    de_mark_commit(current_branch, mark_message)

    print(f'添加tag"{tag_name}"...')
    git.tag('-a', tag_name, '-m', "nothing")
    print('完成！')


def de_mark_commit(current_branch, mark_message):
    code, output = subprocess.getstatusoutput(f'git log -1 --pretty=format:"%s" {current_branch}')
    if code == 0:
        if output == mark_message:
            git.reset('HEAD~')
    else:
        print("查看commit message出错！")
        exit(-1)


def get_stderr(res):
    return str(res.stderr, encoding='utf-8')


def get_stdout(res):
    return str(res.stdout, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="git push")
    parser.add_argument("remote_branch", type=str, help='origin_branch')
    parser.add_argument("to_be_pushed_branch", type=str)
    parser.add_argument("commit_hash_list", type=str, nargs='+', help='commit hash list')
    args = parser.parse_args()
    push("origin", args.remote_branch, args.to_be_pushed_branch, args.commit_hash_list)
