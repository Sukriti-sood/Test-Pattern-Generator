def generate_test_vectors(circuit_file, fault_node, fault_type):
    # Read the circuit file and parse the circuit
    circuit = parse_circuit_file(circuit_file)
    n = len(circuit_file)+4
    # Initialize visited dictionary to keep track of backtracked nodes.
    vis = {}
    # Initialize node_values to keep setting values to the nodes
    node_values = {}
    # Initialize the test vectors
    test_vectors = []
    
    # Determine the test value based on the fault type
    if fault_type == "SA0":
        test_value = 1
    elif fault_type == "SA1":
        test_value = 0
    else:
        raise ValueError("Invalid fault type")
    backtrack(circuit,fault_node,test_value,vis,node_values)
    if fault_node!='Z':
        set_farward_path_of_fault_node(circuit,'Z',vis,node_values)
    # Generate the test vectors
    inputs = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for node,val in node_values.items():
        # Set the test value for the fault node
        if(node=='A' or node=='B' or node=='C' or node=='D'):
          inputs[node] = val
        

    # Propagate the test value through the circuit
    output = simulate_circuit(circuit, node_values)
    
     # Add the test vector and expected output to the list
    test_vector = inputs.values()
    test_vectors.append((test_vector, output))
    
    return test_vectors

 # Function   [ parse_circuit_file]
 # Synopsis   [ usage:	Parse circuit.txt file.

 #              description:
 # 								This functions creates a graph from circuit.
 #                Arguments:
 #                  circuit.txt file
 #            ]
 # **************************************************************************

   
def parse_circuit_file(circuit_file):
    circuit = {}
    with open(circuit_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith('net_'):
                node, equation = line.split('=')
                circuit[node.strip()] = parse_equation(equation.strip())
            elif line.startswith('Z'):
                circuit['Z']= parse_equation(line.split('=')[1].strip())
    return circuit

 # Function   [ parse_equation]
 # Synopsis   [ usage:	Parse lines in circuit.txt file.

 #              description:
 # 								This functions is responsible to creates edges between gate nodes.
 #                Arguments:
 #                  a line of circuit.txt file (equation)
 #            ]
 # **************************************************************************

def parse_equation(equation):
    if '&' in equation:
        gate = '&'
        inputs = equation.split('&')
    elif '|' in equation:
        gate = '|'
        inputs = equation.split('|')
    elif '~' in equation:
        gate = '~'
        inputs = [equation[1:].strip()]
    elif '^' in equation:
        gate = '^'
        inputs = equation.split('^')
    else:
        raise ValueError(f"Invalid gate in equation: {equation}")
    
    return {'gate': gate, 'inputs': [input_node.strip() for input_node in inputs]}

 # Function   [ Backtrack ]
 # Synopsis   [ usage:	Backtrack from a node and keep setting values accordingly.

 #              description:
 #                  this function backtrack from a perticular node to the inputs and sets the values of nodes in the path
 #                Arguments:
 #                  circuit (circuit graph)
 #                  node from which to backtrack
 #                  vis : visited dictionary to check if already backtracked or not.
 #                  node_values: node_values dictionary 
 #            ]
 # **************************************************************************

def backtrack(circuit,current_node,value,vis,node_values):
    node_values[current_node] = value;
    vis[current_node] = 1;
    if(current_node=='A' or current_node=='B' or current_node=='C' or current_node=='D'):
        return
    gate = circuit[current_node]['gate']
    val = 1;
    if(gate=='&'):
        val = value
    elif(gate=='|'):
        val = value
    elif(gate=='~'):
        val = (value^1)
    else:
        cnt =0;
        for nodes in circuit[current_node]['inputs']:
            if(cnt==0 and value==1):
                backtrack(circuit,nodes,1,vis,node_values)  
            else:
                backtrack(circuit,nodes,0,vis,node_values)  
            cnt+=1
        return
    for nodes in circuit[current_node]['inputs']:
        backtrack(circuit,nodes,val,vis,node_values)


 # Function   [ set_farward_path_of_fault_node]
 # Synopsis   [ usage:	set values in the forward path of fault node.

 #              description:
 # 								This functions is responsible to set values in the forward path.
 #                Arguments:
 #                  circuit, current node, visited dictionary, node values
 #            ]
 # **************************************************************************

def set_farward_path_of_fault_node(circuit,current_node,vis,node_values):
    if(current_node=='A' or current_node=='B' or current_node=='C' or current_node=='D'):
        return
    gate = circuit[current_node]['gate']
    val = 1
    for nodes in circuit[current_node]['inputs']:
        set_farward_path_of_fault_node(circuit,nodes,vis,node_values);
    for nodes in circuit[current_node]['inputs']:
        if vis.get(nodes) is not None:
            value = node_values[nodes]
            ans = value
            if(gate=='&'):
                val = 1
            if(gate=='|'):
                val = 0
            else:
                val = (value^1)
            for nds in circuit[current_node]['inputs']:
                if vis.get(nds) is None:
                  com=''
                  if gate=='~':
                    com = (str(val)+"^1")
                  else:  
                    com = (str(ans)+gate+str(val))
                  # print(com)
                  ans = eval(com)
                  backtrack(circuit,nds,val,vis,node_values)
            node_values[current_node] = ans
            vis[current_node] =1;

 # Function   [ simulate_circuit ]
 # Synopsis   [ usage:	find the expacted output for a given input.
 #                Arguments:
 #                  circuit
 #                  input values
 #            ]
 # **************************************************************************

def simulate_circuit(circuit, node_values):
    
    for node, info in circuit.items():
        gate = info['gate']
        node_inputs = info['inputs']
        output = 0
        if gate == '&':
            output = 1
            for input_node in node_inputs:
                output &= node_values[input_node]
        elif gate == '|':
            output = 0
            for input_node in node_inputs:
                output |= node_values[input_node]
        elif gate == '~':
            input_node = node_inputs[0]
            output = (1^node_values[input_node])
        elif gate == '^':
            input1, input2 = node_inputs
            output = node_values[input1] ^ node_values[input2]
        else:
            raise ValueError(f"Invalid gate type: {gate}")
        
        node_values[node] = output
        # print(str(node)+" "+str(output))
    
    return node_values['Z']

# Example usage

if __name__ == "__main__":
  circuit_file = "circuit.txt"
  fault_node = input("faulty node location:- ")
  fault_type = input("Please enter fault type (Stuck at 0(SA0) or Stuck at 1(SA1)):- ")
  
  test_vectors = generate_test_vectors(circuit_file, fault_node, fault_type)
  
  # print(test_vectors)
  # Print the test vectors and expected outputs
  with open("output.txt", "w") as output_file:
      for test_vector, expected_output in test_vectors:
          output_file.write(f"[A, B, C, D]: {list(test_vector)}, Z= {expected_output}\n")

print(f'Check output.txt for test pattern')