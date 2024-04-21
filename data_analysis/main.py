import pyphysio as ph
import pyphysio.filters as flt
import pyphysio.specialized.heart as heart_tools
from pyphysio.indicators import compute_indicators
import pandas as pd
import os

def analyze_ecg(filename,folder_path='data_analysis/data/'):
    print(f'Analyzing {filename}')
    title_without_ext = filename.split('.')[0]
    userID, paintingID, mode = title_without_ext.split('_')
    mode = 'Baseline' if mode == 'B' else 'Stress'

    # Read the data from the file
    data = pd.read_table(f'{folder_path}/{filename}',
                         skiprows=3,
                         sep='\t')

    # Flatten the fifth column (ECG values) and convert it to a numpy array
    ecg_values = data.values[:,5]

    signal = ph.create_signal(ecg_values, sampling_freq=1000)

    # Compute HRV indicators
    td_indicators = heart_tools.preset_hrv_td() #time-domain indicators
    fd_indicators = heart_tools.preset_hrv_fd() #frequency-domain indicators

    signal = flt.IIRFilter([3, 45], btype='bandpass')(signal)
    ibi = heart_tools.BeatFromECG()(signal)
    ibi = ibi.p.process_na('remove', 'remove')

    indicators_td = compute_indicators(td_indicators, ibi)
    indicators_fd = compute_indicators(fd_indicators, ibi.p.resample(4))

    all_indicators = {'userId': userID, 'paintingId': paintingID, 'mode': mode,**indicators_td, **indicators_fd}
    return all_indicators

def main():
    # Get all the files in the data folder
    files = os.listdir('data_analysis/data')
    all_indicators = []
    for file in files:
        if file.endswith('.txt'):
            all_indicators.append(analyze_ecg(file))
    df = pd.DataFrame(all_indicators)
    df.to_csv('data_analysis/hrv.csv', index=False)

if __name__ == '__main__':
    main()
    
    
    