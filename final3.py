import copy
class Node:
    def __init__(self, name):
        self.name = name
        self.next = {}

    def out(self):
        print(self.name)
        print(self.next)


states = []
# data parsing starile trebuie sa fie in ordine 1,2,3,4...
f = open("LFA2 -MINIMAL DFA\Minimal-DFA-Calculator\input.txt")
n = int(f.readline().split(" ")[0])
for i in range(n):
    states.append(Node('q'+str(i)))

initial_state = f.readline().split(" ")[0][1]
lines = f.readlines()
final_states = [int(x[1]) for x in lines[-1].split(" ")]
for line in lines[:-1]:
    line = line.strip().split(" ")
    states[int(line[0][1])].next[line[1]] = line[2]
print("Original DFA: ")
for state in states:
    state.out()
print("initial state", initial_state)
print("final states", final_states)
print()
transitions = states[0].next.keys()


# partitioning proces 
# initial partitions (indexes)
partitions = [[x for x in range(n) if x not in final_states], final_states]
print("Initial partitions:")
print(partitions)
print()
#ambele stari sunt in aceeasi partitite
def same_partition(state1,state2,partitions):
    for partition in partitions:
        if state1 in partition and state2 in partition:
            return 1
    return 0

def partitioner(partitions,states,transitions):
    new_partitions=[]
    copy_partitions=copy.deepcopy(partitions)
    k=0
    for i in range(len(partitions)):
        s1=0
        while(s1<len(partitions[i])):
        # for s1 in range(len(partitions[i])):
            print(s1,"Asdasd")
            state1=partitions[i][s1]
            new_partitions.append([])
            new_partitions[k].append(state1)
            s2=s1+1
            while(s2<len(partitions[i])):
            # for s2 in range(s1+1,len(partitions[i])):
                state2=partitions[i][s2]
                ok=1
                for transition in transitions:

                    tr1=int(states[state1].next[transition][1])
                    tr2=int(states[state2].next[transition][1])
                    print("se verfica: ",state1,state2,"prin: ",transition)
                    if not same_partition(tr1,tr2,copy_partitions):
                        ok=0
                if ok==1:
                    print("alacazam")
                    new_partitions[k].append(state2)
                    partitions[i].remove(state2)
                    s2-=1
                s2+=1
            s1+=1
            print(new_partitions)
            k+=1
            print("VERIFICAM: ",new_partitions,"cu",copy_partitions)
    if copy_partitions != new_partitions:
        copy_partitions = new_partitions
        return partitioner(new_partitions, states, transitions)
    else:
        return copy_partitions
partitions=partitioner(partitions,states,transitions)
print("Minimal Dfa partitions:")
print(partitions)
print()
def new_state_finder(state, partitions):
    for new_state in partitions:
        if state in new_state:
            return 'q'+ "".join([str(x) for x in new_state])
#returns partition(new_state) in wich is state 
def build_dfa(partitions, states,initial_state, final_states):
    new_states=[]
    new_inital_state='k'
    new_final_states=set([])
    k=0
    for state in partitions:
        
        name ="".join([str(x) for x in state])
        new_states.append(Node('q'+name))  
        for transition in transitions:
            new_next=new_state_finder(int(states[state[0]].next[transition][1]),partitions)
            new_states[k].next[transition]=new_next
            print(new_states[k].name)
            print(k)
        k+=1
        new_inital_state= new_state_finder(int(initial_state),partitions)
        for s in final_states:
            new_final_states.add(new_state_finder(s,partitions))
    return new_states,new_inital_state,new_final_states
new_states,new_inital_state,new_final_states = build_dfa(partitions, states, initial_state, final_states)
print("Minimal DFA: ")
for state in new_states:
    state.out()
print("initial state: ",new_inital_state)
print("final states: ",new_final_states)
print()