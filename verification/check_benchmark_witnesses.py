"""Reproduce the five-qubit and Steane hardware benchmarks."""

from collections import Counter
from itertools import combinations

from compiler import NoRecovery, compile_recovery


FIVE_QUBIT = [
    'IXZZXI', 'IIXZZX', 'IXIXZZ', 'IZXIXZ', 'XXXXXX', 'ZZZZZZ',
]


def complete_graph(sites):
    return [(u, v, 1) for u, v in combinations(sorted(sites), 2)]


def cost(generators, lost, graph, output, relays=()):
    try:
        recovery = compile_recovery(generators, lost, graph, output, relay_erased=relays)
    except NoRecovery:
        return None
    assert sum(operation.gate == 'CNOT' for operation in recovery.operations) == recovery.cost
    return recovery.cost


def check_five_qubit():
    sites = set(range(5))
    line = [(u, u + 1, 1) for u in range(4)]
    removed_counts = Counter()
    reset_counts = Counter()

    for lost in combinations(sorted(sites), 2):
        survivors = sites.difference(lost)
        for output in sorted(survivors):
            assert cost(FIVE_QUBIT, lost, complete_graph(survivors), output) == 1
            a, b = sorted(survivors - {output})
            expected_removed = b - a if set(range(a, b + 1)) <= survivors else None
            removed = cost(FIVE_QUBIT, lost, line, output)
            assert removed == expected_removed
            removed_counts[removed] += 1
            reset = cost(FIVE_QUBIT, lost, line, output, relays=lost)
            assert reset == b - a
            reset_counts[reset] += 1

    assert removed_counts == {1: 12, 2: 3, None: 15}
    assert reset_counts == {1: 12, 2: 9, 3: 6, 4: 3}


def steane_generators():
    checks = [
        'I' + ''.join(axis if label & bit else 'I' for label in range(1, 8))
        for axis in ('X', 'Z')
        for bit in (1, 2, 4)
    ]
    return checks + ['X' * 8, 'Z' * 8]


def check_steane():
    generators = steane_generators()
    sites = set(range(7))

    for lost in combinations(sorted(sites), 2):
        t = ((lost[0] + 1) ^ (lost[1] + 1)) - 1
        survivors = sites.difference(lost)
        hardware = complete_graph(survivors)
        for output in sorted(survivors):
            assert cost(generators, lost, hardware, output) == (0 if output == t else 1)
            if output != t:
                partner = ((output + 1) ^ (t + 1)) - 1
                assert partner in survivors - {t, output}
                assert cost(generators, lost, [(t, partner, 1)], output) == 1
                assert cost(generators, lost, [], output) is None


if __name__ == '__main__':
    check_five_qubit()
    check_steane()
    print('Five-qubit and Steane benchmark costs verified.')
