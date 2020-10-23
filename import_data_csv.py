#!/usr/bin/env python

"""
    Script to import book data from .csv file to Model Database DJango
    To execute this script run: 
                                1) manage.py shell
                                2) exec(open('import_data_csv.py').read())
"""

import csv
import pandas as pd
from study_buddy.models import Course

CSV_PATH = 'searchData.csv'

df = pd.read_csv(CSV_PATH)
df = df.drop_duplicates(subset=['Mnemonic', 'Number'])

contSuccess = 0
# Remove all data from Table
Course.objects.all().delete()

for index, row in df.iterrows():
    Course.objects.create(
        prefix=row['Mnemonic'], number=row['Number'], title=row['Title'])
    contSuccess += 1
print(f'{str(contSuccess)} inserted successfully! ')


'''
with open(CSV_PATH, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar=';')
    print('Loading...')
    for row in spamreader:
        Course.objects.create(prefix=row[1], number=row[2])
        contSuccess += 1
    #print(f'{str(contSuccess)} inserted successfully! ')
'''
