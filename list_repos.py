import requests
from gsheet_assignments import GsheetAssignments

def collect_repos():
  resp = requests.get('https://api.github.com/orgs/assignments-for-discussion/repos')
  repos = resp.json()
  while 'next' in resp.links.keys():
    resp = requests.get(resp.links['next']['url'])
    repos.extend(resp.json())
  print(f'#Collected a total of {len(repos)} repositories')
  return repos


def repo_to_row(r):
  return {'repo': r['name'], 'url': files_url(r['html_url']), 'last update': r["updated_at"]}


def repo_overview_to_sheet(repos, interesting, sheet_title):
  all_row_dicts = map(repo_to_row,  repos)
  interesting_rows = [row for row in all_row_dicts if interesting in row['repo']]
  g = GsheetAssignments(sheet_title)
  g.update_repos(2, interesting_rows)


def files_url(url):
  return url + '/pull/1/files'


def fill_status_in_sheet(repos, interesting, sheet_title):
  g = GsheetAssignments(sheet_title)
  interesting_repos = [repo for repo in repos if interesting in repo['name']]
  for r in interesting_repos:
    found_repo = g.find_repo_row(r['name'])
    if found_repo != None:
      row_content = found_repo['row']
      if row_content['status'] == '' or row_content['last update'] < r['updated_at']:
        row_content['last update'] = r['updated_at']
        row_content['status'] = last_status(row_content['repo'])
        row_content['updated'] = 'x'
        g.update_repos(found_repo['row_num'], [row_content])
      else:
        print(f'{r["name"]} already updated for {r["updated_at"]}')
    else:
      row_content = repo_to_row(r)
      row_content['status'] = last_status(row_content['repo'])
      row_content['updated'] = 'x'
      g.append_repo(row_content)
      print(f'{r["name"]} added in sheet')


def last_status(repo_name):
  runs_url = f'https://api.github.com/repos/assignments-for-discussion/{repo_name}/actions/runs'
  status_resp = requests.get(runs_url)
  if status_resp.status_code == 200:
    runs = status_resp.json()
    return runs['workflow_runs'][0]['conclusion']
  else:
    print(f'workflow runs get failed for {runs_url}: status {status_resp.status_code}. try after some time?')
    return ''


if __name__ == '__main__':
  repos = collect_repos()
  interest = 'analytics-and-specification'
  title = 'externship-entrance'
  # repo_overview_to_sheet(repos, interest, title)
  fill_status_in_sheet(repos, interest, title)
  