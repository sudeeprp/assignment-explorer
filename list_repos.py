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
  # as per https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_workflow_runs
  try:
    runs = repo.get_workflow_runs()
  except:
    return 'error'
  if runs.totalCount > 0:
    run_number = runs[0].run_number
    conclusion = runs[0].conclusion
    if conclusion == 'success':
      i = 1
      while i < runs.totalCount and runs[i].run_number == run_number:
        print(f'checking more runs of #{run_number}')
        if runs[i].conclusion != 'success':
          conclusion = runs[i].conclusion
          break
        i += 1
    return conclusion
  else:
    print(f'{repo} has no workflow runs')
    return ''


def github_to_sheet(batch, interest, coverage):
  batch_to_org = {
    'tcq-3': 'clean-code-craft-tcq-3',
    'tcq-4': 'clean-code-craft-tcq-4',
    'clean-s-1': 'clean-s-1',
    'tcq-m-2': 'clean-code-craft-tcq-m-2',
    'tcq-7': 'clean-code-craft-tcq-7',
    'p-1': 'clean-code-craft-p-1',
    'personal': 'clean-code-personal'
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
