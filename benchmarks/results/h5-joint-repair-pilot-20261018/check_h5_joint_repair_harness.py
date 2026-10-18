"""Reuse the existing adversarial tests for unchanged paired/scoring functions."""
from pathlib import Path
import sys
import unittest
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'scripts'))
import h5_joint_repair_pilot as pilot
import test_h5_early_exchange_pilot as tests
tests.pilot=pilot
names=['test_original_material_failures_stay_failures_despite_improvement',
       'test_missing_duplicate_and_failed_seeds_never_get_complete_comparison',
       'test_nonfinite_invalid_scores_and_missing_cut_savings_are_not_scored',
       'test_each_block_keeps_all_arms_and_balances_order_across_seeds',
       'test_expired_session_preserves_failure_without_starting_a_process']
suite=unittest.TestSuite(tests.PilotSummaryTests(name) for name in names)
with (root/'output/h5-joint-repair-probe-20261018/pilot-harness-tests.log').open('x',encoding='utf-8',newline='\n') as stream:
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
assert result.wasSuccessful()
print('Five existing adversarial paired-method tests passed.')
