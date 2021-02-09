# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 13:37:18 2021

@author: Admin
"""

import numpy as np
import random
#************LITTLE ENDIAN FORMAT MSB is 2 and LSB is 0
def get_ground_state(num_qubits):
    # return vector of size 2**num_qubits with all zeroes except first element which is 1
    states = []
    for i in range(2**num_qubits):
        if i==0:
            states.extend([1])
        else:
            states.extend([0])
    return np.array(states)

def get_operator(total_qubits, gate_unitary, target_qubits,gates):
    # return unitary operator of size 2**n x 2**n for given gate and target qubits
    unitary_operator= []
    inv = 0
    control = 0
    target = 0
    if gate_unitary=='h':
        unitary_operator.append([np.sqrt(1/2),np.sqrt(1/2)])
        unitary_operator.append([np.sqrt(1/2),-1.0*np.sqrt(1/2)])
        
    elif gate_unitary == 'cx':
#       
        control = target_qubits[0]
        target = target_qubits[1]
        
        if target - control > 0:
            inv=0
        else:
          inv=1
          
    elif gate_unitary=='u3':
        theta = gates["params"]["theta"]
        phi1 = gates["params"]["phi"]
        lambda1 = gates["params"]["lambda"]
#        print(theta)
#        print(phi1)
#        print(lambda1)
        unitary_operator.append([np.cos(theta/2), -np.exp(lambda1*1.j) * np.sin(theta / 2)])
        unitary_operator.append([np.exp(phi1*1.j) * np.sin(theta / 2), np.exp(lambda1*1.j + phi1*1.j) * np.cos(theta / 2)])
        
        #print(unitary_operator)
        
        
    
        
    
    #unitary_operator = np.array(unitary_operator)
    #print(unitary_operator)
    bit_vector = [[1,0],[0,1]]
    
    num_qubits = np.log2(total_qubits)
   # print(num_qubits)
  #  print(target_qubits)
    arr = []
    for i in range(total_qubits):
        binary = np.binary_repr(i,int(num_qubits))
        binary = "".join(reversed(binary)) 
        #print(binary[0])
        outer = []
        control_val = [1,0] if binary[control]=='0' else [0,1]
        #print(control_val)
        for j in range(int(num_qubits)-1,-1,-1):
            bit_val = int(binary[j])
            
            if gate_unitary=='h':
                if j in target_qubits:
                    outer = unitary_operator[bit_val][:] if len(outer) == 0 else np.kron(outer,unitary_operator[bit_val][:])
                else:
                    outer =  bit_vector[bit_val] if len(outer)==0 else np.kron(outer,bit_vector[bit_val])
           
            elif gate_unitary=='cx':
                if j==control:
                    outer = bit_vector[bit_val] if len(outer)==0 else np.kron(outer,bit_vector[bit_val])
                    #control_val = bit_vector[bit_val]
                elif j == target:
                    multiplier = bit_vector[bit_val] if control_val == [1,0] else bit_vector[1 - bit_val]
                    outer = multiplier if len(outer)==0 else np.kron(outer,multiplier)
                else:
                    outer = bit_vector[bit_val] if len(outer)==0 else np.kron(outer,bit_vector[bit_val])
                    
            elif gate_unitary=='u3':
                if j in target_qubits:
                    outer = unitary_operator[bit_val][:] if len(outer) == 0 else np.kron(outer,unitary_operator[bit_val][:])
                else:
                    outer =  bit_vector[bit_val] if len(outer)==0 else np.kron(outer,bit_vector[bit_val])
                    
            #print(outer)
            
                
            
            
                
                
                    
        arr.append(outer)
            
            
   
    arr = np.array(arr)
    #print(arr.shape)
    #print(arr)
    return arr

def run_program(initial_state, program):
    # read program, and for each gate:
    #   - calculate matrix operator
    #   - multiply state with operator
    # return final state
    out = np.copy(initial_state)
    for gates in program:
        matrix = get_operator(len(my_qpu), gates['gate'],gates["target"],gates)
        #print(matrix.shape)
        out = np.matmul(matrix,out)
        #print(out)
        
        
    return np.abs(out)

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
    #print(arr)
    
    for i in range(len(state_vector)):
        num = np.binary_repr(i,width=int(num_qubits))
        out[str(num)] = arr[i]
    #    print(out)
    return out


#my_circuit = [
#{ "gate": "h", "target": [0,1] },
##first bit is control and second is target 
#{ "gate": "cx", "target": [0,2] }
#]
    
#my_circuit = [
#  { "unitary": [["cos(theta/2)", "-exp(i * lambda) * sin(theta / 2)"], ["exp(i * phi) * sin(theta / 2)", "exp(i * lambda + i * phi) * cos(theta / 2)"]], "params": { "theta": 3.1415, "phi": 1.15708, "lambda": -3.1415 }, "target": [0] }
#  
#]

my_circuit= [
  { "gate": "u3", "params": { "theta": 3.1415, "phi": 1.5708, "lambda": -3.1415 }, "target": [0,1,2,3] }
]

# Create "quantum computer" with 2 qubits (this is actually just a vector :) )

my_qpu = get_ground_state(4)
#print(my_qpu)
#print(get_operator(len(my_qpu), 'h',my_circuit[0]["target"]))
#print(get_operator(len(my_qpu), 'cx',my_circuit[1]["target"]))
#print(get_operator(len(my_qpu), 'u3',my_circuit[0]["target"],my_circuit[0]))

## Run circuit
#
final_state = run_program(my_qpu, my_circuit)
#print(final_state)
##
##
### Read results
##
counts = get_counts(final_state, 1000)
#
print(counts)
#
## Should print something like:
# {
#   "00": 502,
#   "11": 498
# }

# Voila!