import datetime

from sys import argv
log_file = argv[1]

def write(string):
	with open(log_file, "a") as file:
		file.write(string)

log= list()
with open(log_file) as file:
	lines = file.readlines()
	for line in lines:
		line = line.strip('\n')
		if line == '':
			continue
		day, start, *end = line.strip(' ').split(' ')
		end = end[0] if end else None
		log.append	([
					day, 
					datetime.datetime.strptime(f"{day} {start}", "%d %H%M"), 
					datetime.datetime.strptime(f"{day} {end}",  "%d %H%M") if end is not None else None, 
				])
	state = True if (len(log) > 0 and log[-1][-1] is None) else False #whether I am working or not


while True:
	command = input()
	
	if command == 'report':
		log_to_report = log[:-1] if state else log
		report = dict()
		for date, start, end in log_to_report:
			if date not in report.keys():
				report[date] = 0.0
			report[date] = report[date] + (end - start).seconds / 3600
		for date, duration in report.items():
			print(f"{duration} hours worked on date {date}")
	elif command == 'total':
		log_to_report = log[:-1] if state else log
		total = 0.0
		for date, start, end in log_to_report:
			total += (end - start).seconds / 3600
		print(f"{total} hours worked since begin of log")
	elif command == "state":
		print(f"You are {('' if state else 'NOT ')}on the clock")
	elif command == "exit":
		break
	else:
		dt = datetime.datetime.now()
		date, time = dt.strftime("%d %H%M").split(' ')
		state = not state

		if state: # if I just started
			log.append([date, dt, None])
			write(f"{date} {time}")
			print(f"On since {time}", end='')
				
		else:	#if I just ended
			log[-1][-1] = dt
			start_time = log[-1][1]
			duration = (dt - start_time).seconds / 3600
			write(f" {time}\n")
			print(f"Off since {time}, after having worked {duration : .8f} hours", end='')
		
