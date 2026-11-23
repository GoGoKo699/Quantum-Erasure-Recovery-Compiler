"""Independent state-vector checks for the compiled circuits."""

from fractions import Fraction
from itertools import combinations
from math import sqrt
import unittest

from compiler import NoRecovery, compile_recovery


FIVE_QUBIT = ('+IXZZXI', '+IIXZZX', '+IXIXZZ', '+IZXIXZ', '+XXXXXX', '+ZZZZZZ')
LINE = [(i, i + 1, 1) for i in range(4)]


def pauli_on(state, word):
    """Apply a signed tensor-product Pauli in little-endian site order."""
    sign = -1 if word.startswith('-') else 1
    letters = word.lstrip('+-')
    moved = [0j] * len(state)
    for basis, alpha in enumerate(state):
        mapped = basis
        phase = sign
        for k, axis in enumerate(letters):
            bit = (basis >> k) & 1
            if axis in 'XY':
                mapped ^= 1 << k
            if axis == 'Y':
                phase *= -1j if bit else 1j
            if axis == 'Z' and bit:
                phase *= -1
        moved[mapped] = phase * alpha
    return moved


def at_site(state, site, axis):
    n = len(state).bit_length() - 1
    return pauli_on(state, 'I' * site + axis + 'I' * (n - site - 1))


def norm_squared(state):
    return sum(abs(a)**2 for a in state)


def project(state, evolved, outcome):
    sign = (-1)**outcome
    return [(a + sign * b) / 2 for a, b in zip(state, evolved)]


def choi_state(stabilizers):
    size = 1 << len(stabilizers)
    for basis in range(size):
        state = [0j] * size
        state[basis] = 1
        for generator in stabilizers:
            state = project(state, pauli_on(state, generator), 0)
        norm = norm_squared(state)
        if norm:
            return [a / sqrt(norm) for a in state]
    raise ValueError('empty Choi subspace')


def branches_after(state, gate, sites, recorded):
    first = sites[0] + 1
    mask = 1 << first
    if gate == 'H':
        yield [(state[i ^ mask] - a if i & mask else a + state[i ^ mask]) / sqrt(2)
               for i, a in enumerate(state)], recorded
    elif gate == 'S':
        yield [a * 1j if i & mask else a for i, a in enumerate(state)], recorded
    elif gate == 'CNOT':
        target = 1 << (sites[1] + 1)
        yield [state[i ^ target] if i & mask else a for i, a in enumerate(state)], recorded
    else:
        axis = 'Z' if gate == 'RESET' else gate[-1]
        evolved = at_site(state, first, axis)
        for outcome in (0, 1):
            piece = project(state, evolved, outcome)
            if norm_squared(piece) < 1e-20:
                continue
            if gate == 'RESET':
                yield at_site(piece, first, 'X') if outcome else piece, recorded
            else:
                assert gate.startswith('MEASURE_')
                yield piece, recorded | {sites[0]: outcome}


def execute(generators, erased, circuit):
    branches = [(choi_state(generators), {})]
    instructions = [('RESET', (site,), (), 0) for site in erased]
    instructions += [(op.gate, op.sites, op.parity, op.offset) for op in circuit]
    for gate, sites, parity, offset in instructions:
        if gate.startswith('CORRECT_'):
            branches = [
                (at_site(state, sites[0] + 1, gate[-1])
                 if (offset + sum(outcomes[i] for i in parity)) % 2 else state,
                 outcomes)
                for state, outcomes in branches
            ]
        else:
            branches = [next_branch for state, outcomes in branches
                        for next_branch in branches_after(state, gate, sites, outcomes)]
    return branches


class RecoveryTests(unittest.TestCase):
    def assert_bell_recovered(self, generators, erased, output, result):
        branches = execute(generators, erased, result.operations)
        self.assertAlmostEqual(sum(norm_squared(state) for state, _ in branches), 1)
        for state, _ in branches:
            for axis in 'XZ':
                evolved = at_site(at_site(state, 0, axis), output + 1, axis)
                self.assertLess(sum(abs(a - b)**2 for a, b in zip(state, evolved)), 1e-20)
        cnot_edges = [tuple(sorted(op.sites)) for op in result.operations if op.gate == 'CNOT']
        self.assertEqual(tuple(sorted(cnot_edges)), result.join_edges)

    def test_five_qubit_two_erasures_on_line(self):
        erased = (0, 4)
        for output, cost in ((1, 1), (2, 2), (3, 1)):
            with self.subTest(output=output):
                result = compile_recovery(FIVE_QUBIT, erased, LINE, output)
                self.assertEqual(result.cost, cost)
                self.assert_bell_recovered(FIVE_QUBIT, erased, output, result)

    def test_exact_fractional_costs_and_zero_weight_cycle(self):
        for weights, selected in (((Fraction(3, 2), Fraction(3, 2), Fraction(5, 2)), Fraction(5, 2)),
                                  ((0, 0, 0), 0)):
            with self.subTest(weights=weights):
                graph = [(1, 2, weights[0]), (2, 3, weights[1]), (1, 3, weights[2])]
                result = compile_recovery(FIVE_QUBIT, (0, 4), graph, 2)
                self.assertEqual(result.cost, selected)
                self.assertEqual(result.join_edges, ((1, 3),))
                self.assert_bell_recovered(FIVE_QUBIT, (0, 4), 2, result)

    def test_all_five_qubit_recoverable_erasures_on_complete_graph(self):
        graph = [(i, j, 1) for i, j in combinations(range(5), 2)]
        for erased_count in range(3):
            for erased in combinations(range(5), erased_count):
                for output in sorted(set(range(5)) - set(erased)):
                    with self.subTest(erased=erased, output=output):
                        result = compile_recovery(FIVE_QUBIT, erased, graph, output)
                        self.assertEqual(result.cost, int(erased_count == 2))
                        self.assert_bell_recovered(FIVE_QUBIT, erased, output, result)

    def test_disconnected_vs_resettable_relays(self):
        erased = (1, 3)
        with self.assertRaisesRegex(NoRecovery, 'connectivity'):
            compile_recovery(FIVE_QUBIT, erased, LINE, 2)
        result = compile_recovery(FIVE_QUBIT, erased, LINE, 2, relay_erased=erased)
        self.assertEqual(result.cost, 4)
        self.assert_bell_recovered(FIVE_QUBIT, erased, 2, result)
        moved_output = compile_recovery(FIVE_QUBIT, (0,), LINE, 0, relay_erased=(0,))
        self.assertEqual(moved_output.cost, 1)
        self.assert_bell_recovered(FIVE_QUBIT, (0,), 0, moved_output)

    def test_charged_operations_cannot_replace_missing_logical_information(self):
        with self.assertRaisesRegex(NoRecovery, 'no joint logical'):
            compile_recovery(FIVE_QUBIT, (0, 1, 2), LINE, 3, relay_erased=(0, 1, 2))

    def test_signed_generators_and_validation(self):
        rotated_bell = ('-XY', '-ZZ')
        result = compile_recovery(rotated_bell, (), (), 0)
        self.assertEqual(result.cost, 0)
        self.assertEqual(result.logical_x, '-Y')
        self.assertEqual(result.logical_z, '-Z')
        self.assert_bell_recovered(rotated_bell, (), 0, result)
        with self.assertRaisesRegex(ValueError, 'commute'):
            compile_recovery(('+XX', '+ZI'), (), (), 0)
        with self.assertRaisesRegex(ValueError, 'maximally mixed'):
            compile_recovery(('+XI', '+IZ'), (), (), 0)
        with self.assertRaisesRegex(ValueError, 'available'):
            compile_recovery(FIVE_QUBIT, (0,), LINE, 0)


if __name__ == '__main__':
    unittest.main()
