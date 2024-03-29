from asyncio import subprocess
import requests
from github import Github
import json
import subprocess
import re
import traceback


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
  loglines = log.split('\n')
  linecov = [l for l in loglines if any(p in l for p in prefixes)]
  print(f'linecov: {linecov}')
  if len(linecov) == 0:
    print(f'{prefixes} not found')
    return ''
  return re.search('([0-9.]+)%', linecov[0]).group(1)


def extract_coverage(repobase, jobid, token):
  try:
    runlog_resp = requests.get(f'{repobase}/actions/jobs/{jobid}/logs', headers={'Authorization': f"token {token}"})
    print(f'runlog resp status {runlog_resp.status_code}')
    runlog = runlog_resp.text
    cov = cov_percent(runlog, ['lines:', 'TOTAL'])
    if cov == '':
      return cov
    else:
      return float(cov)
  except Exception as e:
    print(f'error extracting logs for {repobase}:')
    print(traceback.format_exc())
    return 'err'


def coverage_from_artifact(artifacts_url, token):
  artifact_set = fetch(artifacts_url, token)
  zip_download_url = artifact_set['artifacts'][0]['archive_download_url']
  zip_resp = requests.get(zip_download_url, stream=True)
  with open("cov_artifact.zip", "wb") as f:
    for chunk in zip_resp.iter_content(chunk_size=1024):
      if chunk:  # filter out keep-alive new chunks
        f.write(chunk)
  print('done writing cov_artifact.zip')


def coverage(org, repo_name, token):
  try:
    repobase = f'https://api.github.com/repos/{org}/{repo_name}'
    runs = fetch(f'{repobase}/actions/runs', token)
    buildflow = extract_first(runs['workflow_runs'], 'name', 'build')
    print(f"going for run {buildflow['id']}")
    joblist = fetch(f"{repobase}/actions/runs/{buildflow['id']}/jobs", token)
    job = extract_first(joblist['jobs'])
    print(f"found job {job['id']}")
    cov = extract_coverage(repobase, job['id'], token)
    if cov == '':
      cov = coverage_from_artifact(buildflow['artifacts_url'], token)
    return cov
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

  print(coverage('clean-code-craft-tcq-7', 'coverage-in-java-KeerthanaKuppuchamy', tok['ken']))
  print(coverage('clean-code-craft-tcq-2', 'coverage-in-cpp-JuanAvelar', tok['ken']))
