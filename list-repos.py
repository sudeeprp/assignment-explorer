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
                last_status(repository["url"])
            ]))


def repo_overview_to_sheet(repos, interesting, sheet_title):
  all_row_dicts = map(lambda r: 
    {'repo': r['name'], 'url': r['html_url'], 'last update': r["updated_at"]},
    repos
  )
  interesting_rows = [row for row in all_row_dicts if interesting in row['repo']]
  g = GsheetAssignments(sheet_title)
  g.update_repos(interesting_rows)


def last_status(repo_url):
    return 'not implemented'

if __name__ == '__main__':
  repos = collect_repos()
  repo_overview_to_sheet(collect_repos(), 'sense', 'tcq2-assignments')
  # print_repos(repos, 'sense')
