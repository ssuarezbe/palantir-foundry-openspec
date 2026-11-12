#!/bin/sh
# Connected build machine only. Installs the Jest harness used by tests/run-all.sh.
# After this, run-all.sh works offline. Nothing here is shipped to Foundry.
set -eu
cd "$(dirname "$0")/../tests/jest-env"
npm install --ignore-scripts --no-audit --no-fund
