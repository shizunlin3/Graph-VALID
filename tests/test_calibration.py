import math
import numpy as np

from graph_valid.constants import MEFF_SNP, MEFF_SV, B3_THRESHOLD_SNP, B3_THRESHOLD_SV
from graph_valid.calibration import empirical_p_value

def test_manuscript_thresholds():
    assert math.isclose(B3_THRESHOLD_SNP, 2.1758637166641537e-07, rel_tol=0, abs_tol=1e-20)
    assert math.isclose(B3_THRESHOLD_SV, 3.813281095840094e-06, rel_tol=0, abs_tol=1e-20)

def test_empirical_p_value():
    null = np.array([0.01, 0.02, 0.03, 0.9])
    assert empirical_p_value(0.025, null) == 3/5
