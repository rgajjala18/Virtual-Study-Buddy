#!/usr/bin/env python

"""
    Script to import book data from .csv file to Model Database DJango
    To execute this script run: 
                                1) manage.py shell
                                2) exec(open('import_course_data.py').read())
"""

import pandas as pd
from study_buddy.models import Course
import requests
import json

url = 'https://api.devhub.virginia.edu/v1/courses'
data = requests.get(url).json()

columns = data['class_schedules']['columns']
courses = data['class_schedules']['records']

df = pd.DataFrame(courses, columns=columns)
df = df[df['catalog_number'] < '5000']
df = df.drop_duplicates(subset=['subject', 'catalog_number'])

contSuccess = 0
# Remove all data from Table
Course.objects.all().delete()

for index, row in df.iterrows():
    Course.objects.create(
        prefix=row['subject'], number=row['catalog_number'], title=row['class_title'])
    contSuccess += 1
print(f'{str(contSuccess)} inserted successfully! ')
