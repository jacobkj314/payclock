#!/usr/bin/python3
import datetime
from sys import argv
from os.path import exists

ACTIVE = True
TIME_FORMAT = "%Y/%m/%d %H:%M:%S"
LOG_LIST = None
LOG_FILE = None
WORKING = False

def write_file(filename, string):
    with open(filename, "a") as file:
        file.write(string)

def read_log(log_file):
    global LOG_LIST, WORKING
    LOG_LIST = list()
    with open(log_file) as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip('\n')
            if line == '':
                continue
            day, start, *end = line.strip(' ').split(' ')
            end = end[0] if end else None
            LOG_LIST.append ([
                                day, 
                                datetime.datetime.strptime(f"{day} {start}", TIME_FORMAT), 
                                datetime.datetime.strptime(f"{day} {end}",   TIME_FORMAT) if end is not None else None, 
                            ])  
        WORKING = True if (len(LOG_LIST) > 0 and LOG_LIST[-1][-1] is None) else False #whether I am working or not
def write_log(dt, date, time, is_start):
    global LOG_LIST, LOG_FILE
    if is_start:
        LOG_LIST.append([date, dt, None])
        write_file(LOG_FILE, f"{date} {time}")
    else: # is end
        LOG_LIST[-1][-1] = dt
        write_file(LOG_FILE, f" {time}\n")
def has_log():
    global LOG_LIST, LOG_FILE
    return not (LOG_LIST is None or LOG_FILE is None)

def get_date_time():
    dt = datetime.datetime.now()
    date, time = dt.strftime(TIME_FORMAT).split()
    return dt, date, time

def get_log():
    global WORKING, LOG_LIST
    log = LOG_LIST
    if not WORKING:
        return log
    current_entry = log[-1][:-1] + [datetime.datetime.now()]
    return log[:-1] + [current_entry]
def get_report():
    log_to_report = get_log()
    report = dict()
    for date, start, end in log_to_report:
        if date not in report.keys():
            report[date] = 0.0
        report[date] = report[date] + (end - start).seconds / 3600
    return report



def START():
    global WORKING, LOG_LIST
    if not has_log():
        return False, "No active log file! Use `log <filename>` to set"
    if WORKING:
        return False, f"You are already clocked in since {LOG_LIST[-1][1].strftime(TIME_FORMAT)}"
    WORKING = True
    dt, date, time = get_date_time()
    write_log(dt=dt, date=date, time=time, is_start=True)
    return True, f"On since {time}"
def END():
    global WORKING
    if not has_log():
        return False, "No active log file! Use `log <filename>` to set"
    if not WORKING:
        return False, f"You are already clocked out since {LOG_LIST[-1][2].strftime(TIME_FORMAT)}"
    WORKING = False
    dt, date, time = get_date_time()
    write_log(dt=dt, date=date, time=time, is_start=False)
    start_time = LOG_LIST[-1][1]
    duration = (dt - start_time).seconds / 3600
    return True, f"Off since {time}, after having worked {duration : .8f} hours"
def CLEAR():
    return True, "\033[2J\033[H"
def LOG(file=None, *other_args):
    global LOG_FILE, LOG_LIST
    if file is None:
        log_file = LOG_FILE
        LOG_FILE = LOG_LIST = None
        return True, f"Disconnected from log file {log_file}"
    LOG_FILE = file
    if not exists(file):
        with open(file, 'w') as writer:
            pass
    read_log(LOG_FILE)
    return True, f"Now writing to log file {LOG_FILE}"
def STATE():
    if not has_log():
        return False, "No active log file! Use `log <filename>` to set"
    return True, f"You are clocked {'in' if WORKING else 'out'}{f' since {LOG_LIST[-1][1 if WORKING else 2].strftime(TIME_FORMAT)}' if len(LOG_LIST) > 0 else ''}"
def REPORT():
    global LOG_LIST
    if not has_log():
        return False, "No active log file! Use `log <filename>` to set"
    output_list = list()
    for date, duration in get_report().items():
        output_list.append(f"{duration} hours worked on date {date}")
    return True, ('\n'.join(output_list) if len(LOG_LIST) > 0 else 'No worked times to report')
def TOTAL():
    if not has_log():
        return False, "No active log file! Use `log <filename>` to set"
    total = 0.0
    for _, duration in get_report().items():
        total += duration
    return True, f"{total} hours worked since begin of log {LOG_FILE}"
def EXIT():
    global ACTIVE
    ACTIVE = False
    return True, None

COMMANDS =  {   "start" :   START, 
                "end"   :   END,
                "log"   :   LOG,
                "clear" :   CLEAR,
                "state" :   STATE,
                "total" :   TOTAL,
                "report":   REPORT,
                "exit"  :   EXIT,

            }

def RUN_COMMAND(full_command):
    command, *args = full_command.split()
    known_command = command in COMMANDS
    output_color = command_color = "31" ; output = f'Unknown command "{command}"'
    command_symbol = "❌"
    if known_command:
        run_complete, output = COMMANDS[command](*args)
        if run_complete:
            command_color = "32" ; output_color = "0"
            command_symbol = "✅"
        else: #run failed
            command_color = output_color = "33"
            command_symbol = "❓"

    print(f"\033[F{command_symbol} \033[{command_color}m{full_command}\033[0m")
    if output is not None:
        output = output.strip('\n')
        print(f"\033[{output_color}m{output}\033[0m")

def main():
    #try to get log_file from arguments
    if len(argv) > 1:
        LOG(argv[1])
    
    while ACTIVE:
        command = input('> ')
        if command == "":
            command = "end" if WORKING else "start"
        RUN_COMMAND(command)


    

if __name__ == "__main__":
    main()