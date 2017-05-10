#f1Scraper by ChrisTheCameraMan

#Script downloads all Formula1 Program Covers From StatsF1.com
#When run again will read f1Scraper.cfg and start from the last successful download
#Also creates log file f1Scraper.log which will advise which files have been downloaded

import urllib
import os
import logging
import os.path
import ConfigParser


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='f1Scraper.log',
                    filemode='w')

logging.info('-----Script Started-----')

if (not os.path.isfile('f1Scraper.cfg')):
	logging.info('No config file. Creating new config file.')
	config = ConfigParser.RawConfigParser()
	config.add_section('LastFile')
	config.set('LastFile', 'gpNum', '0')
	config.set('LastFile', 'year', '1950')
	config.set('LastFile', 'racecount', '0')
	with open('f1Scraper.cfg', 'wb') as configfile:
    		config.write(configfile)
	logging.info('New config file created. Downloading from start')
else:
	logging.info('Config File Found. Starting From Last Successful Download')

config = ConfigParser.RawConfigParser()
config.read('f1Scraper.cfg')

#Iterators start at last case + 1
gpNum = 1 + config.getint('LastFile', 'gpNum') #GP Number (all time)
year = config.getint('LastFile', 'year') #Year of GP
racecount = 1 + config.getint('LastFile', 'racecount') #Race in season

#last successful cases
lastGPNum = config.getint('LastFile', 'gpNum')
lastYear = config.getint('LastFile', 'year')
lastRace = config.getint('LastFile', 'racecount')

#Images are found at the url http://statsf1.free.fr/photos/gp/<year>/<gpNum>a.jpg
starturl = "http://statsf1.free.fr/photos/gp/" 
endurl = "a.jpg"





#count strikes for unsuccessful cases
raceStrike = 0
yearStrike = 0

newImages = 0

while (True):
	#Download image to this directory in the format s<year>e<racecount>.jpg
	urllib.urlretrieve(starturl + str(year) + "/" + str(gpNum) + endurl, "s" + str(year) + "e" + '%02d' % racecount + ".jpg")
	
	#Open file and save first line, close file
	infile = open("s" + str(year) + "e" + '%02d' % racecount + ".jpg", 'r')
	first_line = infile.readline()
	infile.close()
	
	#Check file to see if it is a html
	if (first_line[:14] == "<!DOCTYPE html"):
		#Delete html file
		os.remove("s" + str(year) + "e" + '%02d' % racecount + ".jpg")
		#Log result
		logging.warning(str(gpNum) + " " + "s" + str(year) + "e" + '%02d' % racecount + ".jpg" + " Does Not Exist")
		#Try next three races in same year
		if (raceStrike < 2):
			gpNum += 1
			racecount += 1
			raceStrike +=1
		#Go to next year
		elif (raceStrike == 2 and yearStrike == 0):
			gpNum = lastGPNum + 1
			year += 1
			racecount = 1
			raceStrike = 0
			yearStrike = 1
		#End of script. No more posters.
		else:
			break
		#Jump back to loop unsuccessful case
		continue
	#log successful case
	logging.info(str(gpNum) + " " + "s" + str(year) + "e" + '%02d' % racecount + ".jpg" + " Has been downloaded")
	#Update iteartors, successful values and strikes
	raceStrike = 0
	yearStrike = 0
	lastGPNum = gpNum
	lastYear = year
	lastRace = racecount
	gpNum += 1
	racecount += 1
	newImages += 1
	#End loop successful case
logging.info(str(newImages) + ' New Images Added')
config.set('LastFile', 'gpNum', str(lastGPNum))
config.set('LastFile', 'year', str(lastYear))
config.set('LastFile', 'racecount', str(lastRace))
with open('f1Scraper.cfg', 'wb') as configfile:
    		config.write(configfile)
logging.info('Config File Updated')
logging.info('-----Script Ended-----')
