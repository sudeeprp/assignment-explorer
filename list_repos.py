from gsheet_assignments import GsheetAssignments
from github import Github
from buildlogs import coverage
from sys import argv
import argparse
import os


def collect_repos(githubapi, orgname):
  repos = []
  for repo in githubapi.get_organization(orgname).get_repos():
    print(repo.name, end=' ')
    print(repo.html_url, end='')
    print(str(repo.pushed_at))
    repos.append(repo)
  print(f'#Collected a total of {len(repos)} repositories')
  return repos


def repo_to_row(r):
  return {'repo': r.name, 'url': files_url(r.html_url), 'last update': str(r.pushed_at)}


def files_url(url):
  return url + '/pull/1/files'


def add_lastseen(row_content, org, repo, fetch_coverage):
  row_content['status'] = last_status(repo)
  if row_content['status'] == 'failure':
    row_content['status'] = see_attempts_and_mark(repo, row_content['status'])
  commits = repo.get_commits()
  row_content['commits'] = str(commits.totalCount)
  row_content['last commit'] = str(commits[0].commit.author.date)
  pulls = repo.get_pulls()
  print(f'{repo.name} has {pulls.totalCount} pulls')
  if pulls.totalCount > 0:
    pull1reviews = repo.get_pull(pulls.totalCount).get_reviews()
    row_content['last review'] = ''
    if pull1reviews.totalCount > 0:
      latest_review = pull1reviews[pull1reviews.totalCount - 1]
      row_content['last review'] = str(latest_review.submitted_at)
      row_content['reviewed by'] = str(latest_review.user.login)
    if row_content['last commit'] > row_content['last review']:
      row_content['pending review'] = 'yes'
    row_content['updated'] = 'yes'
    line_coverage = None
    if fetch_coverage == True:
      line_coverage = coverage(org, repo.name, os.environ['GITHUBAPI_TOKEN'])
    if line_coverage != None:
      row_content['coverage'] = line_coverage


def fill_status_in_sheet(org, repos, interesting, sheet_title, fetch_coverage):
  g = GsheetAssignments(sheet_title)
  interesting_repos = [repo for repo in repos if interesting in repo.name]
  for r in interesting_repos:
    found_repo = g.find_repo_row(r.name)
    if found_repo != None:
      row_content = found_repo['row']
      latest_update_time = str(r.pushed_at)
      if row_content['status'] == '' or row_content['last update'] < latest_update_time:
        row_content['last update'] = latest_update_time
        add_lastseen(row_content, org, r, fetch_coverage)
        g.update_repos(found_repo['row_num'], [row_content])
      else:
        print(f'{r.name} already updated for {latest_update_time}')
    else:
      row_content = repo_to_row(r)
      add_lastseen(row_content, org, r, fetch_coverage)
      g.append_repo(row_content)
      print(f'{r.name} added in sheet')


def last_status(repo):
  try:
    latest_commit = repo.get_commits()[0]
    print(f'latest commit: {latest_commit.sha}')
    check_runs = repo.get_commit(latest_commit.sha).get_check_runs()
    run_statuses = []
    for run in check_runs:
      run_statuses.append(run.conclusion)
    combined_status = 'failure' if any(map(lambda x: x == 'failure' or x == 'error', run_statuses)) \
      else 'pending' if any(map(lambda x: x == 'pending', run_statuses)) \
      else 'success'
    return combined_status
  except:
    return 'error'


def see_attempts_and_mark(repo, repo_status):
  status_mark = repo_status
  if repo.fork:
    upstream_repo = repo.parent
    forked_branch = repo.default_branch
    upstream_branch = upstream_repo.default_branch
    forked_commit = repo.get_branch(forked_branch).commit.sha
    upstream_commit = upstream_repo.get_branch(upstream_branch).commit.sha
    comparison = repo.compare(upstream_commit, forked_commit)
    if comparison.ahead_by > 0:
      status_mark = 'attempted'
  return status_mark


def github_to_sheet(batch, interest, coverage):
  batch_to_org = {
    'tcq-3': 'clean-code-craft-tcq-3',
    'tcq-4': 'clean-code-craft-tcq-4',
    'clean-s-1': 'clean-s-1',
    'tcq-m-2': 'clean-code-craft-tcq-m-2',
    'tcq-7': 'clean-code-craft-tcq-7',
    'p-1': 'clean-code-craft-p-1',
    'personal': 'clean-code-personal',
    'igt-icc': 'code-craft-igt-1',
    'us-1': 'code-craft-us-1'
  }

  githubapi = Github(os.environ['GITHUBAPI_TOKEN'])
  org = batch_to_org[batch]
  title = f'{batch}-{interest}'
  repos = collect_repos(githubapi, org)
  fill_status_in_sheet(org, repos, interest, title, coverage)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Explore assignment submissions')
  parser.add_argument('--batch', required=True, help='name of batch')
  parser.add_argument('--interest', required=True, help='assignment name prefix')
  parser.add_argument('--coverage', dest='coverage', action='store_const', const=True, default=False, help='Collect coverage')

  args = parser.parse_args()
  github_to_sheet(args.batch, args.interest, args.coverage)


# To get logs of a run:
# https://api.github.com/repos/clean-code-craft-tcq-1/typewise-alert-c/actions/runs
# look for the run with "name": "Build and Run"
# https://api.github.com/repos/clean-code-craft-tcq-1/typewise-alert-c/actions/runs/1859022428
# https://api.github.com/repos/clean-code-craft-tcq-1/typewise-alert-c/actions/runs/1859022428/logs
# See https://docs.github.com/en/rest/reference/actions#download-workflow-run-logs
