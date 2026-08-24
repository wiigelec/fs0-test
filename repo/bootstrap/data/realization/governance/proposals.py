#!/usr/bin/env python3
from __future__ import annotations

class ProposalLineageError(ValueError):
    pass

def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())

def validate_seed_correction(seed, correction):
    if not isinstance(seed, dict) or not isinstance(correction, dict):
        raise ProposalLineageError("proposal records must be objects")

    seed_id = seed.get("proposal_id")
    correction_id = correction.get("proposal_id")
    if not _nonempty(seed_id) or not _nonempty(correction_id):
        raise ProposalLineageError("proposal_id is required")

    if seed.get("bootstrap_provenance") != "bootstrap-seed":
        raise ProposalLineageError("source proposal is not a bootstrap-installed seed")

    if correction_id == seed_id:
        raise ProposalLineageError("bootstrap-installed seed proposal cannot be corrected in place")

    predecessor = correction.get("predecessor_id")
    if predecessor != seed_id:
        raise ProposalLineageError(
            "seed correction must explicitly identify the corrected seed as predecessor"
        )

    if correction.get("bootstrap_provenance") == "bootstrap-seed":
        raise ProposalLineageError(
            "post-bootstrap correction must not masquerade as an original bootstrap seed"
        )

    return correction
