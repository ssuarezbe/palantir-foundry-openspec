# Upgrade

To move to a new OpenSpec version, rebuild the bundle, regenerate the reference output, read the diff, then update the skills and workspace by hand where needed.
Use a connected build machine. Do not skip the diff: the generated skills change between versions.
Tested here: the scripts on 1.16.0 only. The upgrade flow has not been run on a newer version.

## Steps

1. Edit `VER` in `maintainer/scripts/build.sh` and the pinned paths (`addons/cli/openspec-1.16.0`, `maintainer/tests/run-all.sh`, the launchers and the Jest test default path). Search for `1.16.0`.
2. Run `maintainer/scripts/sync-upstream.sh <new-version>`. It installs the package in a temp folder, runs `init --tools claude` and `--tools continue`, and prints the diff against `maintainer/upstream/generated/`.
3. Read the diff. Note changes to step order, new commands and new flags.
4. Run `maintainer/scripts/sync-upstream.sh <new-version> --write`. It replaces `maintainer/upstream/generated/` and rebuilds `addons/workspace/` with `maintainer/scripts/make-workspace.py`. The script keeps four workflows (explore, propose, apply, archive) plus the `openspec-sync-specs` skill, which the archive skill runs inline. Check that dependency still holds in the new version.
5. Run `maintainer/scripts/build.sh`. Both bundle patches must match. If one fails, upstream changed that code: look at the bundle and fix the pattern in `build.sh`. Do not remove the check.
6. Update `addons/cli/PIN.md`: version, integrity hash, SHA-256, date, audit result.
7. Fork the new schema: `openspec schema fork spec-driven foundry-spec-driven` in a scratch project. Compare it with `core/project-template/openspec/schemas/foundry-spec-driven/`. Re-apply the Foundry and Gherkin sections there. That folder is the only copy. Run `openspec schema validate foundry-spec-driven`.
8. Update `core/aip-skills/` by hand. Compare the new generated skills with the old, apply the same behavior changes in words, keep zero CLI calls and keep each skill under 150 lines.
9. Run `maintainer/tests/run-all.sh`. Fix failures. Add a fixture for any new validation rule the CLI enforces, and port the rule to `addons/ci/python/test_openspec_rules.py`.
10. Update `VERSION`, `CHANGELOG.md` and `THIRD_PARTY_NOTICES.md` (bundled packages change). Run `maintainer/scripts/build.sh --release`.
11. Send the zip and its `.sha256` through the approved transfer.

## What to confirm in Foundry

- That the new version's Node requirement is met in Checks and workspaces.
- That the multi-repository flow in `docs/multi-repo.md` still works: stores are beta. `maintainer/tests/run-all.sh` section 8 covers register, new change from a satellite, doctor and the unregistered-store error.
- That existing changes in `openspec/changes/` still validate with the new bundle before teams upgrade.
