import pandas as pd
from CSEPcon.settings import DIR

def importDataValue(fileName):
    data = pd.read_csv(DIR + "paquete/csv/"+ fileName)
    a = data.to_dict("records")
    return a