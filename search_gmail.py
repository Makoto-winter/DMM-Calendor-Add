from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64

email_bodies = []
booked_classes_info = []

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://mail.google.com/']


def getEmails():
	# Variable creds will store the user access token.
	# If no valid token found, we will create one.
	creds = None

	# The file token.pickle contains the user access token.
	# Check if it exists
	if os.path.exists('token.pickle'):

		# Read the token from the file and store it in the variable creds
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)

	# If credentials are not available or are invalid, ask the user to log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)

		# Save the access token in token.pickle file for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	# Connect to the Gmail API
	service = build('gmail', 'v1', credentials=creds)

	# request a list of all the messages
	# messages is a list of dictionaries where each dictionary contains a message id.
	# the maximum messages are set to 3.
	result = service.users().messages().list(maxResults=3, userId='me', q="subject:Lesson Booking newer_than:17d").execute()
	messages = result.get('messages')

	# Use try-except to avoid any Errors
	try:
		# iterate through all the messages
		for message in messages:
			# getting the message with IDs that we got in the variable, result.
			msg = service.users().messages().get(userId="me", id=message["id"]).execute()
			# trashing the message in order not to add the same class in the future.
			service.users().messages().trash(userId="me", id=message["id"]).execute()
			# print the body of the email
			email_body = base64.urlsafe_b64decode(msg["payload"]["parts"][0]["parts"][0]["body"]["data"]).decode("utf-8")
			# adding the email body to an array.
			global email_bodies
			email_bodies.append(email_body)
	except Exception as e:
		print(e)


def GetTeacherNamesAndTimes():
	try:
		# splitting email_bodies' text to get the teacher name and date/time for a booked class.
		global email_bodies
		for email in email_bodies:
			teacher_name = email.split("with Teacher ")[1].split(" for ")[0]
			lesson_time = email.split("with Teacher ")[1].split(" for ")[1].split(".")[0]
			global booked_classes_info
			booked_classes_info.append({"teacher": teacher_name, "time": lesson_time})
		print(booked_classes_info)
	except Exception as e:
		print(e)

