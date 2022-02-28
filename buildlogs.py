from asyncio import subprocess
import requests
from github import Github
import json
import subprocess
import re


class ExtractException(Exception):
  pass


def fetch(url):
  resp = requests.get(url)
  if resp.status_code == 200:
    return resp.json()
  else:
    raise ExtractException(f'error with {url}: {resp.status_code}')


def extract_first(list, key=None, value=None):
  filtered = []
  if key == None:
    filtered = list
  else:
    filtered = [r for r in list if r[key] == value]
  if len(filtered) == 0:
    raise ExtractException(f'{key}={value} not found')
  return filtered[0]


def cov_percent(log, prefix):
  lines = log.decode('utf-8').split('\n')
  linecov = [l for l in lines if prefix in l]
  if len(linecov) == 0:
    raise ExtractException(f'{prefix} not found')
  return re.search('([0-9.]+)%', linecov[0]).group(1)


def coverage(org, repo_name):
  try:
    repobase = f'https://api.github.com/repos/{org}/{repo_name}'
    runs = fetch(f'{repobase}/actions/runs')
    buildflow = extract_first(runs['workflow_runs'], 'name', 'Build and Run')
    print(f"going for run {buildflow['id']}")
    joblist = fetch(f"{repobase}/actions/runs/{buildflow['id']}/jobs")
    job = extract_first(joblist['jobs'])
    print(f"found job {job['id']}")
    requests.get(f"{repobase}/actions/jobs/{job['id']}/logs")
    runlog = subprocess.check_output(f"gh run view --job {job['id']} --repo {org}/{repo_name} --log")
    return {
      'linecov': cov_percent(runlog, 'lines:'),
      'branchcov': cov_percent(runlog, 'branches:'),
    }
  except ExtractException as e:
    print(e)
    return {
      'linecov': '',
      'branchcov': '',
    }


def repocoverage(repo):
  runs = repo.get_workflow_runs()
  if runs.totalCount > 0:
    buildflows = [r for r in runs if r.name == 'Build and Run']
    print(f'going for run {buildflows[0].id}')
    


if __name__ == '__main__':
  with open('github.json') as f:
    tok = json.load(f)
  githubapi = Github(tok['ken'])
  cov = coverage('clean-code-craft-tcq-2', 'coverage-in-cpp-JuanAvelar')
  print(f'got cov: {cov}')