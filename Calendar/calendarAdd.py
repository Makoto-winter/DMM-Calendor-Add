from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

StartTime = ""
EndTime = ""


def MonthAbbReturnNum(abb):
    if abb == "January":
        return "01"
    elif abb == "February":
        return "02"
    elif abb == "March":
        return "03"
    elif abb == "April":
        return "04"
    elif abb == "May":
        return "05"
    elif abb == "June":
        return "06"
    elif abb == "July":
        return "07"
    elif abb == "August":
        return "08"
    elif abb == "September":
        return "09"
    elif abb == "October":
        return "10"
    elif abb == "Nobember":
        return "11"
    elif abb == "December":
        return "12"


def timeFormatChange(initial_format):
    """
    This function changes the date format
    from: August 09, 2023 10:30
    to: 2023-08-09T13:00:00
    """

    time_array = initial_format.split(" ")
    global StartTime
    StartTime = time_array[2] + "-" + MonthAbbReturnNum(time_array[0]) + "-" + time_array[1].split(",")[0] + "T" \
                + time_array[3] + ":00"

    end_minute = int(time_array[3].split(":")[1]) + 25
    end_hour_and_minute = time_array[3].split(":")[0] + ":" + str(end_minute)
    global EndTime
    EndTime = time_array[2] + "-" + MonthAbbReturnNum(time_array[0]) + "-" + time_array[1].split(",")[0] + "T" \
              + end_hour_and_minute + ":00"


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def CalendarAdd(teacher, lesson_time):
    """
    This function needs two parameters, teacher and LessonTime.

    :param lesson_time: lesson start time
    :param teacher: teacher's name
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        summary_text = "DMM Lesson with " + teacher
        global StartTime
        global EndTime
        # change the time format of two global variables, StartTime and EndTime.
        timeFormatChange(lesson_time)
        event = {
            'summary': summary_text,
            'start': {
                'dateTime': StartTime,
                # You can do "Asia/Tokyo" too if you are in Tokyo.
                'timeZone': "America/Toronto",
            },
            'end': {
                'dateTime': EndTime,
                'timeZone': "America/Toronto",
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    # Two email notifications, 60 minutes and 120 minutes before a lesson
                    {'method': 'email', 'minutes': 2 * 60},
                    {'method': 'email', 'minutes': 60},
                ],
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print('An error occurred: %s' % error)

