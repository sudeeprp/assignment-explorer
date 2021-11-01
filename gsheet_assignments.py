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
    print(f'opening {sheet_title}')
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
      return {'row_num': index + self.heading_row + 1, 'row': self.opened_data[index]}
    else:
      return None

  def update_repos(self, row_to_update, repos_props):
    for repo in repos_props:
      print(f'updating row {row_to_update} with {repo}')
      self.wksheet.update_row(row_to_update,
        repo_to_row_content(repo, self.title_indexes))
      row_to_update += 1

if __name__ == '__main__':
  g = GsheetAssignments('tcq2-assignments')
  print(f'index of sense-py-TalhaKhatib: {g.find_repo_row("sense-py-TalhaKhatib")}')
  # g.update_repos(2, [
  #   {'repo': 'r1', 'url': 'u1', 'last update': 'l1'},
  #   {'repo': 'r2', 'url': 'u2', 'last update': 'l2'}
  # ])

# worksheet.update_value((2,1), 'try')
# print("updated")