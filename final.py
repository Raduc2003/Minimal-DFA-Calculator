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
# initial partitions (indexes)
partitions = []
partitions.append(set([x for x in range(n)]).difference(set(final_states)))
partitions.append(set(final_states))
partitions[0] = list(partitions[0])
partitions[1] = list(partitions[1])


def same_partition(node1, node2, partitions):
    for partition in partitions:
        if node1 in partition and node2 in partition:
            return True
    return False


def partitioner(partitions):
    new_partitions = []
    for partition in partitions:
        for state in partition:
            #verific daca starea e intr-o partitie deja
            state_added = False
            for new_partition in new_partitions:
                if same_partition(state, new_partition[0], partitions):
                    new_partition.append(state)
                    state_added = True
                    break
            
            if not state_added:
                new_partitions.append([state])

    while True:
        partition_found = False
        for partition in new_partitions:
            for i in range(len(partition)):
                for j in range(i+1, len(partition)):
                    state1 = partition[i]
                    state2 = partition[j]
                    if not same_partition(state1, state2, partitions):
                        new_partition = [state1, state2]
                        new_partitions.append(new_partition)
                        partition.remove(state1)
                        partition.remove(state2)
                        partition_found = True
                        break
                if partition_found:
                    break
            if partition_found:
                break
        
        if not partition_found:
            return [partition for partition in new_partitions if partition]

print("partitioning")
print(partitioner(partitions))
print()
partitions=partitioner(partitions)
def build_dfa(partitions, states,initial_state, final_states):
    new_states=[]
    new_inital_state='k'
    new_final_states=[]
    i=0
    for state in partitions:
        name ="".join([str(x) for x in state])
        new_states.append(Node('q'+name))  
        new_states[0].next=states[state[0]].next
        for i in state:
            if i == int(initial_state):
                new_inital_state=i
            if i in final_states:
                new_final_states.append(i)
    return new_states,new_inital_state,new_final_states
new_states,new_inital_state,new_final_states = build_dfa(partitions, states, initial_state, final_states)
print("Minimal DFA: ")
for state in new_states:
    state.out()
print("initial state: ",new_inital_state)
print("final states: ",new_final_states)
print()