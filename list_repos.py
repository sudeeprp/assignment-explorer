import requests
from gsheet_assignments import GsheetAssignments

def collect_repos():
  resp = requests.get('https://api.github.com/orgs/clean-code-craft-tcq-2/repos')
  repos = resp.json()
  while 'next' in resp.links.keys():
    resp = requests.get(resp.links['next']['url'])
    repos.extend(resp.json())
  print(f'#Collected a total of {len(repos)} repositories')
  return repos


def print_repos(repos, interesting):
    print('repo,URL,last update,status')
    for repository in repos:
        reponame = repository['name']
        if interesting in reponame:
            print(','.join([
                reponame,
                repository["html_url"],
                repository["updated_at"],
                last_status(reponame)
            ]))


def repo_overview_to_sheet(repos, interesting, sheet_title):
  all_row_dicts = map(lambda r: 
    {'repo': r['name'], 'url': r['html_url'], 'last update': r["updated_at"]},
    repos
  )
  interesting_rows = [row for row in all_row_dicts if interesting in row['repo']]
  g = GsheetAssignments(sheet_title)
  g.update_repos(interesting_rows)


def fill_status_in_sheet(repos, interesting, sheet_title):
  g = GsheetAssignments(sheet_title)
  for r in repos:
    found_repo = g.find_repo_row(r['name'])
    if found_repo != None:
      row_content = found_repo['row']
      if row_content['status'] == '':
        row_content['status'] = last_status(row_content['repo'])
        g.update_repos(found_repo['row_num'], [row_content])
        print(f'updated row {found_repo["row_num"]} with {row_content}')
      else:
        print(f'{r["name"]} already updated')
    else:
      print(f'{r["name"]} not found in sheet')


def last_status(repo_name):
  runs_url = f'https://api.github.com/repos/clean-code-craft-tcq-2/{repo_name}/actions/runs'
  status_resp = requests.get(runs_url)
  if status_resp.status_code == 200:
    runs = status_resp.json()
    return runs['workflow_runs'][0]['conclusion']
  else:
    print(f'workflow runs get failed for {runs_url}: status {status_resp.status_code}. try after some time?')
    return ''


if __name__ == '__main__':
  repos = collect_repos()
  interest = 'sense'
  # repo_overview_to_sheet(repos, interest, 'tcq2-assignments')
  fill_status_in_sheet(repos, interest, 'tcq2-assignments')
  # print_repos(repos, 'sense')
