import pandas as pd

regions = pd.read_csv('regions.csv')

regions = dict(regions.groupby('question_eng')['region_name_latin'].unique())
