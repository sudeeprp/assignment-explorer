from asyncio import subprocess
import requests
from github import Github
import json
import subprocess
import re


class ExtractException(Exception):
  pass


def fetch(url, token):
  resp = requests.get(url, headers={'Authorization': f"token {token}"})
  if resp.status_code == 200:
    return resp.json()
  else:
    raise ExtractException(f'error with {url}: {resp.status_code}')


def extract_first(list, key=None, substr=None):
  filtered = []
  if key == None:
    filtered = list
  else:
    filtered = [r for r in list if substr in r[key].lower()]
  if len(filtered) == 0:
    raise ExtractException(f'{substr} in {key} not found')
  return filtered[0]


def cov_percent(log, prefixes):
  loglines = log.decode('utf-8').split('\n')
  linecov = [l for l in loglines if any(p in l for p in prefixes)]
  print(f'linecov: {linecov}')
  if len(linecov) == 0:
    print(f'{prefixes} not found')
    return ''
  return re.search('([0-9.]+)%', linecov[0]).group(1)


def extract_coverage(jobid, org, repo_name):
  try:
    runlog = subprocess.check_output(f"gh run view --job {jobid} --repo {org}/{repo_name} --log")
    cov = cov_percent(runlog, ['lines:', 'TOTAL'])
    if cov == '':
      return cov
    else:
      return float(cov)
  except subprocess.CalledProcessError as e:
    print(f'error extracting logs for {repo_name}')
    return 'err'


def coverage(org, repo_name, token):
  try:
    repobase = f'https://api.github.com/repos/{org}/{repo_name}'
    runs = fetch(f'{repobase}/actions/runs', token)
    buildflow = extract_first(runs['workflow_runs'], 'name', 'build')
    print(f"going for run {buildflow['id']}")
    joblist = fetch(f"{repobase}/actions/runs/{buildflow['id']}/jobs", token)
    job = extract_first(joblist['jobs'])
    print(f"found job {job['id']}")
    return extract_coverage(job['id'], org, repo_name)
  except ExtractException as e:
    print(e)
    return ''


def repocoverage(repo, token):
  workflows = repo.get_workflows()
  if workflows.totalCount > 0:
    buildflows = [r for r in workflows if r.name == 'Build and Run']
    print(f'going for workflow {buildflows[0].id}')
    runs = buildflows[0].get_runs()
    if runs.totalCount > 0:
      print(runs[0].logs_url)
      logs = requests.get(runs[0].logs_url, headers={'Authorization': f"token {token}"})
      print(logs.text.decode())


if __name__ == '__main__':
  with open('github.json') as f:
    tok = json.load(f)
  print(coverage('clean-code-craft-tcq-2', 'coverage-in-cpp-JuanAvelar', tok['ken']))
  print(coverage('clean-code-craft-tcq-2', 'coverage-in-py-Venkatesha-Iyengar', tok['ken']))
  print(coverage('clean-code-craft-tcq-2', 'tdd-buckets-SuchithaNM', tok['ken']))
  print(coverage('clean-code-craft-tcq-2', 'tdd-buckets-vaishnavi-nayak-sujir', tok['ken']))
