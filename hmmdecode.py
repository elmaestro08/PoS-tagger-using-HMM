import sys
import math
tag_set = set()
obs_set = set()
dict_t = {}
dict_e = {}

def read_model():
    global tag_set,obs_set,dict_e,dict_t
    with open('hmmmodel.txt','r') as f:
        contents = f.read().strip().split('\n')
    words = contents[1].strip().split(' ')
    tag_set = set(words)
    words = contents[4].strip().split(' ')
    obs_set = set(words)
    words = contents[8].strip().split(' ')
    words = filter(None,words)
    tag = words[0]
    temp = list(tag_set)
    temp1 = list(words[1:])
    for i in range(len(tag_set)):
        key = tag+'-'+temp[i]
        dict_t[key] = float(temp1[i])
    start = 12
    end = start+(len(tag_set))
    for tag in contents[start:end]:
        words = tag.strip().split(' ')
        t = words[0]
        for i in range(len(tag_set)):
            temp = list(tag_set)
            key = t+'-'+temp[i]
            dict_t[key] = float(words[i+1])
    start = end+3
    end = start+len(obs_set)
    for tag in contents[start:end]:
        words = tag.strip().split(' ')
        obs = words[0]
        for i in range(len(tag_set)):
            temp = list(tag_set)
            key = obs+'-'+temp[i]
            dict_e[key] = float(words[i+1])


def viterbi_decoding(sentence,output):
    probability = {}
    backpointer = {}
    observation = sentence.strip().split(' ')
    T = len(observation)
    for q in tag_set:
        key = q+',0'
        t_key = 'q0-'+q
        e_key = observation[0]+'-'+q
        temp = float(dict_e.get(e_key,1))
        if temp == 0:
            probability[key] = float('-inf')
        else:
            probability[key] = math.log(float(dict_t[t_key]))+math.log(temp)
        backpointer[key] = 'q0'
    for t in range(1,T):
        for q in sorted(tag_set):
            prob = float('-inf')
            temp_state = ''
            for q1 in sorted(tag_set):
                #key = q+','+str(t+1)
                temp = float(probability[q1+','+str(t-1)]) + math.log(float(dict_t[q1+'-'+q]))
                if temp>prob:
                    prob = temp
                    temp_state = q1
            x = float(dict_e.get(observation[t]+'-'+q,1))
            if x != 0:
                probability[q+','+str(t)] = prob + math.log(x)
            else:
                probability[q + ',' + str(t)] = float('-inf')
            backpointer[q+','+str(t)] = temp_state
    #print probability
    #print backpointer
    max_prob = float('-inf')
    max_prob_state = ''
    for key in tag_set:
        #print key
        temp = probability[key+','+str(T-1)]
        if temp>max_prob:
            max_prob = temp
            max_prob_state = key
    temp = max_prob_state
    for i in range(T-1,-1,-1):
        temp = backpointer[temp+','+str(i)]
        max_prob_state = temp+' /'+max_prob_state
    output += ' '.join(map(lambda a,b:a+b,observation,max_prob_state.split(' ')[1:]))
    #print states[::-1]
    #output += ' '.join(states[::-1])
    output += '\n'
    return output


def read_input():
    with open(sys.argv[1],'r') as f:
        contents = f.read().strip().split('\n')
    return contents



def main():
    read_model()
    output = ''
    #print op
    contents = read_input()
    for sentence in contents:
        output = viterbi_decoding(sentence, output)
    with open("hmmoutput.txt", "w+") as f:
        f.write(output)
if __name__ == '__main__':
    main()