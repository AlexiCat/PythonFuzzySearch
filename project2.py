#!/usr/bin/env python

######################################################################################################################
# File name: project2.py
# Description: A program that implements several deviations of Horspool's algorithm to perform a fuzzy search
# Author: Alexis Miranda
#
# Notes: This program is only guaranteed to be stable for an alphabet of 256 characters.
#        
######################################################################################################################

import os, sys, time

operations = 0
sOperations = 0

####################COMPUTE SHIFT TABLE####################
def shiftTable(pattern):
	global sOperations
	T = []
	for i in range(256):
		T.append(len(pattern))
	for i in range(len(pattern) - 1):
		if(pattern[i] == "ʘ"):
			continue
		sOperations = sOperations + 1
		T[ord(pattern[i])] = len(pattern) - 1 - i
	return T
###########################################################

####################LOOK FOR EXACT MATCH####################
def exactMatch(phrasee, string):
	global operations
	phrase = phrasee[:]
	T = shiftTable(phrase)
	index = 0
	while(len(string) - index >= len(phrase)):
		i = len(phrase) - 1
		operations = operations + 1
		while(string[index + i] == phrase[i]):
			operations = operations + 1
			if(i == 0):
				return index
			i = i - 1
		#print(string[index + len(phrase) - 1])
		if(ord(string[index + len(phrase) - 1]) > 255):
			#print("Warning: This program only guarantees stability for an alphabet of 256 symbols")
			index = index + len(phrase)
		else:
			index = index + T[ord(string[index + len(phrase) - 1])]
	return -1
############################################################

####################LOOK FOR ONE MISSING CHARACTER####################
def oneChrMatch(phrasee, string):
	global operations
	phrase = phrasee[:]
	partialMatches = []
	for j in range(len(phrase)):
		holdr = phrase[:]
		del phrase[j]
		T = shiftTable(phrase)
		index = 0
		while(len(string) - index >= len(phrase)):
			i = len(phrase) - 1
			operations = operations + 1
			while(string[index + i] == phrase[i]):
				operations = operations + 1
				if(i == 0):
					#return index
					partialMatches.append(("".join(string[index:index+len(phrase)]),index))
					break
				i = i - 1
			if(ord(string[index + len(phrase) - 1]) > 255):
				#print("Warning: This program only guarantees stability for an alphabet of 256 symbols")
				index = index + len(phrase)
			else:
				index = index + T[ord(string[index + len(phrase) - 1])]
		phrase = holdr[:]
	return partialMatches	
######################################################################

####################LOOK FOR ONE EXTRA CHARACTER####################
def oneExtraMatch(phrasee, string):
	global operations
	phrase = phrasee[:]
	partialMatches = []
	for j in range(1,len(phrase)):
		holdr = phrase[:]
		phrase.insert(j,"ʘ")
		T = shiftTable(phrase)
		index = 0
		while(len(string) - index >= len(phrase)):
			i = len(phrase) - 1
			operations = operations + 1
			while(string[index + i] == phrase[i] or phrase[i] == "ʘ"):
				operations = operations + 1
				if(i == 0):
					#return index
					partialMatches.append(("".join(string[index:index+len(phrase)]),index))
					break
				i = i - 1
			if(ord(string[index + len(phrase) - 1]) > 255):
				#print("Warning: This program only guarantees stability for an alphabet of 256 symbols")
				index = index + len(phrase)
			else:
				index = index + T[ord(string[index + len(phrase) - 1])]
		phrase = holdr[:]
	return partialMatches	
####################################################################

####################LOOK FOR ONE REPLACED CHARACTER####################
def replaceMatch(phrasee, string):
	global operations
	phrase = phrasee[:]
	partialMatches = []
	T = shiftTable(phrase)
	index = 0
	while(len(string) - index >= len(phrase)):
		miss = 0
		i = len(phrase) - 1
		operations = operations + 1
		while(string[index + i] == phrase[i] or miss <= 1):
			operations = operations + 1
			if(string[index + i] != phrase[i]):
				miss = miss + 1
				if(miss > 1):
					break
			if(i == 0):
				#return index
				partialMatches.append(("".join(string[index:index+len(phrase)]),index))
				break
			i = i - 1
		if(ord(string[index + len(phrase) - 1]) > 255):
			#print("Warning: This program only guarantees stability for an alphabet of 256 symbols")
			index = index + len(phrase)
		else:
			index = index + T[ord(string[index + len(phrase) - 1])]
	return partialMatches	
#######################################################################


####################LOOK FOR ONE SWAPPED CHARACTER####################
def swapMatch(phrasee, string):
	global operations
	phrase = phrasee[:]
	partialMatches = []
	T = shiftTable(phrase)
	index = 0
	while(len(string) - index >= len(phrase)):
		miss = 0
		i = len(phrase) - 1
		operations = operations + 1
		while(string[index + i] == phrase[i] or miss <= 1):
			operations = operations + 1
			if(string[index + i] != phrase[i]):
				miss = miss + 1
				if(miss > 1):
					break
				if(string[index + i] != phrase[i-1]):
					break
				if(string[index + i-1] != phrase[i]):
					break
				i = i - 1
			if(i == 0):
				#return index
				partialMatches.append(("".join(string[index:index+len(phrase)]),index))
				break
			i = i - 1
		if(ord(string[index + len(phrase) - 1]) > 255):
			#print("Warning: This program only guarantees stability for an alphabet of 256 symbols")
			index = index + len(phrase)
		else:
			index = index + T[ord(string[index + len(phrase) - 1])]
	return partialMatches
######################################################################

####################GET FILE NAME####################
#Get list of files
dirs = os.listdir()

#Ask user for file name
print("Please select a file (0 to exit):")
i = 0
for file in dirs:
	i = i + 1
	print("(" + str(i) + ") " + file)

choice = int(input("\nChoice: "))

if(choice == 0):
	exit()

i = 1
fname = ""
for file in dirs:
	if(i == choice):
		fname = file
	i = i+1

if (fname == ""):
	print("Error: Invalid choice")
	exit()
#####################################################

file = open(fname)
document = list(file.read())
file.close()

phrase = input("Please enter a search phrase: ")
lPhrase = list(phrase)

t0 = time.time()
ex = exactMatch(lPhrase, document)
t1 = time.time()

run = t1 - t0

if (ex != -1):
	print("\nExact match found at index " + str(ex))
	print("Runtime: " + str(float(run)))
	print("Basic operations: " + str(operations))
	print("Basic operations (shift table): " + str(sOperations))
else:
	operations = 0
	sOperations = 0
	t0 = time.time()
	chrr = oneChrMatch(lPhrase, document)
	extr = oneExtraMatch(lPhrase, document)
	rplce = replaceMatch(lPhrase, document)
	swp = swapMatch(lPhrase, document)
	t1 = time.time()
	run = t1 - t0
	total = len(chrr) + len(extr) + len(rplce) + len(swp)

	if(total > 0):
		print("\nApproximate matches found")
		print("\nOne character missing:")
		for i in range(len(chrr)):
			print("".join(chrr[i][0]) + " at index " + str(chrr[i][1]))

		print("\nOne character added:")
		for i in range(len(extr)):
			print("".join(extr[i][0]) + " at index " + str(extr[i][1]))

		print("\nOne character replaced:")
		for i in range(len(rplce)):
			print("".join(rplce[i][0]) + " at index " + str(rplce[i][1]))

		print("\nOne character swapped:")
		for i in range(len(swp)):
			print("".join(swp[i][0]) + " at index " + str(swp[i][1]))

		print("\nTotal approximate matches: " + str(total))
		print("Runtime: " + str(float(run)))
		print("Basic operations: " + str(operations))
		print("Basic operations (shift table): " + str(sOperations))
	else:
		print("\nNo matches found")