# Assignment Explorer

Summarizes Assignment submission along with build / workflow-run status.

## Pre-requisites

Install dependencies

```bash
pip install -r requirements.txt
```

Create a Google Sheet in your Google Drive with column headings in the first sheet. The column headings are:

repo,url,status,lines,branches,pending review,reviewer,last update,last commit,last review,reviewed by,commits,updated

Remember the title of this Google Sheet. This is where the submissions summary will arrive.

Check `interest` and `title` at the bottom of `list_repos.py`:

- `interest` must identify the assignment (prefixed in all submission by GitHub Classroom)
- `title` is the title of your Google Sheet.

Place the json file having Google-project-key in this folder.

Permit the email in there to write to your Google Sheet
