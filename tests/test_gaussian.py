import unittest

import numpy as np

from diderot_mls.gaussian import anomaly_mask, estimate_parameters, gaussian_pdf


class GaussianTests(unittest.TestCase):
    def test_standard_normal_peak(self) -> None:
        expected = 1 / np.sqrt(2 * np.pi)
        self.assertAlmostEqual(float(gaussian_pdf(0.0, 0.0, 1.0)), expected)

    def test_density_integrates_to_one(self) -> None:
        x = np.linspace(-10.0, 10.0, 200_001)
        area = np.trapezoid(gaussian_pdf(x, 0.0, 1.0), x)
        self.assertAlmostEqual(float(area), 1.0, places=6)

    def test_maximum_likelihood_estimates(self) -> None:
        mu, variance = estimate_parameters(np.array([8, 9, 10, 11, 12]))
        self.assertAlmostEqual(mu, 10.0)
        self.assertAlmostEqual(variance, 2.0)

    def test_anomaly_mask(self) -> None:
        flags = anomaly_mask(np.array([0.0, 5.0]), 0.0, 1.0, epsilon=1e-3)
        self.assertEqual(flags.tolist(), [False, True])

    def test_invalid_sigma(self) -> None:
        with self.assertRaises(ValueError):
            gaussian_pdf(0.0, 0.0, 0.0)


if __name__ == "__main__":
    unittest.main()
