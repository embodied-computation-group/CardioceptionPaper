import papermill as pm
import subprocess
import os

dataPath = 'Z:/MINDLAB2019_Visceral-Mind/1_VMP_aux/'
reportPath = 'Z:/MINDLAB2019_Visceral-Mind/6_reports/'
sub = os.listdir(dataPath)

for sub in os.listdir(os.path.join(os.getcwd(), 'data')):

    pm.execute_notebook(
       'Analyses.ipynb',
       path + sub + '.ipynb',
       parameters=dict(subject=sub)
    )

    command = f'jupyter nbconvert {path}{sub}.ipynb --output {path}{sub}_report.html --no-input'
    subprocess.call(command)
