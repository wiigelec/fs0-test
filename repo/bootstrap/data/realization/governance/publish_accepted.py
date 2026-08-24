#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="repo/scripts/publish-accepted",
        description="Retired compatibility entrypoint; governed PR merge publishes accepted state.",
    )
    parser.add_argument("--candidate")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = {
        "schema_version": "1",
        "record_type": "accepted-state-publication-result",
        "status": "retired",
        "errors": [
            "publish-accepted is retired; merge an eligible governed pull request into refs/heads/main"
        ],
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("FS0 accepted-state publication: RETIRED")
        print(report["errors"][0], file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
