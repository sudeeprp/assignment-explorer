import requests
from gsheet_assignments import GsheetAssignments
from github import Github
import json

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


def fill_status_in_sheet(repos, interesting, sheet_title):
  g = GsheetAssignments(sheet_title)
  interesting_repos = [repo for repo in repos if interesting in repo.name]
  for r in interesting_repos:
    found_repo = g.find_repo_row(r.name)
    if found_repo != None:
      row_content = found_repo['row']
      latest_update_time = str(r.pushed_at)
      if row_content['status'] == '' or row_content['last update'] < latest_update_time:
        row_content['last update'] = latest_update_time
        row_content['status'] = last_status(r)
        row_content['updated'] = 'x'
        g.update_repos(found_repo['row_num'], [row_content])
      else:
        print(f'{r.name} already updated for {latest_update_time}')
    else:
      row_content = repo_to_row(r)
      row_content['status'] = last_status(r)
      row_content['updated'] = 'x'
      g.append_repo(row_content)
      print(f'{r.name} added in sheet')


def last_status(repo):
  # as per https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_workflow_runs
  runs = repo.get_workflow_runs()
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


if __name__ == '__main__':
  with open('github.json') as f:
    tok = json.load(f)
  githubapi = Github(tok['ken'])

  org = 'clean-code-craft-tcq-2'
  interest = 'well-named'
  title = 'tcq2-well-named-assignment'

  repos = collect_repos(githubapi, org)
  fill_status_in_sheet(repos, interest, title)
  