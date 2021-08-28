import requests
import json
import time

def clickup_data():
  workers = {}   # dictionary of workers with ids as their keys

  key = '#####' # ----- Replace ##### with api key from your clickup 
  headers = {
    'Authorization': key
  }
  headers2 = {
    'Authorization': key,
    'Content-Type': 'application/json'
  }

  # fetching team id and member details
  team_url = 'https://api.clickup.com/api/v2/team'
  response_team = requests.get(team_url, headers=headers)
  teams_data = json.loads(response_team.text)
  for team in teams_data['teams']:
    if team['name'] == '#####': # ----- Replace ##### with team name
      team_id = team['id']
      for member in team['members']:
        worker_data = { 'name': member['user']['username'],
                        'tasks': []
                      }
        workers[member['user']['id']] = worker_data
      break

  # fetching 'Kunden' space id through team id
  spaces_url = f'https://api.clickup.com/api/v2/team/{team_id}/space?archived=false'
  response_spaces = requests.get(spaces_url, headers=headers)
  spaces_data = json.loads(response_spaces.text)
  for space in spaces_data['spaces']:
      if space['name'] == 'Kunden':
        space_id = space['id']
        break

  # fetching lists using space id
  list_of_lists = []
  lists_url = f'https://api.clickup.com/api/v2/space/{space_id}/list?archived=false'
  response_lists = requests.get(lists_url, headers=headers)
  lists_data = json.loads(response_lists.text)
  for listed in lists_data['lists']:
    list_of_lists.append(listed['id'])

  #fetching tasks from list ids
  for list_id in list_of_lists:
    tasks_url = f'https://api.clickup.com/api/v2/list/{list_id}/task?archived=false'
    response_tasks = requests.get(tasks_url, headers=headers)
    tasks_data = json.loads(response_tasks.text)

    for task in tasks_data['tasks']:
      if str(task['status']['status']).lower() == 'time tracking':
        for field in task['custom_fields']:
          if str(field['name']).lower() == 'rate':
            try:
              rate = field['value'] + '' + field['type_config']['currency_type']
            except:
              rate = 'Not defined'
          if str(field['name']).lower() == 'total hours':
            try:
              total_hours = field['value']
            except:
              total_hours = 'Not defined'
        for assignee in task['assignees']:
          task_data = {'id': task['id'], 
                      'name': task['name'],
                      'rate': rate,
                      'available hours': total_hours,
                      'hours logged': 0
                      }
          workers[assignee['id']]['tasks'].append(task_data) 
    time.sleep(1)

  # fetching this week's time using team id
  one_week = 604800000 #milliseconds
  end_date = int(time.time())*1000
  start_date = end_date - one_week

  for assignee in workers:
    time_url = f'https://api.clickup.com/api/v2/team/{team_id}/time_entries?start_date={start_date}&end_date={end_date}&assignee={assignee}'
    response_time = requests.get(time_url, headers=headers2)
    time_data = json.loads(response_time.text)
    for entry in time_data['data']:
      try:
        task_id = entry['task']['id']
      except:
        continue
      more_time = entry['duration']
      for j in range(len(workers[assignee]['tasks'])):
        if workers[assignee]['tasks'][j]['id'] == task_id:
          workers[assignee]['tasks'][j]['hours logged'] += int(more_time)

  return (workers)