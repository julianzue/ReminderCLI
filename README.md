# ReminderCLI

## Description
- With this cli program written in python, you can create reminders for the day.
- When the time is up, you get a notification.
- You can create a new Reminder with the "new" command.
  ```
  python3 app.py new --name 'Test' -t 10:30
  ```
- You can show all reminders with the "show" command.
  ```
  python3 app.py show
  ```
- If you want to delete a reminder you can use the "delete" command.
  ```
  python3 app.py delete --index 1
  ```
- With the "live" command you can see the still open reminders and you get the notifications
  ```
  python3 app.py live
  ```

## Requirements
- colorama
- click
- rich

## Platform
- Linux
