import papermill as pm
import subprocess
import os

dataPath = 'C:/Users/au646069/ECG/1_VPN_aux/'
reportPath = 'C:/Users/au646069/github/CardioceptionPaper/reports/'
subList = os.listdir(dataPath)

# Heart rate Discrimination
for sub in subList:

   try:
      pm.execute_notebook(
         'HeartRateDiscrimination.ipynb',
         reportPath + 'HRD/' + sub + '.ipynb',
         parameters=dict(subject=sub, path=dataPath)
      )

      command = f'jupyter nbconvert {reportPath}{sub}.ipynb --output {reportPath}HRD/{sub}_report.html --no-input --to html'
      subprocess.call(command)
      os.remove(reportPath + 'HRD/' + sub + '.ipynb')

   except:
      print(f'Subject {sub} not found.')

# Heartbeat Counting task
for sub in subList:

   try:
      pm.execute_notebook(
         'HeartBeatCounting.ipynb',
         reportPath + 'HBC/' + sub + '.ipynb',
         parameters=dict(subject=sub, path=dataPath)
      )

      command = f'jupyter nbconvert --to html --execute {reportPath}HBC/{sub}.ipynb --output {reportPath}HBC/{sub}_report.html'
      subprocess.call(command)
      os.remove(reportPath + 'HBC/' + sub + '.ipynb')
   except:
      print(f'Subject {sub} not found.')