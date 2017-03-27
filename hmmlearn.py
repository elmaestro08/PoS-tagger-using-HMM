import sys
tag_set = set()
obs_set = set()
def read_input():
    with open(sys.argv[1],'r') as f:
        contents = f.read().strip().split('\n')
        contents = ['q0 ' + x for x in contents]
    return contents

def transition_prob(contents):
    global tag_set
    global obs_set
    temp = []
    temp1 = []
    dict_transition = {}
    dict_transition_denominator = {}
    for line in contents:
        words = line.strip().split(' ')
        for curr_ptr in range(len(words)-1):
            next_ptr = curr_ptr + 1
            curr_tag = words[curr_ptr][-2:]
            next_tag = words[next_ptr][-2:]
            temp.append(curr_tag)
            temp1.append(words[curr_ptr][:-3])
            if curr_ptr == (len(words) - 2):
                temp.append(next_tag)
                temp1.append(words[next_ptr][:-3])
            if not dict_transition_denominator.has_key(curr_tag):
                dict_transition_denominator[curr_tag] = 1
            else:
                dict_transition_denominator[curr_tag] += 1
            if not dict_transition.has_key(curr_tag+'-'+next_tag):
                dict_transition[curr_tag+'-'+next_tag] = 1
            else:
                dict_transition[curr_tag + '-' + next_tag] += 1
    temp = [x for x in temp if x!='q0']
    tag_set = set(temp)
    temp1 = filter(None,temp1)
    obs_set = set(temp1)
    return dict_transition,dict_transition_denominator

def emission_prob(contents):
    dict_emission = {}
    dict_tagCount = {}
    for line in contents:
        words = line.strip().split(' ')
        for curr_ptr in range(len(words)):
            wordtag = words[curr_ptr]
            tag = words[curr_ptr][-2:]
            if not dict_tagCount.has_key(tag):
                dict_tagCount[tag] = 1
            else:
                dict_tagCount[tag] += 1
            if not dict_emission.has_key(wordtag):
                dict_emission[wordtag] = 1
            else:
                dict_emission[wordtag] += 1
    dict_tagCount.pop('q0',None)
    return dict_emission,dict_tagCount

def write_to_file(dict_t,dict_td,dict_e,dict_tc):
    fileContents = ''
    fileContents += 'Tags:\n'
    fileContents +=' '.join(tag_set)
    fileContents +='\n\nObservations:\n'
    fileContents +=' '.join(obs_set)
    fileContents +='\n\nInitial Probability:\n'
    fileContents += 'tag '+' '.join(tag_set)
    fileContents +='\nq0 '
    for tag in tag_set:
        key = 'q0-'+tag
        fileContents += ' '+str((float(dict_t.get(key,0))+1.0)/(float(dict_td.get('q0'))+len(tag_set)))
    fileContents += '\n\nTransition probability:\n'
    fileContents += 'tag '+' '.join(tag_set)
    for tag in tag_set:
        fileContents +='\n'+tag
        for tag1 in tag_set:
            key = tag+'-'+tag1
            fileContents += ' '+str((float(dict_t.get(key,0))+1.0)/(float(dict_td[tag])+len(tag_set)))
    fileContents += '\n\nEmission Probability:\n'
    fileContents += 'tag '+' '.join(tag_set)
    for obs in obs_set:
        fileContents += '\n'+obs
        for tag in tag_set:
            key = obs+'/'+tag
            fileContents += ' '+str(float(dict_e.get(key,0))/float(dict_tc[tag]))
    with open("hmmmodel.txt", "w+") as f:
        f.write(fileContents)

def main():
    contents = read_input()
    dict_t,dict_td = transition_prob(contents) #O(n) to remove
    dict_e,dict_tc = emission_prob(contents)
    write_to_file(dict_t,dict_td,dict_e,dict_tc)


if __name__ == '__main__':
    main()