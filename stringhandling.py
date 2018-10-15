def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def bestmatch(lst, item, threshold=0.5, max=5):
    index = -1
    bestld = -1
    for i in range(0, len(lst)):
        for j in range(0, len(lst[i])):
            ld = levenshteinDistance(lst[i][j].upper(), item.upper())
            #logging.info("words=({},{}) index={}, best={}, current={}".format(lst[i][j].upper(), item.upper(), index, bestld, ld))
            if index == -1 or bestld > ld:
                bestld = ld
                index = i
    
    if bestld > threshold*len(item) or bestld > max:
        index = -1
    return index

def replacebest(string, replace, threshold=0.5, max=2):
    words = string.split()
    
    for i in range(0, len(words)):
        index = -1
        bestld = -1
        for j in range(0, len(replace)):
            ld = levenshteinDistance(replace[j].upper(), words[i].upper())
            if index == -1 or bestld > ld:
                bestld = ld
                index = j
    
        if bestld > threshold*len(words[i]) or bestld > max:
            index = -1

        if (index != -1):
            words[i] = replace[index]

    
    return ' '.join(words)