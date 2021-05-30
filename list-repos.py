import requests


def collect_repos():
    resp = requests.get('https://api.github.com/orgs/clean-code-craft-tcq-1/repos')
    repos = resp.json()
    while 'next' in resp.links.keys():
        resp = requests.get(resp.links['next']['url'])
        repos.extend(resp.json())
    print(f'#Collected a total of {len(repos)} repositories')
    return repos


def print_repos(repos, interesting):
    print('Owner,URL')
    for repository in repos:
        reponame = repository['full_name']
        if interesting in reponame:
            print(repository["html_url"])


if __name__ == '__main__':
    print_repos(collect_repos(), 'stream-bms-data')
