#!/usr/bin/env python
"""End to end tests for lib.flows.general.collectors."""


from grr.endtoend_tests import base
from grr.lib import flow_runner
from grr.lib.checks import checks as rdf_checks


class TestCheckRunner(base.AutomatedTest):
  """Test RunChecksFlow."""
  platforms = ["Linux"]
  flow = "CheckRunner"
  check_ids = [
      "CIS-LOGIN-UNIX-HASH", "CIS-NET-SYNCOOKIES", "CIS-SSH-PROTOCOL",
      "CIS-NET-LOGMART"
  ]
  args = {"restrict_checks": check_ids}

  def CheckFlow(self):
    results = self.CheckCollectionNotEmptyWithRetry(
        self.session_id.Add(flow_runner.RESULTS_SUFFIX), self.token)
    checks_run = [
        r.check_id for r in results if isinstance(r, rdf_checks.CheckResult)
    ]
    # Verify the expected checks were run.
    self.assertItemsEqual(self.check_ids, checks_run)
