import search_gmail
import Calendar.calendarAdd as add

search_gmail.getEmails()
search_gmail.GetTeacherNamesAndTimes()

# booked_classes_info is a nested list that includes teacher's name and lesson time for maximum 3 classes.
# [
# {'teacher': 'Sabya', 'time': 'August 04, 2023 08:30'},
# {'teacher': 'Jason M', 'time': 'August 02, 2023 21:30'},
# {'teacher': 'Shawn', 'time': 'August 01, 2023 22:30'}
# ]
for nth_class in search_gmail.booked_classes_info:
    add.CalendarAdd(nth_class['teacher'], nth_class['time'])

