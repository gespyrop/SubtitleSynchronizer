"""
I had to adjust the (unsynchronized) subtitles
of a video every time I opened VLC.
With this program I can change the subtitles' file permanently
and delay the subtitles by a specific amount of time.
"""

from sys import argv

if len(argv) == 1: 
	file = raw_input("\nEnter subtitles file name: ")
else:
	file = argv[1]

if file[-4:] not in [".srt", ".txt"]:
	file += ".srt"

def stringFixer(num):
	if num < 10 and num > 0:
		return "0" + str(num)
	elif num >= 10:
		return str(num)
	else:
		return "00"

def timeIncrease(time, shiftTime):
	print(time)
	try:
		newSec = int(time[6:8]) + shiftTime
		increaseMin = 0
		if newSec < 60:
			newSec = stringFixer(newSec)
		else:
			increaseMin = newSec / 60
			newSec = stringFixer(newSec % 60)

		newMin = int(time[3:5]) + increaseMin
		increaseHr = 0
		if newMin < 60:
			newMin = stringFixer(newMin)
		else:
			increaseHr = newMin / 60
			newMin = stringFixer(newMin % 60)
		
		newHr = int(time[:2]) + increaseHr
		newHr = stringFixer(newHr)

		return newHr + ":" + newMin + ":" + newSec
	except ValueError:
		print "\nError: Invalid time format! (%s)" % time
		exit(1)

def timeToSec(time):
	return int(time[6:8]) + int(time[3:5]) * 60 + int(time[:2]) * 3600


try:
	with open(file, "r") as f:
		shiftTime = int(raw_input("\n(In seconds)\nDelay subtitles by: "))
		lines = f.readlines()

		checkIndex = 0
		while "-->" not in lines[checkIndex]:
			checkIndex += 1

		firstSubStart = lines[checkIndex][:lines[checkIndex].find("-") - 5]
		if (timeToSec(firstSubStart) + shiftTime) < 0:
			print "\nError: Subtitles might go out of sync!\n"
			exit()

		for line in lines:
			index = lines.index(line)
			if "-->" in line:
				startTime = line[:line.find("-") - 5]
				endTime = line[line.find(">") + 2:-6]

				newStartTime = timeIncrease(startTime, shiftTime)
				newEndTime = timeIncrease(endTime, shiftTime)

				if(shiftTime > 0):
					line = line.replace(endTime, newEndTime)
					line = line.replace(startTime, newStartTime)
				else:
					line = line.replace(startTime, newStartTime)
					line = line.replace(endTime, newEndTime)

				lines[index] = line		

	with open(file, "w") as f:
		for line in lines:
			f.write(line)
		print "\nSubtitles synchronized!\n"

except IOError:
	print "\nError: File not found!\n"
