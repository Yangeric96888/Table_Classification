import pandas as pd
from UnclassifiedTable import UnclassifiedTable
from glob import glob

# Iterate through file names
if __name__ == '__main__':

    # Correlation database
    print('''
    ---Correlation---
    ''')
    for i in range(18):
        print("###")
        print(i)
        currentFile = pd.read_csv(glob("apr_correlation_predicted/*.csv")[i])
        currentFile = UnclassifiedTable(currentFile)
        print(currentFile.classify_table())

    # Regression database
    print(''''
    ---Regression---
    ''')
    for i in range(23):
        print("###")
        print(i)
        currentFile = pd.read_csv(glob("apr_regression_predicted/*.csv")[i])
        currentFile = UnclassifiedTable(currentFile)
        print(currentFile.classify_table())
