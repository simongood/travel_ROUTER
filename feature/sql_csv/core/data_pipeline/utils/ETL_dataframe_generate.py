import pandas as pd

def ETL_dataframe_generate(filepath = 'data/ETL_dataframe.csv'):
    ETL_dataframe = pd.read_csv(filepath, index_col='place_id')
    return ETL_dataframe


if __name__ == '__main__' :
    ETL_dataframe = ETL_dataframe_generate()
    print(ETL_dataframe)