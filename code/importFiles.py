from shutil import copyfile, copyfileobj
import zipfile
import os


def import_from_aux(localPath, serverPath):
    """Import raw files from AUX"""

    subList = os.listdir(serverPath)
    # HRD
    for sub in subList:
        if sub.startswith('sub'):

            file = [serverPath+f'{sub}/HRD/{sub[4:]}001_final.txt',
                    serverPath+f'{sub}/HRD/{sub[4:]}HRD_final.txt',
                    serverPath+f'{sub}/{sub[4:]}HRD/{sub[4:]}HRD_final.txt']
            try:
                copyfile(file[0], f'{localPath}{sub}/HRD/HRD_final.txt')
            except:
                try:
                    copyfile(file[1], f'{localPath}{sub}/HRD/HRD_final.txt')
                except:
                    try:
                        copyfile(file[2], f'{localPath}{sub}/HRD/HRD_final.txt')
                    except:
                        try:
                            with zipfile.ZipFile(serverPath+f'{sub}/HRD.zip', 'r') as zip_ref:
                                source = zip_ref.open(f'Users/stimuser/Desktop/data/{sub[4:]}HRD/{sub[4:]}HRD_final.txt')
                                target = open(f'{localPath}{sub}/HRD/HRD_final.txt', "wb")
                                with source, target:
                                    copyfileobj(source, target)
                        except:
                            print(f'{file[2]} not found')



    # HRD - PPG signal_df
    for sub in subList:
        if sub.startswith('sub'):

            file = [serverPath+f'{sub}/HRD/{sub[4:]}_signal.txt',
                    serverPath+f'{sub}/HRD/{sub[4:]}_signal.txt',
                    serverPath+f'{sub}/{sub[4:]}HRD/{sub[4:]}_signal.txt']
            try:
                copyfile(file[0], f'{localPath}{sub}/HRD/signal.txt')
            except:
                try:
                    copyfile(file[1], f'{localPath}{sub}/HRD/signal.txt')
                except:
                    try:
                        copyfile(file[2], f'{localPath}{sub}/HRD/signal.txt')
                    except:
                        try:
                            with zipfile.ZipFile(serverPath+f'{sub}/HRD.zip', 'r') as zip_ref:
                                source = zip_ref.open(f'Users/stimuser/Desktop/data/{sub[4:]}HRD/{sub[4:]}_signal.txt')
                                target = open(f'{localPath}{sub}/HRD/signal.txt', "wb")
                                with source, target:
                                    copyfileobj(source, target)
                        except:
                            print(f'{file[2]} not found')


    # HRD - posteriors
    for sub in subList:
        if sub.startswith('sub'):

            for cond in ['Intero_posterior.npy', 'Extero_posterior.npy']:
                file = [serverPath+f'{sub}/HRD/{sub[4:]}{cond}',
                        serverPath+f'{sub}/HRD/{sub[4:]}{cond}',
                        serverPath+f'{sub}/{sub[4:]}HRD/{sub[4:]}{cond}']
                try:
                    copyfile(file[0], f'{localPath}{sub}/HRD/{cond}')
                except:
                    try:
                        copyfile(file[1], f'{localPath}{sub}/HRD/{cond}')
                    except:
                        try:
                            copyfile(file[2], f'{localPath}{sub}/HRD/{cond}')
                        except:
                            try:
                                with zipfile.ZipFile(serverPath+f'{sub}/HRD.zip', 'r') as zip_ref:
                                    source = zip_ref.open(f'Users/stimuser/Desktop/data/{sub[4:]}HRD/{sub[4:]}{cond}')
                                    target = open(f'{localPath}{sub}/HRD/{cond}', "wb")
                                    with source, target:
                                        copyfileobj(source, target)
                            except:
                                print(f'{file[2]} not found')

    # HBC
    for sub in subList:
        if sub.startswith('sub'):

            file = [serverPath+f'{sub}/HBC/{sub[4:]}002_final.txt',
                    serverPath+f'{sub}/HBC/{sub[4:]}HRD_final.txt',
                    serverPath+f'{sub}/{sub[4:]}HBC/{sub[4:]}HBC_final.txt']
            try:
                copyfile(file[0], f'{localPath}{sub}/HBC/HBC_final.txt')
            except:
                try:
                    copyfile(file[1], f'{localPath}{sub}/HBC/HBC_final.txt')
                except:
                    try:
                        copyfile(file[2], f'{localPath}{sub}/HBC/HBC_final.txt')
                    except:
                        try:
                            with zipfile.ZipFile(serverPath+f'{sub}/HBC.zip', 'r') as zip_ref:
                                source = zip_ref.open(f'Users/stimuser/Desktop/data/{sub[4:]}HBC/{sub[4:]}HBC_final.txt')
                                target = open(f'{localPath}{sub}/HBC/HBC_final.txt', "wb")
                                with source, target:
                                    copyfileobj(source, target)
                        except:
                            print(f'{file[2]} not found')


    # HBC (PPG files)
    for sub in subList:
        if sub.startswith('sub'):

            for i in range(6):

                file = [serverPath+f'{sub}/HBC/{sub[4:]}{i}_{i}.npy',
                        serverPath+f'{sub}/HBC/{sub[4:]}{i}_{i}.npy',
                        serverPath+f'{sub}/{sub[4:]}HBC/{sub[4:]}{i}_{i}.npy']
                try:
                    copyfile(file[0], f'{localPath}{sub}/HBC/{sub[4:]}_{i}.npy')
                except:
                    try:
                        copyfile(file[1], f'{localPath}{sub}/HBC/{sub[4:]}_{i}.npy')
                    except:
                        try:
                            copyfile(file[2], f'{localPath}{sub}/HBC/{sub[4:]}_{i}.npy')
                        except:
                            try:
                                with zipfile.ZipFile(serverPath+f'{sub}/HBC.zip', 'r') as zip_ref:
                                    source = zip_ref.open(f'Users/stimuser/Desktop/data/{sub[4:]}HBC/{sub[4:]}{i}_{i}.npy')
                                    target = open(f'{localPath}{sub}/HBC/{sub[4:]}_{i}.npy', "wb")
                                    with source, target:
                                        copyfileobj(source, target)
                            except:
                                print(f'{file[2]} not found')

    # HRD - Del 2
    for sub in subList:
        if sub.startswith('sub'):
            if os.path.exists(serverPath+f'{sub}/HRD_del2.zip'):
                if not os.path.exists(f'{localPath}/{sub}/HRD_del2/'):
                    os.makedirs(f'{localPath}{sub}/HRD_del2/')

            try:
                with zipfile.ZipFile(serverPath+f'{sub}/HRD_del2.zip', 'r') as zip_ref:
                    source = zip_ref.open(f'Users/stimuser/Desktop/data/{sub[4:]}HRD_del2/{sub[4:]}HRD_del2_final.txt')
                    target = open(f'{localPath}{sub}/HRD_del2/HRD_del2_final.txt', "wb")
                    with source, target:
                        copyfileobj(source, target)
            except:
                print(f'{sub} not found')
