import { execFileSync } from "child_process";
import * as fs from "fs";
import * as path from "path";

// Repository root: the nearest parent of this file that holds openspec/config.yaml.
// OPENSPEC_ROOT overrides it. OPENSPEC_CLI overrides the bundle path.
function findRoot(): string {
  if (process.env.OPENSPEC_ROOT) return process.env.OPENSPEC_ROOT;
  let dir = __dirname;
  while (!fs.existsSync(path.join(dir, "openspec", "config.yaml"))) {
    const parent = path.dirname(dir);
    if (parent === dir) throw new Error("openspec/config.yaml not found above " + __dirname);
    dir = parent;
  }
  return dir;
}

const root = findRoot();
const cli =
  process.env.OPENSPEC_CLI ||
  path.join(root, "tools", "openspec", "openspec-1.16.0", "dist", "cli", "openspec.mjs");

// A satellite repository declares `store: <id>` and keeps no specs. Its specs are validated in the spec home.
const satellite = /^store:/m.test(fs.readFileSync(path.join(root, "openspec", "config.yaml"), "utf8"));

(satellite ? describe.skip : describe)("OpenSpec", () => {
  it("validates all specs and changes (strict)", () => {
    if (!fs.existsSync(cli)) {
      throw new Error(`OpenSpec bundle not found at ${cli}. Copy cli/ from palantir-foundry-openspec to tools/openspec/, or set OPENSPEC_CLI.`);
    }
    try {
      execFileSync(process.execPath, [cli, "validate", "--all", "--strict", "--no-interactive"], {
        cwd: root,
        env: { ...process.env, OPENSPEC_TELEMETRY: "0" },
        stdio: "pipe",
        encoding: "utf8",
      });
    } catch (e: any) {
      throw new Error("openspec validate failed:\n" + (e.stdout || "") + (e.stderr || ""));
    }
  });
});
