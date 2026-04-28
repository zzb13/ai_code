#!/usr/bin/env python3
"""
GitHub 自动化助手 CLI

快速创建 PR、查看状态、自动化常见操作
"""

import argparse
import subprocess
import sys
import os


class GitHubAssistant:
    def __init__(self):
        self.check_auth()
    
    def check_auth(self):
        """检测 GitHub 认证方式"""
        try:
            result = subprocess.run(
                ['gh', 'auth', 'status'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.auth_method = 'gh'
                return
        except FileNotFoundError:
            pass
        
        if os.getenv('GITHUB_TOKEN'):
            self.auth_method = 'token'
        else:
            self.auth_method = 'none'
    
    def run_cmd(self, cmd, check=True):
        """运行 shell 命令"""
        print(f"▶️ {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if check and result.returncode != 0:
            print(f"❌ 命令失败: {result.stderr}")
            sys.exit(1)
        return result
    
    def create_pr(self, title, body, branch, base='main', draft=False):
        """创建 Pull Request"""
        print(f"📝 创建 PR: {title}")
        print(f"   分支: {branch} -> {base}")
        
        if self.auth_method == 'gh':
            cmd = [
                'gh', 'pr', 'create',
                '--title', title,
                '--body', body,
                '--base', base
            ]
            if draft:
                cmd.append('--draft')
            self.run_cmd(' '.join(cmd))
        else:
            print("❌ 需要 gh CLI 来创建 PR")
            sys.exit(1)
        
        print("✅ PR 创建成功")
    
    def list_prs(self, state='open'):
        """列出 Pull Requests"""
        print(f"📋 列出 {state} PRs...")
        
        if self.auth_method == 'gh':
            result = self.run_cmd('gh pr list --state ' + state)
            print(result.stdout)
        else:
            print("❌ 需要 gh CLI")
    
    def merge_pr(self, pr_number, method='squash'):
        """合并 PR"""
        print(f"🔀 合并 PR #{pr_number} ({method})")
        
        if self.auth_method == 'gh':
            cmd = f'gh pr merge {pr_number} --{method} --delete-branch'
            self.run_cmd(cmd)
            print("✅ PR 已合并")
        else:
            print("❌ 需要 gh CLI")
    
    def check_ci_status(self, pr_number=None):
        """检查 CI 状态"""
        print("🔍 检查 CI 状态...")
        
        if pr_number:
            cmd = f'gh pr checks {pr_number}'
        else:
            cmd = 'gh run list --limit 5'
        
        result = self.run_cmd(cmd)
        print(result.stdout)
    
    def review_pr(self, pr_number, action='comment', body=''):
        """审查 PR"""
        print(f"👀 审查 PR #{pr_number}: {action}")
        
        if self.auth_method == 'gh':
            cmd = f'gh pr review {pr_number} --{action}'
            if body:
                cmd += f' --body "{body}"'
            self.run_cmd(cmd)
            print("✅ 审查完成")
        else:
            print("❌ 需要 gh CLI")
    
    def create_branch(self, branch_name, base='main'):
        """创建新分支"""
        print(f"🌿 创建分支: {branch_name} (基于 {base})")
        
        # 更新主分支
        self.run_cmd('git fetch origin')
        self.run_cmd(f'git checkout {base}')
        self.run_cmd(f'git pull origin {base}')
        
        # 创建新分支
        self.run_cmd(f'git checkout -b {branch_name}')
        print(f"✅ 分支 {branch_name} 已创建")
    
    def commit_changes(self, message, test=False):
        """提交变更"""
        print("💾 提交变更...")
        
        # 检查是否有变更
        result = self.run_cmd('git status --short', check=False)
        if not result.stdout.strip():
            print("⚠️ 没有需要提交的变更")
            return
        
        # 运行测试（如果需要）
        if test:
            print("🧪 运行测试...")
            self.run_cmd('pytest', check=False)
        
        # 提交
        self.run_cmd('git add .')
        self.run_cmd(f'git commit -m "{message}"')
        print("✅ 变更已提交")
    
    def push_and_create_pr(self, title, body, base='main', draft=False):
        """推送并创建 PR（完整流程）"""
        # 获取当前分支
        result = self.run_cmd('git branch --show-current')
        branch = result.stdout.strip()
        
        print(f"🚀 推送分支: {branch}")
        self.run_cmd(f'git push -u origin {branch}')
        
        print("✅ 推送成功，创建 PR...")
        self.create_pr(title, body, branch, base, draft)


def main():
    parser = argparse.ArgumentParser(description='GitHub 自动化助手')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # pr create
    pr_create = subparsers.add_parser('pr', help='创建 PR')
    pr_create.add_argument('--title', required=True, help='PR 标题')
    pr_create.add_argument('--body', default='', help='PR 描述')
    pr_create.add_argument('--branch', help='分支名（默认当前分支）')
    pr_create.add_argument('--base', default='main', help='目标分支')
    pr_create.add_argument('--draft', action='store_true', help='创建草稿 PR')
    
    # pr list
    pr_list = subparsers.add_parser('list', help='列出 PRs')
    pr_list.add_argument('--state', default='open', help='状态 (open/closed/all)')
    
    # pr merge
    pr_merge = subparsers.add_parser('merge', help='合并 PR')
    pr_merge.add_argument('number', type=int, help='PR 编号')
    pr_merge.add_argument('--method', default='squash', choices=['merge', 'squash', 'rebase'])
    
    # check ci
    check_ci = subparsers.add_parser('ci', help='检查 CI 状态')
    check_ci.add_argument('--pr', type=int, help='PR 编号')
    
    # review
    review = subparsers.add_parser('review', help='审查 PR')
    review.add_argument('number', type=int, help='PR 编号')
    review.add_argument('--action', default='comment', choices=['approve', 'request-changes', 'comment'])
    review.add_argument('--body', default='', help='评论内容')
    
    # branch
    branch = subparsers.add_parser('branch', help='创建分支')
    branch.add_argument('name', help='分支名')
    branch.add_argument('--base', default='main', help='基础分支')
    
    # commit
    commit = subparsers.add_parser('commit', help='提交变更')
    commit.add_argument('message', help='提交信息')
    commit.add_argument('--test', action='store_true', help='提交前运行测试')
    
    # workflow
    workflow = subparsers.add_parser('workflow', help='完整工作流：推送并创建 PR')
    workflow.add_argument('--title', required=True, help='PR 标题')
    workflow.add_argument('--body', default='', help='PR 描述')
    workflow.add_argument('--base', default='main', help='目标分支')
    workflow.add_argument('--draft', action='store_true', help='创建草稿 PR')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    assistant = GitHubAssistant()
    
    if args.command == 'pr':
        branch = args.branch or subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True, text=True
        ).stdout.strip()
        assistant.create_pr(args.title, args.body, branch, args.base, args.draft)
    
    elif args.command == 'list':
        assistant.list_prs(args.state)
    
    elif args.command == 'merge':
        assistant.merge_pr(args.number, args.method)
    
    elif args.command == 'ci':
        assistant.check_ci_status(args.pr)
    
    elif args.command == 'review':
        assistant.review_pr(args.number, args.action, args.body)
    
    elif args.command == 'branch':
        assistant.create_branch(args.name, args.base)
    
    elif args.command == 'commit':
        assistant.commit_changes(args.message, args.test)
    
    elif args.command == 'workflow':
        assistant.push_and_create_pr(args.title, args.body, args.base, args.draft)


if __name__ == '__main__':
    main()
