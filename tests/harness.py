"""Test infrastructure for the Ontoloop suite.

This module is test infrastructure only. It is not product code.

It provides two helpers every seat in the test writing wave uses:

require(module_name)
    Import the named product module and return it. The product is
    built at Step 14, so a product module that does not exist yet
    fails the calling test individually and legibly with an
    AssertionError whose message starts with the prefix
    "NOT BUILT (Step 14): " followed by the module name.

stage_carried(reason)
    Fail the calling test with an AssertionError whose message
    starts with the prefix "STAGE-CARRIED: " followed by the reason.
    Stage carried rows run against a later stage or a real target;
    they are never skipped and never passed at this step.
"""

import importlib

NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "
STAGE_CARRIED_PREFIX = "STAGE-CARRIED: "


def require(module_name):
    """Return the named product module, or fail as not built."""
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        missing = exc.name or ""
        if missing == module_name or module_name.startswith(missing + "."):
            raise AssertionError(NOT_BUILT_PREFIX + module_name) from None
        raise


def stage_carried(reason):
    """Fail the calling test as stage carried, with the reason."""
    raise AssertionError(STAGE_CARRIED_PREFIX + reason)
