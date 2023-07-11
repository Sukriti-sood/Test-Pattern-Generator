primary_inputs = []

# Function   [find_pifind_pi]
# Synopsis   [ usage:	Return primary inputs used in the circuit.


#              description:
# 								This functions add primary inputs to list.
#                Arguments:
#                  circuit
#            ]
# **************************************************************************
def find_pi(circuit):
    for key in circuit.keys():
        for node in circuit[key]["inputs"]:
            if "net_" not in node:
                primary_inputs.append(node)
    primary_inputs.sort()


def generate_test_vectors(circuit_file, fault_node, fault_type):
    # Read the circuit file and parse the circuit
    circuit = parse_circuit_file(circuit_file)

    find_pi(circuit)

    # Initialize visited dictionary to keep track of backtracked nodes.
    vis = {}

    # Initialize node_values to keep setting values to the nodes
    node_values = {}

    # Initialize the test vectors
    test_vector = []

    # Determine the test value based on the fault type
    if fault_type == "SA0":
        test_value = 1
    elif fault_type == "SA1":
        test_value = 0
    else:
        raise ValueError("Invalid fault type")

    dfs(circuit, fault_node, test_value, vis, node_values)

    if fault_node != "Z":
        set_farward_path_of_fault_node(circuit, "Z", vis, node_values)

    # Generate the test vectors
    for pi in primary_inputs:
        test_vector.append(node_values[pi])

    ans = [test_vector, node_values["Z"]]

    return ans


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

    with open(circuit_file, "r") as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()

            if line.startswith("net_"):
                node, equation = line.split("=")

                circuit[node.strip()] = parse_equation(equation.strip())
            elif line.startswith("Z"):
                circuit["Z"] = parse_equation(line.split("=")[1].strip())
    return circuit


# a = b^c
# Function   [ parse_equation]
# Synopsis   [ usage:	Parse lines in circuit.txt file.


#              description:
# 								This functions is responsible to creates edges between gate nodes.
#                Arguments:
#                  a line of circuit.txt file (equation)
#            ]
# **************************************************************************
def parse_equation(equation):
    if "&" in equation:
        gate = "&"
        inputs = equation.split("&")
    elif "|" in equation:
        gate = "|"
        inputs = equation.split("|")
    elif "~" in equation:
        gate = "~"
        inputs = [equation[1:].strip()]
    elif "^" in equation:
        gate = "^"
        inputs = equation.split("^")
    else:
        raise ValueError(f"Invalid gate in equation: {equation}")

    return {"gate": gate, "inputs": [input_node.strip() for input_node in inputs]}


# Function   [ dfs ]
# Synopsis   [ usage:	Backtrack from a node and keep setting values accordingly.


#              description:
#                  this function dfs from a perticular node to the inputs and sets the values of nodes in the path
#                Arguments:
#                  circuit (circuit graph)
#                  node from which to dfs
#                  vis : visited dictionary to check if already backtracked or not.
#                  node_values: node_values dictionary
#            ]
# **************************************************************************
def dfs(circuit, current_node, value, vis, node_values):
    node_values[current_node] = value
    vis[current_node] = 1
    # if current_node is primary input no need to go further
    if current_node in primary_inputs:
        return
    gate = circuit[current_node]["gate"]
    val = 1
    if gate == "&":
        val = value
    elif gate == "|":
        val = value
    elif gate == "~":
        val = value ^ 1
    else:
        cnt = 0
        for node in circuit[current_node]["inputs"]:
            if cnt == 0 and value == 1:
                dfs(circuit, node, 1, vis, node_values)
            else:
                dfs(circuit, node, 0, vis, node_values)
            cnt += 1
        return
    for node in circuit[current_node]["inputs"]:
        dfs(circuit, node, val, vis, node_values)


# Function   [ set_farward_path_of_fault_node]
# Synopsis   [ usage:	set values in the forward path of fault node.


#              description:
# 								This functions is responsible to set values in the forward path.
#                Arguments:
#                  circuit, current node, visited dictionary, node values
#            ]
# **************************************************************************
def set_farward_path_of_fault_node(circuit, current_node, vis, node_values):
    if current_node in primary_inputs:
        return
    gate = circuit[current_node]["gate"]
    val = 1
    for nodes in circuit[current_node]["inputs"]:
        if vis.get(nodes) is None:
            set_farward_path_of_fault_node(circuit, nodes, vis, node_values)
    for node in circuit[current_node]["inputs"]:
        if vis.get(node) is not None:
            value = node_values[node]
            ans = value
            if gate == "&":
                val = 1
            elif gate == "|":
                val = 0
            else:
                val = value ^ 1
            for nds in circuit[current_node]["inputs"]:
                if vis.get(nds) is None:
                    com = str(ans) + gate + str(val)
                    ans = eval(com)
                    dfs(circuit, nds, val, vis, node_values)
            node_values[current_node] = ans
            vis[current_node] = 1
            return


# Example usage
if __name__ == "__main__":
    circuit_file = "circuit.txt"
    fault_node = input("faulty node location:- ")
    fault_type = input(
        "Please enter fault type (Stuck at 0(SA0) or Stuck at 1(SA1)):- "
    )

    ans = generate_test_vectors(circuit_file, fault_node, fault_type)


    # Print the test vectors and expected outputs
    with open("output.txt", "w") as output_file:
        test_vector = ans[0]
        expected_output = ans[1]
        output_file.write(
            f"{list(primary_inputs)}: {list(test_vector)}, Z= {expected_output}\n"
        )

print("Check output.txt for test pattern")
