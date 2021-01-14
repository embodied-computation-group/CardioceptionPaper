# Author: Nicolas Legrand <nicolas.legrand@cfin.au.dk>

import papermill as pm
import subprocess
import os
import multiprocessing as mp

sub = 'sub_0076'
def reportHRD(
    sub,
    datapath="C:/Users/au646069/ECG/1_VPN_aux/",
    reportPath="C:/Users/au646069/github/CardioceptionPaper/reports/",
    session='Del1'
):
        
    try:
        pm.execute_notebook(
            "C:/Users/au646069/github/CardioceptionPaper/code/HeartRateDiscrimination.ipynb",
            f"{reportPath}HRD/{sub}.ipynb",
            parameters=dict(subject=sub, path=datapath, session=session),
        )
        command = f"jupyter nbconvert --to html --execute --TemplateExporter.exclude_input=True {reportPath}HRD/{sub}.ipynb --output {reportPath}HRD/{sub}_report.html"
        subprocess.call(command)
        os.remove(reportPath + "HRD/" + sub + ".ipynb")
    except:
        print(f'Subject {sub} not found.')


if __name__ == "__main__":
    datapath = "C:/Users/au646069/ECG/1_VPN_aux/"
    subList = os.listdir(datapath)
    pool = mp.Pool(processes=4)
    pool.map(reportHRD, subList)
