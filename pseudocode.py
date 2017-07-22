shiftTable(pattern[0..m-1]):
	Table = []
	for i in range(256):
		Table.append(len(pattern))
	for i in range(len(pattern) - 1):
		if(pattern[i] == wildcard):
			continue
		Table[pattern[i]] = len(pattern) - 1 - i


ExactMatch(pattern[0..m-1], string[0..n-1]):
	Table = shiftTable(pattern)
	index = 0
	while(len(string) - index >= len(pattern)):
		i = len(pattern) - 1
		while(string[index + i] == pattern[i]):
			if(i == 0):
				return index
			i = i - 1
		index = index + Table[string[index + len(pattern) - 1]]
	return -1

oneChrMatch(pattern[0..m-1], string[0..n-1]):
	partialMatches = []
	for j in range(len(pattern)):
		holdr = pattern
		del pattern[j]
		Table = shiftTable(pattern)
		index = 0
		while(len(string) - index >= len(pattern)):
			i = len(pattern) - 1
			while(string[index + i] == pattern[i]):
				if(i == 0):
					partialMatches.append((string[index:index+len(pattern)],index))
					break
				i = i - 1
			index = index + Table[string[index + len(pattern) - 1]]
		pattern = holdr
	return partialMatches

oneExtraMatch(pattern[0..m-1], string[0..n-1]):
	partialMatches = []
	for j in range(1,len(pattern)):
		holdr = pattern
		pattern.insert(j,wildcard)
		Table = shiftTable(pattern)
		index = 0
		while(len(string) - index >= len(pattern)):
			i = len(pattern) - 1
			while(string[index + i] == pattern[i] or pattern[i] == wildcard):
				if(i == 0):
					partialMatches.append((string[index:index+len(pattern)],index))
					break
				i = i - 1
			index = index + Table[string[index + len(pattern) - 1]]
		pattern = holdr
	return partialMatches	

replaceMatch(pattern[0..m-1], string[0..n-1]):
	partialMatches = []
	Table = shiftTable(pattern)
	index = 0
	while(len(string) - index >= len(pattern)):
		miss = 0
		i = len(pattern) - 1
		while(string[index + i] == pattern[i] or miss <= 1):
			if(string[index + i] != pattern[i]):
				miss = miss + 1
				if(miss > 1):
					break
			if(i == 0):
				partialMatches.append((string[index:index+len(pattern)],index))
				break
			i = i - 1
		index = index + Table[string[index + len(pattern) - 1]]
	return partialMatches	

swapMatch(pattern[0..m-1], string[0..n-1]):
	partialMatches = []
	Table = shiftTable(pattern)
	index = 0
	while(len(string) - index >= len(pattern)):
		miss = 0
		i = len(pattern) - 1
		while(string[index + i] == pattern[i] or miss <= 1):
			if(string[index + i] != pattern[i]):
				miss = miss + 1
				if(miss > 1):
					break
				if(string[index + i] != pattern[i-1]):
					break
				if(string[index + i-1] != pattern[i]):
					break
				i = i - 1
			if(i == 0):
				partialMatches.append((string[index:index+len(pattern)],index))
				break
			i = i - 1
		index = index + Table[string[index + len(pattern) - 1]]
	return partialMatches