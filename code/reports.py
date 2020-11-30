import papermill as pm
import subprocess
import os

dataPath = 'C:/Users/au646069/ECG/1_VPN_aux/'
reportPath = 'C:/Users/au646069/github/CardioceptionPaper/reports/'
subList = os.listdir(dataPath)

for sub in subList:

   try:
      pm.execute_notebook(
         'HeartRateDiscrimination.ipynb',
         reportPath + sub + '.ipynb',
         parameters=dict(subject=sub, path=dataPath)
      )

      command = f'jupyter nbconvert {reportPath}{sub}.ipynb --output {reportPath}{sub}_report.html --no-input --to html'
      subprocess.call(command)
   except:
      print(f'Subject {sub} not found.')