# Exact reference compiler

`compiler.py` implements the graph recovery construction in Python 3.10 or later using the standard library. It enumerates the surviving logical Pauli representatives, solves the minimum weighted $T$-join for each candidate pair, and returns a circuit attaining the smallest cost.

## Run the example

From the repository root, recover the five-qubit code at the middle site of a line after erasing both endpoints.

```python
from verification.compiler import compile_recovery

choi = ('+IXZZXI', '+IIXZZX', '+IXIXZZ', '+IZXIXZ', '+XXXXXX', '+ZZZZZZ')
line = [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)]
result = compile_recovery(choi, erased=(0, 4), hardware=line, output=2)

print(result.cost)         # 2
print(result.join_edges)   # ((1, 2), (2, 3))
for operation in result.operations:
    print(operation)
```

### Inputs

| Argument | Format |
| --- | --- |
| `generators` | For $n$ physical sites, supply $n+1$ independent commuting generators of the pure Choi stabilizer state. Each string has an optional `+` or `-` sign and $n+1$ letters from `IXYZ`. The first Pauli acts on the inaccessible reference. The remaining letters correspond to physical sites `0` through `n-1`. The reference must be maximally mixed. |
| `erased` | Indices of erased sites. Edges to these sites are dropped by default. |
| `hardware` | Undirected edges `(u, v, cost)` with distinct endpoints and nonnegative integer or `fractions.Fraction` costs. List each edge once. The word length defines the vertices, including isolated sites. |
| `output` | One available physical site designated to hold the recovered logical qubit. |
| `relay_erased` | Optional subset of `erased` whose hardware can be reset to a fresh qubit and reused. These sites keep their incident edges and can serve as outputs. To supply an extra fresh site, append it to the Choi words and add a separate product-state `+Z` stabilizer for that qubit. |

`NoRecovery` reports a missing pair of surviving logical representatives or hardware connectivity that prevents recovery at the designated site. Malformed input raises `ValueError`.

### Output certificate

| Field | Meaning |
| --- | --- |
| `cost` | Sum of the charged CNOT edge weights. |
| `join_edges` | Selected forest with one CNOT on each listed edge. |
| `logical_x`, `logical_z` | Signed physical Pauli words before synthesis, with an `I` for each erased physical input. Appending the corresponding reference `X` or `Z` on the left gives an element of the supplied Choi stabilizer group. |
| `operations` | The ordered sequence of operations on physical sites. |

`H` and `S` denote the one-qubit Hadamard and phase gates. `CNOT` lists the control followed by the target. `RESET` prepares $\lvert0\rangle$ on its named site. `MEASURE_X`, `MEASURE_Y` and `MEASURE_Z` record a bit indexed by site, with bit `0` for eigenvalue $+1$. For `CORRECT_X` and `CORRECT_Z`, apply the indicated Pauli on the output exactly when the recorded bits listed in `parity`, XORed with `offset`, equal `1`.

The implementation uses exact graph costs. It enumerates the shortened stabilizer group once, then uses subset dynamic programming for each distinct minimum-weight matching of terminals. The representative search and the worst-case matching cost are exponential, so this implementation is for small instances and independent checks.

## Run the checks

```sh
python3 -m unittest discover -s verification -v
```

The tests use a separate state-vector simulator to prepare signed Choi states, trace out erased inputs, and check the two output Bell stabilizers on every nonzero circuit branch. Tests cover all zero-, one- and two-erasure patterns and surviving output sites of the five-qubit code on the complete graph, weighted and zero-cost edge cases, resettable relays and unavailable logical information.
