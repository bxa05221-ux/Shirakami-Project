"""Run the minimal Shirakami Core Conformance suite.

The suite deliberately selects only authority-preservation tests. It is not a
replacement for the broader regression suite; it is the small gate that must
remain green before a build can claim core conformance.
"""
from __future__ import annotations

import subprocess
import sys

CORE_TESTS = [
    "scripts/test_verification_integrity.py",
    "scripts/test_verification_forgery.py",
    "scripts/test_verifier_authenticity.py",
    "scripts/test_verifier_provenance.py",
    "scripts/test_independent_verifier.py",
    "scripts/test_cross_layer_authority_chain.py",
    "scripts/test_full_human_gate.py",
    "scripts/test_human_gate_authenticity.py",
    "scripts/test_human_identity_auth.py",
    "scripts/test_human_decision_replay.py",
    "scripts/test_decision_binding.py",
    "scripts/test_end_to_end_integrity.py",
    "scripts/test_full_system_authority.py",
]

def main() -> int:
    cmd = [sys.executable, "-m", "pytest", "-q", *CORE_TESTS]
    print("SHIRAKAMI CORE CONFORMANCE")
    print("tests:", len(CORE_TESTS))
    print("principle: verification PASS != authorization")
    print("principle: AI/runtime output cannot become human authority")
    print("principle: mutation/provenance/identity changes must fail closed")
    return subprocess.call(cmd)

if __name__ == "__main__":
    raise SystemExit(main())
