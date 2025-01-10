import os
import pickle
import pathlib
import pandas as pd
from datetime import datetime, timedelta, time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

BASE_DIR = pathlib.Path(__file__).parent.resolve()

# Define file paths dynamically
FILE_PATH = os.path.join(BASE_DIR, 'static', 'xls')
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_SUMMARY = 'Courses by Scheduler'
TIMEZONE = 'Asia/Kolkata'

def authcheck():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
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

def main():
    creds = authcheck()
    service = build('calendar', 'v3', credentials=creds)

    existing_calendar_id = get_calendar_id(service, CALENDAR_SUMMARY)
    if existing_calendar_id:
        delete_calendar(service, existing_calendar_id)

    calendar_id = create_calendar(service, CALENDAR_SUMMARY)

    semester = input("Enter your semester: ")

    df = pd.read_excel(FILE_PATH + '/courses.xlsx')
    df.columns = df.columns.str.strip()
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

        day_map = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4, 'SA': 5, 'SU': 6}
        for day in days:
            daynum = day_map[day]
            create_event(service, calendar_id, course, room, ('Prof. ' + prof), daynum, day, start_time, end_time)

if __name__ == '__main__':
    main()
