import * as cp from "child_process";
import * as fs from "fs";
import * as path from "path";

// One-off probe. Copy it into the tests folder, commit, read the Checks log, then delete it.
// It always passes. It prints what this Checks environment allows and which situation in docs/setup.md fits.
// If this file fails to compile, the repository's tsconfig does not accept Node types (see tsconfig.snippet.json).

// Nearest parent folder that contains `name`, as openspec.test.ts finds the repository root.
function up(name: string): string | null {
  let dir = __dirname;
  for (;;) {
    if (fs.existsSync(path.join(dir, name))) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) return null;
    dir = parent;
  }
}

it("reports what Checks allows", () => {
  const [major, minor] = process.versions.node.split(".").map(Number);
  const nodeOk = major > 22 || (major === 22 && minor >= 12);
  let child = "no";
  try {
    child = cp.execFileSync(process.execPath, ["--version"], { encoding: "utf8" }).trim() === process.version ? "yes" : "no";
  } catch (e) {
    child = "no (" + String((e as Error).message).split("\n")[0] + ")";
  }
  const specRoot = up("openspec/config.yaml") ? "found" : "NOT found above this folder";
  const cli = process.env.OPENSPEC_CLI || path.join(up("openspec/config.yaml") || "", "tools", "openspec", "openspec-1.16.0", "dist", "cli", "openspec.mjs");
  const cliFound = fs.existsSync(cli);
  const situation = nodeOk && child === "yes" && cliFound ? "2 (CLI through Jest)" : "3 (TypeScript port, no CLI)";
  console.log(
    [
      "OPENSPEC PROBE",
      `  node ${process.version} (OpenSpec 1.16.0 wants 22.12 or newer): ${nodeOk ? "ok" : "too old"}`,
      `  child process: ${child.startsWith("yes") ? "allowed" : "blocked: " + child}`,
      `  openspec/config.yaml: ${specRoot}`,
      `  tools/openspec bundle: ${cliFound ? "present" : "not present"}`,
      `  use situation: ${situation}  (docs/setup.md)`,
    ].join("\n"),
  );
  expect(true).toBe(true);
});
