# Test Pattern Generator

Implementation of Test Pattern Genereation algorithm in python based upon path sensitization algorithm.

## RUN

``` python3 main.py```

## INPUT

- Circuit File *circuit.txt*
- Fault Location (Any node in the circuit)
- Fault Type (Stuck at 0 ---> SA0) OR (Stuck at 0 ---> SA1)

### Circuit Format

- The circuit will have 4 inputs - A, B, C and D. All of which are boolean type (only 0 and 1 are valid inputs)
- The circuit’s output will always be Z which is also a boolean.
- The circuit will be built using the following operations -
  - AND ( & ) gate
  - OR ( | ) gate
  - NOT ( ~ ) gate
  - XOR ( ^ ) gate
- The circuit would purely be a combinational logic.
- All internal nodes in the circuit would be named as : “net_<alphanumeric string>”
- Each input ( A / B / C / D ) would be utilized only once in the circuit.
- Gates take only two inputs
- There are no fanout branches in the circuit


## OUTPUT

Test vector and expected output is printed in *output.txt* file.

## Simulation
![SImulation](https://github.com/Sukriti-sood/Test-Pattern-Generator/assets/55010599/2e6a8dda-b2ac-405d-9da7-bea2c8edaff6)

