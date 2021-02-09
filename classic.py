# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 13:37:18 2021

@author: Admin
"""

import numpy as np
import random

def get_ground_state(num_qubits):
    # return vector of size 2**num_qubits with all zeroes except first element which is 1
    states = []
    for i in range(2**num_qubits):
        if i==0:
            states.extend([1])
        else:
            states.extend([0])
    return np.array(states)

def get_operator(total_qubits, gate_unitary, target_qubits):
    # return unitary operator of size 2**n x 2**n for given gate and target qubits
    unitary_operator= []
    gate = 0   #single qubit gate
    if gate_unitary=='h':
        unitary_operator.append([np.sqrt(1/2),np.sqrt(1/2)])
        unitary_operator.append([np.sqrt(1/2),-1.0*np.sqrt(1/2)])
        
    elif gate_unitary == 'cx':
#        
        unitary_operator.append([1,0,0,0])
        unitary_operator.append([0,1,0,0])
        unitary_operator.append([0,0,0,1])
        unitary_operator.append([0,0,1,0])
        
#        unitary_operator.append([1,0,0,0])
#        unitary_operator.append([0,1,0,0])
#        unitary_operator.append([0,0,0,1])
#        unitary_operator.append([0,0,1,0])
        gate =2  #2qubit gate
        
    
        
    
    unitary_operator = np.array(unitary_operator)
    #print(unitary_operator)
    
    num_qubits = np.log2(total_qubits)
   # print(num_qubits)
  #  print(target_qubits)
    arr = []
    for i in range(int(num_qubits)):
        #0 -> MSB
        #1 -> LSB 
        #Big Endian
        if(gate == len(target_qubits)):
            return unitary_operator
        
        if i==0:
            if i in target_qubits:
                arr = np.copy(unitary_operator)
            else:
                arr = np.identity(unitary_operator.shape[0])
        else:
            if i in target_qubits:
                arr = np.kron(arr,unitary_operator)
            else:
                arr = np.kron(arr,np.identity(unitary_operator.shape[0]))
   # print(arr)
                
            
        
   
    
    return arr

def run_program(initial_state, program):
    # read program, and for each gate:
    #   - calculate matrix operator
    #   - multiply state with operator
    # return final state
    out = np.copy(initial_state)
    for gates in program:
        matrix = get_operator(len(my_qpu), gates['gate'],gates["target"])
        print(matrix.shape)
        out = np.matmul(matrix,out)
        print(out)
        
        
    return out

def measure_all(state_vector):
    
    # choose element from state_vector using weighted random and return it's index
    states = [i for i in range(len(state_vector))]
    out = random.choices(states,weights=state_vector)
    return out

def get_counts(state_vector, num_shots):
    # simply execute measure_all in a loop num_shots times and
    # return object with statistics in following form:
    #   {
    #      element_index: number_of_ocurrences,
    #      element_index: number_of_ocurrences,
    #      element_index: number_of_ocurrences,
    #      ...
    #   }
    # (only for elements which occoured - returned from measure_all)
    out = {}
    arr = np.zeros(len(state_vector))
    num_qubits = np.log2(len(state_vector))
    

    for i in range(num_shots):
        state = measure_all(state_vector)
        arr[state] +=1
    print(arr)
    
    for i in range(len(state_vector)):
        num = np.binary_repr(i,width=int(num_qubits))
        out[str(num)] = arr[i]
    #    print(out)
    return out


my_circuit = [
{ "gate": "h", "target": [0] }, 
{ "gate": "cx", "target": [0, 1] }
]
    
#my_circuit = [
#  { "unitary": [["cos(theta/2)", "-exp(i * lambda) * sin(theta / 2)"], ["exp(i * phi) * sin(theta / 2)", "exp(i * lambda + i * phi) * cos(theta / 2)"]], "params": { "theta": 3.1415, "phi": 1.15708, "lambda": -3.1415 }, "target": [0] }
#  
#]


# Create "quantum computer" with 2 qubits (this is actually just a vector :) )

my_qpu = get_ground_state(2)
#print(my_qpu)
#print(get_operator(len(my_qpu), 'h',my_circuit[0]["target"]))
#print(get_operator(len(my_qpu), 'cx',my_circuit[1]["target"]))

## Run circuit
#
final_state = run_program(my_qpu, my_circuit)
print(final_state)
#
#
## Read results
#
counts = get_counts(final_state, 1000)
#
print(counts)

# Should print something like:
# {
#   "00": 502,
#   "11": 498
# }

# Voila!