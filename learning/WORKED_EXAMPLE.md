# Worked recovery on three surviving sites

After two known losses in the five-qubit code, local Clifford changes of axis put the surviving Choi correlations in the following form. Local Pauli corrections absorb signs.

```math
P=X_R X_a X_b X_o,\qquad Q=Z_R Z_a Z_b Z_o.
```

The hardware sites contribute three local anticommutations. To leave only the output $`o`$, toggle sites $`a`$ and $`b`$. If they share a unit-cost edge, that edge is the T-join.

Conjugate by CNOT from $`a`$ to $`b`$.

```math
P'=X_R X_a X_o,\qquad Q'=Z_R Z_b Z_o.
```

Measure $`X_a`$ and $`Z_b`$ with outcomes $`s_X,s_Z\in\{+1,-1\}`$. The two correlations become $`s_X X_R X_o`$ and $`s_Z Z_R Z_o`$. If $`s_X=-1`$, apply $`Z_o`$. If $`s_Z=-1`$, apply $`X_o`$. Every possible measurement record now gives the standard Bell state on the reference and output. By the Choi representation, the decoder acts as the identity on the unknown qubit.

## Change the graph

A path through available relays can move one anticommutation to the other. At a relay where both tracked factors are identity, reset to the positive $`Z`$ eigenstate and multiply the second generator by that local $`Z`$. The factors on the edge have the form $`X_a I`$ and $`Z_a Z`$, so one CNOT moves the anticommutation forward. It cancels against the one at $`b`$ on the last edge.

| Available connections | Terminals | Minimum CNOT count |
|---|---|---:|
| The edge between $`a`$ and $`b`$ | $`\{a,b\}`$ | 1 |
| A path of length $`L`$ between them | $`\{a,b\}`$ | $`L`$ |
| Separate components for $`a`$ and $`b`$ | $`\{a,b\}`$ | Infeasible |

On a three-site line with the middle as output, the two endpoints are terminals and both edges are required. See the [benchmarks](../science/benchmarks.md) for layouts with unavailable or resettable loss sites.
