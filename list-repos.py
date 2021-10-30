import requests


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


def last_status(repo_url):


if __name__ == '__main__':
    print_repos(collect_repos(), 'sense')
