from numpy import column_stack
from gsheet_assignments import GsheetAssignments
import os

class Interest:
    def __init__(self, batch, name, interest, sheetname):
        self.batch = batch
        self.name = name
        self.interest = interest
        self.sheetname = sheetname

    def reponame2user(self, repo_name):
        lang_prefixes = ['in-c-', 'in-cpp-', 'in-cs-', 'in-java-', 'in-py-', 'in-js-']
        repo_name = repo_name.replace(f'{self.interest}-', '')
        for prefix in lang_prefixes:
            repo_name = repo_name.replace(prefix, '')
        return repo_name

    def load(self, morecols):
        g = GsheetAssignments(self.sheetname)
        columns = {'repo': 'User', 'status': self.name}
        columns.update(morecols)
        return g.column_content(columns)


if __name__ == '__main__':
    with open('symbolic-grail-229104-bd96d8b17794.json') as drivecredfile:
        drivecred = drivecredfile.read()
        os.environ['GOOGLE_SERVICE_ACCOUNT_CREDENTIALS'] = drivecred

    batch = 'tcq-m-2'
    evaluations = [
        {'name': 'Naming', 'interest': 'well-named', 'sheetname': f'{batch}-well-named', 'morecols': {}},
        {'name': 'Proven code', 'interest': 'test-failer', 'sheetname': f'{batch}-test-failer', 'morecols': {}},
        {'name': 'Simplicity', 'interest': 'simple-monitor', 'sheetname': f'{batch}-simple-monitor', 'morecols': {}},
        {'name': 'Strategy with tests', 'interest': 'coverage', 'sheetname': f'{batch}-coverage', 'morecols': {'coverage': 'Assessment: coverage'}},
        {'name': 'Extend with TDD', 'interest': 'tdd-buckets', 'sheetname': f'{batch}-tdd-buckets', 'morecols': {}},
        {'name': 'Collaboration project', 'interest': 'stream-line', 'sheetname': f'{batch}-stream-line', 'morecols': {}},
    ]

    summary = None
    for eval in evaluations:
        interest = Interest(batch, eval['name'], eval['interest'], eval['sheetname'])
        results = interest.load(eval['morecols'])
        results['User'] = results['User'].apply(interest.reponame2user)
        print(f"Done: {eval['sheetname']}")
        if summary is None:
            summary = results
        else:
            summary = summary.merge(results, how='outer', on='User')
    
    summary.to_csv(f'{batch}-summary.csv')
    print(f"Wrote: {batch}-summary.csv")
