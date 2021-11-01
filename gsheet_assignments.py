import pygsheets

def repo_to_row_content(repo, title_indexes):
  row_content = [''] * len(title_indexes)
  for prop in repo:
    row_content[title_indexes[prop]] = repo[prop]
  return row_content


class GsheetAssignments:
  heading_row = 1
  def __init__(self, sheet_title) -> None:
    gc = pygsheets.authorize(service_file='sheeta.json')
    sheetfile = gc.open(sheet_title)
    self.wksheet = sheetfile[0]
    self.opened_data = self.wksheet.get_all_records()
    headings = self.wksheet.get_row(self.heading_row)
    self.title_indexes = {}
    for index_titles in enumerate(headings):
      self.title_indexes[index_titles[1]] = index_titles[0]
    print(self.title_indexes)

  def find_repo_row(self, repo_name):
    index = next((index for (index, d) in enumerate(self.opened_data)
      if d['repo'] == repo_name), None)
    if (index != None):
      return index + self.heading_row + 1
    else:
      return None

  def update_repos(self, repos_props):
    row_to_update = self.heading_row + 1
    for repo in repos_props:
      self.wksheet.update_row(row_to_update,
        repo_to_row_content(repo, self.title_indexes))
      row_to_update += 1

if __name__ == '__main__':
  g = GsheetAssignments('tcq2-assignments')
  print(f'index of repo1: {g.find_repo_row("repo1")}')
  print(f'index of repo3: {g.find_repo_row("repo3")}')
  print(f'index of unknown: {g.find_repo_row("unknown")}')
  g.update_repos([
    {'repo': 'r1', 'url': 'u1', 'last update': 'l1'},
    {'repo': 'r2', 'url': 'u2', 'last update': 'l2'}
  ])

# worksheet.update_value((2,1), 'try')
# print("updated")