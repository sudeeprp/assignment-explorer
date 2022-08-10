from list_repos import github_to_sheet
import json
import os

batch = 'tcq-m-2'
interest = 'spring'

# batch = 'clean-s-1'
# interest = 'coverage'
# interest = 'simple-monitor'
# title = 'clean-s-1-simple-monitor-assignment'
# interest = 'test-failer'
# title = 'clean-s-1-test-failer-assignment'
# interest = 'well-named'
# title = 'clean-s-1-well-named-assignment'
# interest = 'spring'
# title = 'clean-s-1-entrance'

# batch = 'tcq-4'
# interest = 'coverage'
# interest = 'test-failer'
# title = 'tcq4-test-failer-assignment'
# interest = 'well-named'
# title = 'tcq4-well-named-assignment'
# interest = 'spring'
# title = 'tcq4-spring-assessment'

# batch = 'tcq-3'
# interest = 'tdd-buckets'
# title = 'tcq-3-tdd-buckets'
# interest = 'tdd-buckets'
# title = 'tcq3-tdd-buckets-assessment'
# interest = 'coverage'
# title = 'tcq3-coverage-assessment'
# interest = 'simple-monitor'
# title = 'tcq3-simple-monitor-assignment-reviews'
# interest = 'test-failer'
# title = 'tcq3-test-failer-assignment'
# interest = 'well-named'
# title = 'tcq3-well-named-assignment'
# interest = 'spring'
# title = 'tcq3-spring-assessment'

# org = 'clean-coder-lead-1'
# interest = 'summerent'
# title = 'clean-coder-lead-1-entrance' 

# org = 'clean-code-craft-tcq-2'
# interest = 'stream-line'
# title = 'tcq2-stream-line'
# interest = 'tdd-buckets'
# title = 'tcq2-tdd-buckets-assessment'
# interest = 'coverage'
# title = 'tcq2-coverage-assessment'
# interest = 'simple-monitor'
# title = 'tcq2-simple-monitor-assignment-reviews'
# interest = 'test-failer'
# title = 'tcq2-test-failer-assignment-reviews'
# interest = 'well-named'
# title = 'tcq2-well-named-assignment-reviews'

with open('github.json') as githubtokenfile:
    tok = json.load(githubtokenfile)
    os.environ['GITHUBAPI_TOKEN'] = tok['ken']

with open('symbolic-grail-229104-bd96d8b17794.json') as drivecredfile:
    drivecred = drivecredfile.read()
    os.environ['GOOGLE_SERVICE_ACCOUNT_CREDENTIALS'] = drivecred

github_to_sheet(batch, interest, coverage=False)
