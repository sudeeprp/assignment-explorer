from numpy import column_stack
from gsheet_assignments import GsheetAssignments

class Interest:
    def __init__(self, batch, interest, sheetname):
        self.batch = batch
        self.interest = interest
        self.sheetname = sheetname

    def reponame2user(self, repo_name):
        lang_prefixes = ['in-c-', 'in-cpp-', 'in-cs-', 'in-java-', 'in-py-']
        repo_name = repo_name.replace(f'{self.interest}-', '')
        for prefix in lang_prefixes:
            repo_name = repo_name.replace(prefix, '')
        return repo_name

    def load(self, morecols):
        g = GsheetAssignments(self.sheetname)
        columns = {'repo': 'user', 'status': self.interest}
        columns.update(morecols)
        return g.column_content(columns)


if __name__ == '__main__':
    # batch = 'tcq2'
    # evaluations = [
    #     {'interest': 'well-named', 'sheetname': f'{batch}-well-named-assignment-reviews', 'morecols': {}},
    #     {'interest': 'test-failer', 'sheetname': f'{batch}-test-failer-assignment-reviews', 'morecols': {}},
    #     {'interest': 'simple-monitor', 'sheetname': f'{batch}-simple-monitor-assignment-reviews', 'morecols': {}},
    #     {'interest': 'coverage', 'sheetname': f'{batch}-coverage-assessment', 'morecols': {
    #         'coverage': 'assessment-coverage',
    #         'tests=spec': 'assessment-readability',
    #         'strong asserts': 'assessment-tests'
    #     }},
    #     {'interest': 'tdd-buckets', 'sheetname': f'{batch}-tdd-buckets-assessment', 'morecols': {}},
    # ]
    batch = 'clean-s-1'
    evaluations = [
        {'interest': 'spring', 'sheetname': f'{batch}-entrance', 'morecols': {}},
    ]

    summary = None
    for eval in evaluations:
        interest = Interest(batch, eval['interest'], eval['sheetname'])
        results = interest.load(eval['morecols'])
        results['user'] = results['user'].apply(interest.reponame2user)
        print(f"Done: {eval['sheetname']}")
        if summary is None:
            summary = results
        else:
            summary = summary.merge(results, how='outer', on='user')
    
    summary.to_csv(f'{batch}-summary.csv')
    print(f"Wrote: {batch}-summary.csv")
