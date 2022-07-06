# Assignment Explorer

Summarizes [Assignment submissions](running-batches.md) along with build / workflow-run status.

## Pre-requisites

This script runs as an action as well as locally. Local running instructions are at the end.

### Sheet to collect submissions

- Create a Google Sheet and name it with the `batch`-`assignment`. E.g., if the batch is `tcq-4` and the assignment is `well-named`, then the sheet name should be `tcq-4-well-named`.
- Place these column headings in the first row of the first sheet:

repo,url,status,coverage,pending review,reviewer,last update,last commit,last review,reviewed by,commits,updated

### Run GitHub action

- Share the sheet with edit access to assignmentrecords@symbolic-grail-229104.iam.gserviceaccount.com
- Go to Actions and select Submission results under 'All workflows'
- Drop-down the 'Run workflow', select the batch and assignment name. Run the workflow

### Run locally

To use this tool locally, you need:

1. a [GitHub token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/) with the `repo` scope.
1. Google Drive [service-account credentials](https://developers.google.com/workspace/guides/create-credentials#service-account)

Install dependencies

```bash
pip install -r requirements.txt
```

Place the GitHub token in a file called github.json, with an object containing a key called 'ken', having value of the token

```json
{
  "ken": "github-token"
}
```

Place the json file having Google-project-key in this folder. Update its name in `select-assignment-report.py`. It will be similar to this:

```
{
  "type": "service_account",
  "project_id": "abcd-1234",
  "private_key_id": "xyz-5678",
  "private_key": "-----BEGIN PRIVATE KEY...
  "client_email": "email@project.iam.gserviceaccount.com"
  ...
}
```

Permit the email in there to write to your Google Sheet

Uncomment the required batch and interest and run `python select-assignment-report.py`
