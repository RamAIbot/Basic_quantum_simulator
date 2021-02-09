# Basic_quantum_simulator

<h2> Overview </h2>

<p>The project focusses on building a simulator for quantum computing based on the principles of quantum mechanics similar to IBM Qiskit. The simulator is capable of performing
Hadamard gate, CNOT gate and various other unitary gates on the qubits. The Unitary gates are described based on the value of theta,lambda and phi. The Hadamard and CNOT gate is
predefined in the simulator.</p>

<p>There are two versions of the simulator here. The Big_Endian.py uses the Big Endian format to describe the qubits which assigns 0 to MSB and increase towards LSB. The final.py
uses Little Endian format to describe the qubits where 0 is assigned to LSB and increases towards MSB </p>

<h2> Approach Used in design </h2>

<p> The initial approach was to take kronecker product of the gates on the targets bits and multiply with identity for non target bits. This approach is implemented in classic.py.</p>

<h4> Example </h4>
<p> Suppose if we need to implement Hadamard gate operation on the 0th bit in a 2 qubit system, We first take the kronecker product Hadamard matrix for the zeroth bit and multiply with Identity for second bit as no operations is performed for second bit. Conversely if we want to perform Hadamard to second qubit we take kronecker of identity matrix signifying no operations for the first qubit and Hadamard matrix for second qubit.</p>

<h5> Kronecker Product </h5>

<img src="" alt="mat3"/>

<h5> Hadamard for first qubit example </h5>

<img src="" alt="mat1"/>

<h4> State Repressentation </h4>

<p> Here as a basic example we use tow qubit system and it has 4 states 00,01,10,11. We represent the inital state which is of 00 in the form of a matrix so that we can directly multiply with our Hadamard gate through matrix multiplication. We use kronecker product to do so. </p>

<p> Since 0 = [1 0] and 1 = [0 1] we can denote the four states as below </p>

<UL>
  <LI> 00 => [1 0] Kronecker [1 0] </LI>
  <LI> 01 => [1 0] Kronecker [0 1] </LI>
  <LI> 10 => [0 1] Kronecker [1 0] </LI>
  <LI> 11 => [0 1] Kronecker [0 1] </LI>
</UL>

such that their amplitudes sum up to 1.

<img src="" alt="mat2"/>

<p> Now the result of the Hadamard operation can be directly obtained by the matrix multiplication by Hadamard matrix which is kronecker with identity and the state matrix </p>

