import { readFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";

const root = dirname(dirname(fileURLToPath(import.meta.url)));

async function expectContains(file, fragments) {
  const source = await readFile(join(root, file), "utf8");
  for (const fragment of fragments) {
    assert.ok(source.includes(fragment), `${file} should contain ${fragment}`);
  }
}

await expectContains("src/app/inventory/page.tsx", [
  "Add System",
  "Edit System",
  "Assessment Target",
  "Scanner Compatibility",
  "Manual review only",
  "Archive",
  "createSystem",
  "updateSystem",
]);

await expectContains("src/app/workflows/page.tsx", [
  "Guided Operator Workflow",
  "Target location",
  "Choose Assessment Profile",
  "Review Recommended Scans",
  "No automated scanner is compatible",
  "Create and run first scan",
  "createAssessment",
  "executeScannerRun",
]);

await expectContains("src/app/scanners/page.tsx", [
  "Target type",
  "Target location",
  "Assessment method",
  "No enabled scanner matches this system target",
]);

await expectContains("src/app/findings/page.tsx", [
  "Save triage",
  "Initiate retest",
  "Accept risk",
  "Mark false positive",
  "transitionFinding",
]);

await expectContains("src/app/evidence/page.tsx", [
  "Evidence Detail",
  "Chain of evidence",
  "Artifact references",
  "scanner_run_id",
]);

await expectContains("src/app/review-board/page.tsx", [
  "AIRB Intake",
  "Create intake",
  "Exception expiration",
  "approved_with_exception",
  "updateAirbReview",
]);

await expectContains("src/components/navigation.tsx", ["Guided Workflow", "/workflows"]);
