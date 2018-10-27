import sys
import numpy as np
import pandas as pd


if __name__ == '__main__':
    file_name = sys.argv[1]

    df = pd.read_csv(file_name)

    df['roof_tupe'] = df['temperature'].map(lambda x: np.random.choice(
        ['', 'flat', 'gabled', 'round', 'inappropriate'],
        p=[0.8, 0.12, 0.04, 0.02, 0.02]
    ))

    df.to_csv(file_name)
