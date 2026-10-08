import unittest

from chinese_remainder_theorem import solve, NotCoprimeError, ModulusTooSmallError


class TestSolve(unittest.TestCase):
    def test_single_congruence(self):
        self.assertEqual(solve([3], [5]), 3)

    def test_two_congruences(self):
        self.assertEqual(solve([2, 3], [3, 5]), 8)

    def test_classic_example(self):
        # x ≡ 2 mod 3, x ≡ 3 mod 5, x ≡ 2 mod 7  =>  23
        self.assertEqual(solve([2, 3, 2], [3, 5, 7]), 23)

    def test_solution_in_range(self):
        r = [1, 4, 6]
        m = [5, 7, 11]
        x = solve(r, m)
        self.assertGreaterEqual(x, 0)
        self.assertLess(x, 5 * 7 * 11)
        for ri, mi in zip(r, m):
            self.assertEqual(x % mi, ri)

    def test_zero_residue(self):
        self.assertEqual(solve([0, 0], [2, 3]), 0)

    def test_solution_is_product_minus_one(self):
        # x ≡ m_i - 1 for each i  =>  x = product - 1
        m = [3, 5, 7]
        r = [mi - 1 for mi in m]
        self.assertEqual(solve(r, m), 3 * 5 * 7 - 1)

    def test_residue_equal_to_modulus_minus_one(self):
        self.assertEqual(solve([4], [5]), 4)

    def test_residue_zero_modulus_one(self):
        # A modulus of 1 collapses to the trivial congruence x ≡ 0 (mod 1),
        # which every integer satisfies. This is the standard way to make a
        # congruence "drop out" without breaking coprimality.
        self.assertEqual(solve([2, 0], [3, 1]), 2)

    def test_large_pairwise_coprime(self):
        # 10^9+7, 10^9+9, 10^9+21 are pairwise coprime primes.
        m = [1000000007, 1000000009, 1000000021]
        r = [123456, 789012, 345678]
        x = solve(r, m)
        for ri, mi in zip(r, m):
            self.assertEqual(x % mi, ri)

    def test_non_coprime_raises(self):
        with self.assertRaises(NotCoprimeError):
            solve([1, 2], [2, 4])

    def test_non_coprime_with_later_pair(self):
        # First pair is fine (2,3); the third modulus shares a factor with 6.
        with self.assertRaises(NotCoprimeError):
            solve([0, 0, 0], [2, 3, 4])

    def test_residue_out_of_range_negative(self):
        with self.assertRaises(ModulusTooSmallError):
            solve([-1], [5])

    def test_residue_out_of_range_equal(self):
        with self.assertRaises(ModulusTooSmallError):
            solve([5], [5])

    def test_residue_out_of_range_later_pair(self):
        with self.assertRaises(ModulusTooSmallError):
            solve([1, 7], [3, 5])

    def test_modulus_must_be_positive(self):
        with self.assertRaises(ValueError):
            solve([1], [-5])

    def test_modulus_zero(self):
        with self.assertRaises(ValueError):
            solve([0], [0])

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            solve([1, 2], [3])

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            solve([], [])

    def test_rejects_bool(self):
        # bool subclasses int, but passing True as a modulus is a caller bug.
        with self.assertRaises(TypeError):
            solve([0], [True])

    def test_rejects_float(self):
        with self.assertRaises(TypeError):
            solve([2.0], [3.0])

    def test_duplicate_modulus_raises(self):
        with self.assertRaises(NotCoprimeError):
            solve([1, 2], [5, 5])


if __name__ == "__main__":
    unittest.main()
