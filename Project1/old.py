    import numpy as np
def get_matches_starting_at(data, pattern, index, starting_index, resulting_matches, ibi):

    P = pattern[0]
    if data[index:index+len(P)] == P:
        if len(pattern) == 1:
            resulting_matches.append((starting_index,index+len(P)))
        else:
            c = np.array(ibi[0])
            for new_index in c[(c > index) & (c <= index + pattern[1][1]+len(P))]:
                get_matches_starting_at(data, pattern[2:], new_index, starting_index, resulting_matches, ibi[1:])

        return resulting_matches
    else:
        return []

def get_all_matches(data, pattern):
    matches_found = []
    ibi = []
    for pat in pattern[2::2]:
        ibi.append([m.start() for m in re.finditer(pat, data)])
    for index in [m.start() for m in re.finditer(pattern[0], data)]:
        matches_at_index = get_matches_starting_at(data, pattern, index, index, [], ibi)
        matches_found += matches_at_index

    return set(matches_found)


def matchA(pattern, showout = True):
    regx = pat2reg(pattern)
    totmatches = []
    for i in range(1,4):
        with open("Anwiki_p" + str(i), 'r') as myfile:
            content = myfile.readlines()

        for text in content:
            matches = re.findall(regx, text)
            if len(matches) > 0:
                for match in matches:
                    totmatches.append(match)
    total_matches = []
    for match in totmatches:
        b = get_all_matches(match, pattern)
        for m in b:
            total_matches.append(match[m[0]:m[1]])
            
    print(len(total_matches))
    if showout:
        for match in total_matches:
            print(match)

def matchA2(pattern):
    total_matches = []
    for i in range(1,4):
        with open("Anwiki_p" + str(i), 'r') as myfile:
            content = myfile.readlines()

        for text in content:
            matches = david_finder(text, pattern)
            if len(matches) > 0:
                for match in matches:
                    total_matches.append(match)
            
    return(total_matches)

import glob, multiprocessing

def process(line, pattern):
    matches = david_finder(line, pattern)
    total_matches = []
    if len(matches) > 0:
        for match in matches:
            total_matches.append(match)
    return(total_matches)

def worker(file, pattern, reg):
    total_matches = []
    with open(file, 'r') as f:
        for line in f:
            if all(c in line for c in pattern[::2]):
                #pass
                matches = process(line, pattern)
                if len(matches) > 0:
                    for match in matches:
                        total_matches.append(match)
                    
    return(total_matches)

start = time.time()

pattern = ['technical', (0, 20), 'university', (0, 20), 'denmark']
reg = pat2reg(pattern)
pool = multiprocessing.Pool(4)
results = []

for ifile in glob.glob('enwiki_p*'):
    res = pool.apply_async(worker,[ifile, pattern, reg])
    results.append([ifile,res])

pool.close()
pool.join()

matches = []
for result in results:
    matches += result[1].get()
print(len(matches))
print("Elapsed time:" + str(time.time()-start))

def matchcat(pattern):
    regx = pat2reg(pattern)
    matches = re.findall(regx, cat, overlapping=True)
    total_matches = []
    for match in matches:
        b = get_all_matches(match, pattern)
        for m in b:
            total_matches.append(match[m[0]:m[1]])
    return total_matches


with open("Dumps/" + pat2reg(pattern), 'w') as f:
    f.write(str(len(matches)) + "\n")
    f.write("\n".join(matches))