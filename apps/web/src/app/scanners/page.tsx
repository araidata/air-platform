"use client";

import { useEffect, useMemo, useState } from "react";
import {
  AlertTriangle,
  Braces,
  CheckCircle2,
  FileJson,
  Play,
  RefreshCw,
  ShieldAlert,
  TerminalSquare,
} from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { PageHeader } from "@/components/page-header";
import { type ApiAssessmentToolRun, type ApiScannerAdapter, apiClient } from "@/lib/api-client";
import { formatDate, labelize, StatusPill, statusTone } from "@/lib/format";

const testOptions = [
  { id: "prompt_injection", label: "Prompt Injection" },
  { id: "jailbreak", label: "Jailbreak" },
  { id: "system_prompt_leakage", label: "System Prompt Leakage" },
  { id: "encoding_obfuscation", label: "Encoding / Obfuscation" },
  { id: "toxicity_unsafe_content", label: "Toxicity / Unsafe Content" },
  { id: "pii_leakage", label: "PII Leakage" },
  { id: "policy_bypass", label: "Policy Bypass" },
];

const garakTestIds = new Set([
  "prompt_injection",
  "jailbreak",
  "system_prompt_leakage",
  "encoding_obfuscation",
  "toxicity_unsafe_content",
]);

const defaultTemplate = `{
  "prompt": "{{prompt}}"
}`;

const fieldClass =
  "mt-2 h-10 w-full rounded-md border border-white/10 bg-black/30 px-3 text-sm text-zinc-100";
const textAreaClass =
  "mt-2 min-h-32 w-full rounded-md border border-white/10 bg-black/30 px-3 py-2 font-mono text-xs leading-5 text-zinc-100";

export default function ScannerWorkbenchPage() {
  const [engine, setEngine] = useState<"garak" | "http_tester">("garak");
  const [targetName, setTargetName] = useState("County AI endpoint");
  const [targetUrl, setTargetUrl] = useState("http://localhost:8000/chat");
  const [method, setMethod] = useState<"GET" | "POST">("POST");
  const [requestTemplate, setRequestTemplate] = useState(defaultTemplate);
  const [responsePath, setResponsePath] = useState("response");
  const [authHeaderName, setAuthHeaderName] = useState("");
  const [authHeaderValue, setAuthHeaderValue] = useState("");
  const [generations, setGenerations] = useState(1);
  const [timeoutSeconds, setTimeoutSeconds] = useState(60);
  const [selectedTests, setSelectedTests] = useState<string[]>([
    "prompt_injection",
    "jailbreak",
    "system_prompt_leakage",
  ]);
  const [runs, setRuns] = useState<ApiAssessmentToolRun[]>([]);
  const [adapters, setAdapters] = useState<ApiScannerAdapter[]>([]);
  const [selectedRun, setSelectedRun] = useState<ApiAssessmentToolRun | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadRuns() {
      const [records, adapterRecords] = await Promise.all([
        apiClient.assessmentToolRuns(),
        apiClient.scannerAdapters(),
      ]);
      setRuns(records);
      setAdapters(adapterRecords);
      setSelectedRun((current) => current ?? records[0] ?? null);
    }
    loadRuns().catch((caught) =>
      setError(caught instanceof Error ? caught.message : "Unable to load assessment runs"),
    );
  }, []);

  const visibleTestOptions = useMemo(
    () => (engine === "garak" ? testOptions.filter((option) => garakTestIds.has(option.id)) : testOptions),
    [engine],
  );

  const runLabel = useMemo(() => {
    const testLabel = selectedTests.length === 1 ? labelize(selectedTests[0]) : `${selectedTests.length} tests`;
    return engine === "garak" ? `Run garak ${testLabel}` : `Run live HTTP ${testLabel}`;
  }, [engine, selectedTests]);

  const severityCounts = useMemo(() => {
    const counts = new Map<string, number>();
    for (const finding of selectedRun?.findings ?? []) {
      counts.set(finding.severity, (counts.get(finding.severity) ?? 0) + 1);
    }
    return Array.from(counts.entries());
  }, [selectedRun]);

  function toggleTest(testId: string) {
    setSelectedTests((current) =>
      current.includes(testId)
        ? current.filter((item) => item !== testId)
        : [...current, testId],
    );
  }

  function selectEngine(nextEngine: "garak" | "http_tester") {
    setEngine(nextEngine);
    if (nextEngine === "garak") {
      setSelectedTests((current) => {
        const filtered = current.filter((testId) => garakTestIds.has(testId));
        return filtered.length ? filtered : ["prompt_injection"];
      });
    }
  }

  async function runAssessment() {
    setError(null);
    setIsRunning(true);
    try {
      const parsedTemplate = JSON.parse(requestTemplate) as Record<string, unknown>;
      const run = await apiClient.createAssessmentToolRun({
        engine,
        target_name: targetName,
        target_url: targetUrl,
        method,
        request_template: parsedTemplate,
        response_path: responsePath,
        auth_header_name: authHeaderName || null,
        auth_header_value: authHeaderValue || null,
        selected_tests: selectedTests,
        generations,
        timeout_seconds: timeoutSeconds,
      });
      setSelectedRun(run);
      const nextRuns = await apiClient.assessmentToolRuns();
      setRuns(nextRuns);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Assessment failed");
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <AppShell>
      <PageHeader
        title="Assessment Tool"
        description="Run garak or direct HTTP tests against an AI endpoint, watch the assessment process, and review real findings and report output."
        actions={<ShieldAlert className="size-6 text-cyan-100" aria-hidden="true" />}
      />

      {error ? (
        <div className="mb-4 rounded-lg border border-red-300/20 bg-red-300/10 p-3 text-sm text-red-100">
          {error}
        </div>
      ) : null}

      <div className="grid gap-6 xl:grid-cols-[380px_1fr_420px]">
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="flex items-center gap-2">
            <TerminalSquare className="size-5 text-cyan-100" aria-hidden="true" />
            <h2 className="text-base font-semibold text-zinc-50">Target and Tests</h2>
          </div>

          <div className="mt-4 grid grid-cols-2 gap-2">
            {[
              ["garak", "Garak"],
              ["http_tester", "Live HTTP Tester"],
            ].map(([value, label]) => (
              <button
                key={value}
                type="button"
                onClick={() => selectEngine(value as "garak" | "http_tester")}
                className={`h-10 rounded-md border px-3 text-sm font-medium ${
                  engine === value
                    ? "border-cyan-300/30 bg-cyan-300/10 text-cyan-50"
                    : "border-white/10 bg-black/20 text-zinc-300"
                }`}
              >
                {label}
              </button>
            ))}
          </div>

          <div className="mt-4 space-y-3">
            <label className="block">
              <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Target name</span>
              <input value={targetName} onChange={(event) => setTargetName(event.target.value)} className={fieldClass} />
            </label>
            <label className="block">
              <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Endpoint URL</span>
              <input value={targetUrl} onChange={(event) => setTargetUrl(event.target.value)} className={fieldClass} />
            </label>
            <div className="grid grid-cols-2 gap-3">
              <label className="block">
                <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">HTTP method</span>
                <select value={method} onChange={(event) => setMethod(event.target.value as "GET" | "POST")} className={fieldClass}>
                  <option value="POST">POST</option>
                  <option value="GET">GET</option>
                </select>
              </label>
              <label className="block">
                <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Response path</span>
                <input value={responsePath} onChange={(event) => setResponsePath(event.target.value)} className={fieldClass} />
              </label>
            </div>
            <label className="block">
              <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">JSON request template</span>
              <textarea value={requestTemplate} onChange={(event) => setRequestTemplate(event.target.value)} className={textAreaClass} />
            </label>
            <div className="grid grid-cols-2 gap-3">
              <label className="block">
                <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Auth header</span>
                <input placeholder="Authorization" value={authHeaderName} onChange={(event) => setAuthHeaderName(event.target.value)} className={fieldClass} />
              </label>
              <label className="block">
                <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Header value</span>
                <input type="password" value={authHeaderValue} onChange={(event) => setAuthHeaderValue(event.target.value)} className={fieldClass} />
              </label>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <label className="block">
                <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Generations</span>
                <input type="number" min={1} max={5} value={generations} onChange={(event) => setGenerations(Number(event.target.value))} className={fieldClass} />
              </label>
              <label className="block">
                <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Timeout seconds</span>
                <input type="number" min={5} max={300} value={timeoutSeconds} onChange={(event) => setTimeoutSeconds(Number(event.target.value))} className={fieldClass} />
              </label>
            </div>
          </div>

          <div className="mt-5">
            <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Test suites</p>
            <div className="mt-2 grid gap-2">
              {visibleTestOptions.map((option) => (
                <label key={option.id} className="flex items-center gap-2 rounded-md border border-white/10 bg-black/20 px-3 py-2 text-sm text-zinc-300">
                  <input type="checkbox" checked={selectedTests.includes(option.id)} onChange={() => toggleTest(option.id)} />
                  {option.label}
                </label>
              ))}
            </div>
          </div>

          <button
            type="button"
            onClick={runAssessment}
            disabled={isRunning || !targetUrl || !selectedTests.length}
            className="mt-5 inline-flex h-11 w-full items-center justify-center gap-2 rounded-md border border-cyan-300/25 bg-cyan-300/10 px-4 text-sm font-semibold text-cyan-50 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isRunning ? <RefreshCw className="size-4 animate-spin" /> : <Play className="size-4" />}
            {isRunning ? "Running assessment" : runLabel}
          </button>
        </section>

        <main className="space-y-6">
          <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
            <div className="flex items-center justify-between gap-3">
              <div>
                <h2 className="text-base font-semibold text-zinc-50">Execution Process</h2>
                <p className="mt-1 text-sm text-zinc-500">
                  {selectedRun ? `${labelize(selectedRun.engine)} run ${selectedRun.id.slice(0, 8)}` : "No assessment run selected"}
                </p>
              </div>
              {selectedRun ? <StatusPill value={selectedRun.status} /> : null}
            </div>
            <div className="mt-4 space-y-3">
              {(selectedRun?.steps ?? []).map((step, index) => (
                <div key={`${step.label}-${index}`} className="flex gap-3 rounded-md border border-white/10 bg-black/20 p-3">
                  <span className={`mt-0.5 grid size-6 shrink-0 place-items-center rounded-md border text-xs ${statusTone(step.status ?? "pending")}`}>
                    {step.status === "completed" ? <CheckCircle2 className="size-4" /> : index + 1}
                  </span>
                  <div>
                    <p className="font-medium text-zinc-100">{step.label}</p>
                    <p className="mt-1 text-sm text-zinc-500">{step.detail}</p>
                  </div>
                </div>
              ))}
              {!selectedRun?.steps?.length ? (
                <p className="rounded-md border border-white/10 bg-black/20 p-3 text-sm text-zinc-500">
                  Configure a target and run an assessment to see validation, probe execution, parsing, findings, and report generation.
                </p>
              ) : null}
            </div>
          </section>

          <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
            <div className="flex items-center gap-2">
              <AlertTriangle className="size-5 text-amber-100" aria-hidden="true" />
              <h2 className="text-base font-semibold text-zinc-50">Findings</h2>
            </div>
            <div className="mt-4 flex flex-wrap gap-2">
              {severityCounts.map(([severity, count]) => (
                <span key={severity} className={`rounded-md border px-2 py-1 text-xs ${statusTone(severity)}`}>
                  {count} {labelize(severity)}
                </span>
              ))}
              {!severityCounts.length ? <span className="text-sm text-zinc-500">No findings yet.</span> : null}
            </div>
            <div className="mt-4 space-y-3">
              {(selectedRun?.findings ?? []).map((finding) => (
                <article key={finding.id} className="rounded-lg border border-white/10 bg-black/20 p-4">
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <p className="font-medium text-zinc-100">{finding.title}</p>
                      <p className="mt-1 text-sm text-zinc-500">{labelize(finding.test)}</p>
                    </div>
                    <StatusPill value={finding.severity} />
                  </div>
                  <p className="mt-3 text-sm leading-6 text-zinc-300">{finding.rationale}</p>
                  <div className="mt-3 grid gap-3 lg:grid-cols-2">
                    <EvidenceBlock label="Failed prompt or probe" value={finding.prompt} />
                    <EvidenceBlock label="Response excerpt" value={finding.response_excerpt} />
                  </div>
                  <p className="mt-3 text-sm text-zinc-400">{finding.remediation}</p>
                </article>
              ))}
            </div>
          </section>
        </main>

        <aside className="space-y-6">
          <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
            <div className="flex items-center gap-2">
              <FileJson className="size-5 text-cyan-100" aria-hidden="true" />
              <h2 className="text-base font-semibold text-zinc-50">Report</h2>
            </div>
            {selectedRun ? (
              <div className="mt-4 space-y-3">
                <Info label="Target" value={selectedRun.target_url} />
                <Info label="Completed" value={formatDate(selectedRun.completed_at)} />
                <Info label="Findings" value={`${selectedRun.findings.length}`} />
                <div className="rounded-md border border-white/10 bg-black/20 p-3">
                  <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Artifacts</p>
                  <div className="mt-2 space-y-1">
                    {Object.entries(selectedRun.artifacts).map(([key, value]) => (
                      <p key={key} className="break-all font-mono text-xs text-zinc-400">
                        {labelize(key)}: {String(value)}
                      </p>
                    ))}
                    {!Object.keys(selectedRun.artifacts).length ? (
                      <p className="text-sm text-zinc-500">No artifacts yet.</p>
                    ) : null}
                  </div>
                </div>
                <div className="rounded-md border border-white/10 bg-black/20 p-3">
                  <p className="flex items-center gap-2 text-xs uppercase tracking-[0.08em] text-zinc-500">
                    <Braces className="size-4" aria-hidden="true" />
                    Raw report JSON
                  </p>
                  <pre className="mt-3 max-h-[420px] overflow-auto whitespace-pre-wrap rounded-md bg-black/30 p-3 text-xs leading-5 text-zinc-300">
                    {JSON.stringify(selectedRun.report, null, 2)}
                  </pre>
                </div>
              </div>
            ) : (
              <p className="mt-4 text-sm text-zinc-500">Run an assessment to generate a report.</p>
            )}
          </section>

          <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
            <h2 className="text-base font-semibold text-zinc-50">Recent Runs</h2>
            <div className="mt-3 space-y-2">
              {runs.slice(0, 6).map((run) => (
                <button
                  key={run.id}
                  type="button"
                  onClick={() => setSelectedRun(run)}
                  className={`w-full rounded-md border p-3 text-left ${
                    selectedRun?.id === run.id ? "border-cyan-300/25 bg-cyan-300/10" : "border-white/10 bg-black/20"
                  }`}
                >
                  <div className="flex items-center justify-between gap-3">
                    <span className="text-sm font-medium text-zinc-100">{run.target_name}</span>
                    <StatusPill value={run.status} />
                  </div>
                  <p className="mt-2 text-xs text-zinc-500">
                    {labelize(run.engine)} / {run.findings.length} findings / {formatDate(run.created_at)}
                  </p>
                </button>
              ))}
              {!runs.length ? <p className="text-sm text-zinc-500">No assessments executed.</p> : null}
            </div>
          </section>

          <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
            <h2 className="text-base font-semibold text-zinc-50">Scanner Capabilities</h2>
            <div className="mt-3 space-y-2">
              {adapters.map((adapter) => (
                <div key={adapter.adapter_name} className="rounded-md border border-white/10 bg-black/20 p-3">
                  <div className="flex items-center justify-between gap-3">
                    <p className="font-medium text-zinc-100">{labelize(adapter.scanner_name)}</p>
                    <StatusPill value={adapter.supported_execution_modes[0] ?? "python"} />
                  </div>
                  <p className="mt-2 text-xs text-zinc-500">{adapter.scanner_version}</p>
                  <p className="mt-2 text-sm leading-5 text-zinc-400">
                    {adapter.supported_scan_types.map(labelize).join(", ")}
                  </p>
                </div>
              ))}
            </div>
          </section>
        </aside>
      </div>
    </AppShell>
  );
}

function Info({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-white/10 bg-black/20 p-3">
      <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">{label}</p>
      <p className="mt-2 break-all text-sm text-zinc-200">{value}</p>
    </div>
  );
}

function EvidenceBlock({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-white/10 bg-black/30 p-3">
      <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">{label}</p>
      <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-zinc-300">{value || "No evidence captured."}</p>
    </div>
  );
}
