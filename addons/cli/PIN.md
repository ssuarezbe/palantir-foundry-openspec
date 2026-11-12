# Upstream pin

| Item | Value |
| --- | --- |
| Package | `@fission-ai/openspec` |
| Version | 1.16.0 |
| Licence | MIT |
| npm integrity | `sha512-WQVhZoIR5PoacH/H0qh84VKMcXFbKCIKuAI96arHS3KiKYhJStlRrjUKGxLqLYKLym0j+2hAAY5MZUrPE5qXIA==` |
| npm tarball SHA-1 | `580efe69fa63b5678ca9b9fc9d94de139df68915` |
| SHA-256 of `addons/cli/openspec-1.16.0/dist/cli/openspec.mjs` | `6cc32f74b918356c2c80a1bf4208aeb72602972651f666d2f6ff107aa8ff328b` |
| Built | 2026-11-10 |
| Kit version | 1.16.0-foundry.4 |

`addons/cli/SHA256SUMS` holds the same SHA-256. `maintainer/tests/run-all.sh` checks it.

## How it was built

Run `maintainer/scripts/build.sh`. It does this:

1. `npm ci --ignore-scripts` in a temporary folder, from the lock of record in `maintainer/scripts/pinned/` (package.json and package-lock.json). The npm package ships no lockfile, so without this its 57 bundled dependencies resolve fresh on every build and the bundle changes.
2. `bun build <pkg>/bin/openspec.js --target=node --format=esm --outfile addons/cli/openspec-1.16.0/dist/cli/openspec.mjs`.
3. Patches two places in the bundle (see below).
4. Copies the package's `package.json` and `schemas/` next to `dist/`.
5. Writes the SHA-256, the licence texts of the 57 bundled packages and the bundled-package table.

Build machine: macOS, Node 20.19.3, npm 10.8.2, Bun 1.2.19. Two builds in a row from the pinned lock give the same SHA-256. Not yet checked on another machine or Bun version.

History: kit builds `foundry.1` and `foundry.2` were made before the lock existed (SHA-256 `bf48784f41eb3ad72f19cbfc0a6c0667f6d64e51cd1f7dc24906a848b03750fe`). A rebuild a day later gave a different hash because a dependency had moved. That bundle cannot be recreated. If a zip from before `foundry.4` was transferred anywhere, replace it.

## Local changes to upstream code

`maintainer/scripts/build.sh` edits two lines of the bundle with `sed`. It fails if either pattern is not found exactly once. Nothing else is changed.

1. **Schemas path.** Upstream looks for `schemas/` at `../../../schemas` from its own file. That is right for the npm layout and wrong for a single-file bundle at `dist/cli/`. The path becomes `../../schemas`, so `schemas/` sits inside `addons/cli/openspec-1.16.0/`.
2. **Double start.** Upstream `index.js` starts the CLI when it is the entry file, and `bin/openspec.js` starts it again. In a one-file bundle both run, so every command ran twice (duplicate output, and `archive` failed on its own lock). The self-start guard is changed to `if (false)`.

`maintainer/tests/run-all.sh` checks that a command prints once.

## Node version

Upstream `engines` says `node >=22.12.0`. The bundle was built and tested here on Node 20.19.3 and works there. That is outside upstream's stated support. Confirm the Node version in your Foundry environments (see docs/setup.md).

## Registry signatures

`npm audit signatures` on the build machine, 2026-11-10:

```
57 packages have verified registry signatures
22 packages have verified attestations
```

## Generated reference

In the source repository, `maintainer/upstream/generated/claude/` and `maintainer/upstream/generated/continue/` are the raw output of `openspec init --tools claude` and `--tools continue` (telemetry off). Do not edit them. They are the diff baseline for upgrades.
