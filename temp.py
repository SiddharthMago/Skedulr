import pandas as pd
from datetime import datetime, timedelta, time
FILE_PATH = "/Users/mago/Desktop/Projects/scheduler/static/xls"

kadambdf = pd.read_excel(FILE_PATH + '/kadamb.xlsx')
kadambdf.columns = kadambdf.columns.str.strip()

northdf = pd.read_excel(FILE_PATH + '/north.xlsx')
northdf.columns = northdf.columns.str.strip()

southdf = pd.read_excel(FILE_PATH + '/south.xlsx')
southdf.columns = southdf.columns.str.strip()

yukdf = pd.read_excel(FILE_PATH + '/yuktahaar.xlsx')
yukdf.columns = yukdf.columns.str.strip()

df = pd.read_excel(FILE_PATH + '/courses.xlsx')
df.columns = df.columns.str.strip()

df['Semester'] = df['Semester'].astype(str).str.strip()
filtered_df = df[df['Semester'] == str(1)]
data_list = filtered_df.to_dict(orient='records')
for row in data_list:
    code = row['Course Code']
    course = row['Course']
    course = code + ' - ' + course
    prof = row['Prof']
    days = row['Day']
    days = days.split(',')
    room = row['Room']
    start = row['Start']
    end = row['End']
    start_time = datetime.strptime(start, '%H:%M').time()
    end_time = datetime.strptime(end, '%H:%M').time()

    print(start_time, end_time)

day_map = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4, 'SA': 5, 'SU': 6}
breakfast_time = {'start': time(7, 30), 'end': time(8, 0)}
lunch_time = {'start': time(12, 30), 'end': time(13, 30)}
dinner_time = {'start': time(20, 0), 'end': time(21, 0)}

for index, row in kadambdf.iterrows():
    meal_type = row['x']
    print(meal_type)
    for day, day_code in day_map.items():
        meal_description = row[day]
        if meal_type == 'BR':
            start_time = breakfast_time['start']
            end_time = breakfast_time['end']
        elif meal_type == 'LU':
            start_time = lunch_time['start']
            end_time = lunch_time['end']
        elif meal_type == 'DI':
            start_time = dinner_time['start']
            end_time = dinner_time['end']

        # now = datetime.utcnow()
        # start_date = now + timedelta((day_map[day] - now.weekday() + 7) % 7)
        # start_datetime = datetime.combine(start_date, start_time) + timedelta(hours=5, minutes=30)
        # end_datetime = datetime.combine(start_date, end_time) + timedelta(hours=5, minutes=30)

        print(start_time, end_time)