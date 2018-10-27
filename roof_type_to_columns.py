import sys
import numpy as np
import pandas as pd


if __name__ == '__main__':
    file_name = sys.argv[1]

    df = pd.read_csv(file_name)

    df['inappropriate_type'] = df['roof_tupe'].map(
        lambda x: 1 if x == 'inappropriate' else 0
    )

    df['flat_roof'] = df['roof_tupe'].map(
        lambda x: 1 if x == 'flat' else 0
    )

    df['gabled_roof'] = df['roof_tupe'].map(
        lambda x: 1 if x == 'gabled' else 0
    )

    df['round_roof'] = df['roof_tupe'].map(
        lambda x: 1 if x == 'round' else 0
    )

    df.pop('roof_tupe')

    df.to_csv(file_name)
