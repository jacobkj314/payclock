# Shift Timer

This is a simple CLI clock for clocking in and out of hourly remote jobs. 


Here are all commands used by my shift clock:

log: use log <filename> to set the file that will be used to log your times clocking in and out. The filename may not contain spaces.

The format is human readable and consists of the day, the start time, then the end time (each on a new line) with the days represented as year/month/day, and times represented as hour:minute:second

The log file can also be selected while running the program using a command line argument:  `python clock.py <filename>`.

Running log without an argument will print the full log


in/start: This will clock you in. Ensure that you have selected a log file before running this

out/end: This will clock you out. Ensure that you have selected a log file before running this.

Simply pressing enter without typing a command will automatically send the appropriate clock in/out command. If you are already clocked in, it will clock you out, and vice-versa.


state: This indicates whether you are clocked in or out.

report: This totals up hours worked by day and prints out a summary for each day

total: This totals up all hours worked in your current log file


clear: This clears the screen


exit: This exits the program. Because all hours are logged in your selected file, you can exit the program, even if you are clocked in