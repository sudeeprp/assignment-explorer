import pygsheets
import pandas as pd

def repo_to_row_content(repo, title_indexes):
  row_content = [''] * len(title_indexes)
  for prop in repo:
    row_content[title_indexes[prop]] = repo[prop]
  return row_content


class GsheetAssignments:
  heading_row = 1
  def __init__(self, sheet_title) -> None:
    gc = pygsheets.authorize(service_account_env_var='GOOGLE_SERVICE_ACCOUNT_CREDENTIALS')
    print(f'opening {sheet_title}')
    sheetfile = gc.open(sheet_title)
    self.wksheet = sheetfile[0]
    self.opened_data = self.wksheet.get_all_records()
    self.bottom_row = len(self.opened_data) + 1
    headings = self.wksheet.get_row(self.heading_row)
    self.title_indexes = {}
    for index_titles in enumerate(headings):
      self.title_indexes[index_titles[1]] = index_titles[0]
    print(self.title_indexes)

  def find_repo_row(self, repo_name):
    index = next((index for (index, d) in enumerate(self.opened_data)
      if d['repo'] == repo_name), None)
    if (index != None):
      return {'row_num': index + self.heading_row + 1, 'row': self.opened_data[index]}
    else:
      return None

  def update_repos(self, row_to_update, repos_props):
    for repo in repos_props:
      print(f'updating row {row_to_update} with {repo}')
      self.wksheet.update_row(row_to_update,
        repo_to_row_content(repo, self.title_indexes))
      row_to_update += 1

  def append_repo(self, repo_props):
    self.wksheet.update_row(self.bottom_row + 1, repo_to_row_content(repo_props, self.title_indexes))
    self.bottom_row += 1

  def column_content(self, headings_map):
    return pd.DataFrame(self.opened_data, columns=headings_map).rename(columns=headings_map)
