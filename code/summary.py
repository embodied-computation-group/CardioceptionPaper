import pandas as pd
import numpy as np
from metadPy.sdt import rates, dprime, criterion
from metadPy.utils import trials2counts, discreteRatings
from systole.detection import rr_artefacts


def groupLevel(datapath, subjects, verbose=True):
    """Extract summary statistics"""

    ####################
    # Summary statistics
    ####################
    group_df = pd.DataFrame([])  # Group level summary
    for session in ['Del1', 'Del2']:
        sess = '_del2' if session == 'Del2' else ''
        for sub in subjects:
            if session == 'Del1':
                # Heart Beat Counting
                try:
                    df = pd.read_csv(f'{datapath}{sub}/HBC/HBC_final.txt')
                    beats = []
                    for i in range(6):
                        ppg = np.load(f'{datapath}{sub}/HBC/{sub[4:]}_{i}.npy')
                        nRR = sum(ppg[1])

                        # Check for artefacts
                        artefacts = rr_artefacts(np.diff(np.where(ppg[1])[0]) * (1000/75))
                        if np.any([np.any(artefacts['missed'])]):
                            n = sum(artefacts['missed'])
                            if verbose:
                                print(f'Subject {sub} - Recording {i} - {n} missed beat')
                            nRR += n
                        if np.any([np.any(artefacts['extra'])]):
                            n = sum(artefacts['extra'])
                            if verbose:
                                print(f'Subject {sub} - Recording {i} - {n} extra beat')
                            nRR -= n

                        beats.append(nRR)
                    df['Beats'] = beats
                    hbc_score = ((df.Beats - df.Reported).abs() / ((df.Beats + df.Reported)/2)).mean()
                except:
                    hbc_score = np.nan

            # Heart Rate Discrimination
            try:
                df = pd.read_csv(f'{datapath}{sub}/HRD{sess}/HRD{sess}_final.txt')       
                taskDuration = (df['StartListening'].iloc[-1] - df['StartListening'].iloc[0])/60

                if 'StartListening' in df.columns:
                    df = df.drop('StartListening', axis=1)

                resp = 'Estimation' if session == 'Del1' else 'Decision'

                for modality in ['Intero', 'Extero']:
                    if session == 'Del1':
                        this_df = df[df.Modality == modality]
                    else:
                        this_df = df[(df.Modality == modality) & (df.TrialType == 'psi')]

                    threshold, slope = this_df.EstimatedThreshold.iloc[-1], this_df.EstimatedSlope.iloc[-1]
                    estimationRT, confidenceRT = this_df[f'{resp}RT'].median(), this_df.ConfidenceRT.median()
                    accuracy, confidence = this_df['ResponseCorrect'].mean() * 100, this_df['Confidence'].mean()

                    # SDT
                    hit = sum((this_df.responseBPM > this_df.listenBPM) & (this_df[resp] == 'More'))
                    miss = sum((this_df.responseBPM > this_df.listenBPM) & (this_df[resp] == 'Less'))
                    fa = sum((this_df.responseBPM < this_df.listenBPM) & (this_df[resp] == 'More'))
                    cr = sum((this_df.responseBPM < this_df.listenBPM) & (this_df[resp] == 'Less'))
                    hr, far = rates(hit, miss, fa, cr)
                    d, c = dprime(hr, far), criterion(hr, far)

                    group_df = group_df.append({'Subject': sub,
                                                'Session': session,
                                                'Modality': modality,
                                                'Accuracy': accuracy,
                                                'Confidence': confidence,
                                                'Threshold': threshold,
                                                'Slope': slope,
                                                'TaskDuration': taskDuration,
                                                'DecisionRT': estimationRT,
                                                'ConfidenceRT': confidenceRT,
                                                'dPrime': d,
                                                'Criterion': c,
                                                'HBC': hbc_score}, ignore_index=True)
            except:
                if verbose:
                    print(f'Subject: {sub} not found')

    ##################
    # Concatenate data
    ##################
    merged_df = pd.DataFrame([])  # Concatenated raw data
    for sub in subjects:
        for session in ['Del1', 'Del2']:
            sess = '_del2' if session == 'Del2' else ''
            # Heart Rate Discrimination
            try:
                df = pd.read_csv(f'{datapath}{sub}/HRD{sess}/HRD{sess}_final.txt')
                if 'StartListening' in df.columns:
                    df = df.drop('StartListening', axis=1)
                df['Subject'] = sub
                df['Session'] = session 
                merged_df = merged_df.append(df, ignore_index=True)
            except:
                if verbose:
                    print(f'Error with subject: {sub}')

    return group_df, merged_df