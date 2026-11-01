from graph_valid.constants import BOOTSTRAP_SEED, BOOTSTRAP_REPLICATES

def test_canonical_bootstrap_configuration():
    assert BOOTSTRAP_SEED == 282049723644848642
    assert BOOTSTRAP_REPLICATES == 10_000
