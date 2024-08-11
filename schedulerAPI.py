import os
import pickle
import pandas as pd
from datetime import datetime, timedelta, time
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from flask import Flask, render_template, redirect, flash
import pathlib

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__, static_folder='static', template_folder='templates')
BASE_DIR = pathlib.Path(__file__).parent.resolve()

# Define file paths dynamically
FILE_PATH = os.path.join(BASE_DIR, 'static', 'xls')
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials.json')
TOKEN_PATH = os.path.join(BASE_DIR, 'token.pickle')

df = pd.read_excel(os.path.join(FILE_PATH, 'courses.xlsx'))
df.columns = df.columns.str.strip()

@app.route('/')
def init():
    return render_template("main.html", wait=True)

@app.route('/Courses')
def courses():
    filtered_df = df[['Semester', 'Course Code', 'Course']]
    course_list = filtered_df.to_dict(orient='records')
    return render_template("main.html", courses=course_list)

@app.route('/Courses/<int:semester>')
def sem_courses(semester):
    df['Semester'] = df['Semester'].astype(str).str.strip()
    filtered_df = df[df['Semester'] == str(semester)]
    filtered_df = filtered_df[['Course Code', 'Course']]
    semcourses = filtered_df.to_dict(orient='records')
    return render_template("main.html", semcourses=semcourses)

@app.route('/Courses/<string:course_code>')
def course_dets(course_code):
    filtered_df = df[df['Course Code'] == str(course_code)]
    course_details = filtered_df.to_dict(orient='records')
    course_details = course_details[0]
    return render_template("main.html", course_details=course_details)

# Calendar Scheduling:
SCOPES = ['https://www.googleapis.com/auth/calendar']
COURSE_CALENDAR_SUMMARY = 'Courses by Scheduler'
MESS_CALENDAR_SUMMARY = 'Mess by Scheduler'
TIMEZONE = 'Asia/Kolkata'
day_map = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4, 'SA': 5, 'SU': 6}

# Load mess data from Excel files
kadambdf = pd.read_excel(os.path.join(FILE_PATH, 'kadamb.xlsx'))
kadambdf.columns = kadambdf.columns.str.strip()

northdf = pd.read_excel(os.path.join(FILE_PATH, 'north.xlsx'))
northdf.columns = northdf.columns.str.strip()

southdf = pd.read_excel(os.path.join(FILE_PATH, 'south.xlsx'))
southdf.columns = southdf.columns.str.strip()

yukdf = pd.read_excel(os.path.join(FILE_PATH, 'yuktahaar.xlsx'))
yukdf.columns = yukdf.columns.str.strip()

def authcheck():
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_calendar_id(service, summary):
    calendars = service.calendarList().list().execute()
    for calendar in calendars['items']:
        if calendar['summary'] == summary:
            return calendar['id']
    return None

def delete_calendar(service, calendar_id):
    try:
        service.calendars().delete(calendarId=calendar_id).execute()
        print(f'Calendar deleted: {calendar_id}')
    except Exception as e:
        print(f'Error deleting calendar: {e}')

def create_calendar(service, summary):
    calendar = {
        'summary': summary,
        'timeZone': TIMEZONE
    }
    created_calendar = service.calendars().insert(body=calendar).execute()
    print(f'Calendar created: {created_calendar["id"]}')
    return created_calendar['id']

def create_event(service, calendar_id, summary, location, description, day, day_of_week, start_time, end_time):
    now = datetime.utcnow()
    start_date = now + timedelta((day - now.weekday() + 7) % 7)
    end_date = start_date

    start_datetime = datetime.combine(start_date, start_time) + timedelta(hours=5, minutes=30)
    end_datetime = datetime.combine(end_date, end_time) + timedelta(hours=5, minutes=30)

    print(f"Creating event: {summary}")
    print(f"Start time: {start_datetime} (UTC: {start_datetime.isoformat()})")
    print(f"End time: {end_datetime} (UTC: {end_datetime.isoformat()})")

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': TIMEZONE,
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': TIMEZONE,
        },
        'recurrence': [
            f'RRULE:FREQ=WEEKLY;BYDAY={day_of_week};UNTIL={end_datetime.year}1231T235959Z'
        ]
    }

    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f"Created event: {created_event['id']}")
    print()

def create_mess_events(service, calendar_id, df, mess_name):
    breakfast_time = {'start': time(7, 30), 'end': time(8, 0)}
    lunch_time = {'start': time(12, 30), 'end': time(13, 30)}
    dinner_time = {'start': time(20, 0), 'end': time(21, 0)}

    for index, row in df.iterrows():
        meal_type = row['x']
        for day, daynum in day_map.items():
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

            create_event(service, calendar_id, mess_name, meal_type, meal_description, daynum, day, start_time, end_time)

@app.route('/Schedule/<int:semester>')
def schedule(semester):
    creds = authcheck()
    service = build('calendar', 'v3', credentials=creds)

    existing_calendar_id = get_calendar_id(service, COURSE_CALENDAR_SUMMARY)
    if existing_calendar_id:
        delete_calendar(service, existing_calendar_id)

    calendar_id = create_calendar(service, COURSE_CALENDAR_SUMMARY)

    df['Semester'] = df['Semester'].astype(str).str.strip()
    filtered_df = df[df['Semester'] == str(semester)]
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

        print("--------------------------------------------")
        print(f"Course: {course}")
        print(f"Start time: {start_time}")
        print(f"End time: {end_time}")

        for day in days:
            daynum = day_map[day]
            create_event(service, calendar_id, course, room, ('Prof. ' + prof), daynum, day, start_time, end_time)

    existing_calendar_id = get_calendar_id(service, MESS_CALENDAR_SUMMARY)
    if existing_calendar_id:
        delete_calendar(service, existing_calendar_id)

    calendar_id = create_calendar(service, MESS_CALENDAR_SUMMARY)

    create_mess_events(service, calendar_id, kadambdf, 'Kadamb')
    create_mess_events(service, calendar_id, northdf, 'North')
    create_mess_events(service, calendar_id, southdf, 'South')
    create_mess_events(service, calendar_id, yukdf, 'Yuktahaar')

    return redirect('https://calendar.google.com/calendar')

if __name__ == '__main__':
    app.run(debug=True)
