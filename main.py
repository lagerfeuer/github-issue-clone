#!/usr/bin/env python3

from argparse import ArgumentParser
from github import Github


def _parse_args():
  parser = ArgumentParser(description='Github Issue Clone')
  parser.add_argument('--token', help='Github access token', required=True)
  parser.add_argument('--from', dest='repo_from',
                      help='Repository of the original issues', required=True)
  parser.add_argument('--to', dest='repo_to',
                      help='New repository for the issues', required=True)
  parser.add_argument('issues', metavar='ISSUE', type=int, nargs='*',
                      help='Specify issue numbers, only these will be cloned')
  parser.add_argument('--dry-run', action='store_true', default=False,
                      help='Perform a dry run, do create issues')
  args = parser.parse_args()
  return args


# TODO: filtering
# allow filtering by issue numbers
def clone(gh, origin, copy, issue_numbers, dry_run):
  issues = gh.get_repo(origin).get_issues()
  repo_copy = gh.get_repo(copy)
  for issue in sorted(issues, key=lambda issue: issue.number):
    print(f"Cloning issue #{issue.number}...")
    title, body = issue.title, issue.body
    body += f"\n\n___\nThis issue has been cloned from: https://github.com/{origin}/issues/{issue.number}"
    if not dry_run:
      repo_copy.create_issue(title=title, body=body) 


def main():
  args = _parse_args()
  gh = Github(args.token)
  if args.dry_run:
    print("* Running with --dry-run, no changes will be performed.")
  clone(gh, args.repo_from, args.repo_to, args.issues, args.dry_run)


if __name__ == '__main__':
  main()
