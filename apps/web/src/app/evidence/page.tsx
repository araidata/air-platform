"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { FileJson, Link2, ScrollText } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { TableHead, TableShell, Td, Th } from "@/components/data-table";
import { FilterBar } from "@/components/filter-bar";
import { MetricCard } from "@/components/metric-card";
import { PageHeader } from "@/components/page-header";
import {
  type ApiAssessment,
  type ApiEvidence,
  type ApiFinding,
  type ApiScannerRun,
  type ApiSystem,
  apiClient,
} from "@/lib/api-client";
import { formatDate, StatusPill } from "@/lib/format";

export default function EvidencePage() {
  const [systems, setSystems] = useState<ApiSystem[]>([]);
  const [assessments, setAssessments] = useState<ApiAssessment[]>([]);
  const [findings, setFindings] = useState<ApiFinding[]>([]);
  const [evidence, setEvidence] = useState<ApiEvidence[]>([]);
  const [runs, setRuns] = useState<ApiScannerRun[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [activeFilter, setActiveFilter] = useState("All evidence");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      const [systemRecords, assessmentRecords, findingRecords, evidenceRecords, runRecords] =
        await Promise.all([
          apiClient.systems(),
          apiClient.assessments(),
          apiClient.findings(),
          apiClient.evidence(),
          apiClient.scannerRuns(),
        ]);
      setSystems(systemRecords);
      setAssessments(assessmentRecords);
      setFindings(findingRecords);
      setEvidence(evidenceRecords);
      setRuns(runRecords);
      setSelectedId((current) => current ?? evidenceRecords[0]?.id ?? null);
    }
    loadData().catch((caught) =>
      setError(caught instanceof Error ? caught.message : "Unable to load evidence"),
    );
  }, []);

  const systemById = useMemo(
    () => new Map(systems.map((system) => [system.id, system])),
    [systems],
  );
  const assessmentById = useMemo(
    () => new Map(assessments.map((assessment) => [assessment.id, assessment])),
    [assessments],
  );
  const findingById = useMemo(
    () => new Map(findings.map((finding) => [finding.id, finding])),
    [findings],
  );
  const runById = useMemo(() => new Map(runs.map((run) => [run.id, run])), [runs]);
  const selected = evidence.find((record) => record.id === selectedId) ?? null;
  const visibleEvidence = evidence.filter((record) => {
    if (activeFilter === "Scanner output") return record.evidence_type === "scanner_output";
    if (activeFilter === "Raw logs") return record.evidence_type === "raw_log";
    if (activeFilter === "Prompt/output") return ["prompt", "model_response"].includes(record.evidence_type);
    if (activeFilter === "Civil rights") {
      return [
        "bilingual_screenshot",
        "translated_response",
        "accessibility_evidence",
        "fairness_review_note",
        "appeal_process_documentation",
      ].includes(record.evidence_type);
    }
    if (activeFilter === "Linked findings") return Boolean(record.finding_id);
    return true;
  });
  const scannerRunId = selected?.metadata_json?.scanner_run_id;
  const selectedRun = typeof scannerRunId === "string" ? runById.get(scannerRunId) : undefined;

  return (
    <AppShell>
      <PageHeader
        title="Evidence & Audit"
        description="Review raw, normalized, operator-provided, and scanner-generated evidence with linked systems, assessments, findings, and scanner runs."
      />

      {error ? (
        <div className="mb-4 rounded-lg border border-red-300/20 bg-red-300/10 p-3 text-sm text-red-100">
          {error}
        </div>
      ) : null}

      <div className="mb-6 grid gap-4 md:grid-cols-4">
        <MetricCard label="Evidence records" value={evidence.length} detail="Preserved support records" />
        <MetricCard
          label="Scanner generated"
          value={evidence.filter((record) => record.metadata_json?.scanner_run_id).length}
          detail="Records linked to scanner runs"
          tone="good"
          badgeLabel="Scanner"
        />
        <MetricCard
          label="Linked findings"
          value={evidence.filter((record) => record.finding_id).length}
          detail="Evidence supporting normalized findings"
          tone="neutral"
          badgeLabel="Findings"
        />
        <MetricCard
          label="Civil-rights evidence"
          value={
            evidence.filter((record) =>
              ["accessibility_evidence", "fairness_review_note", "translated_response"].includes(record.evidence_type),
            ).length
          }
          detail="Fairness, access, and appeal evidence"
          tone="warn"
          badgeLabel="Review"
        />
      </div>

      <FilterBar
        items={["All evidence", "Scanner output", "Raw logs", "Prompt/output", "Civil rights", "Linked findings"]}
        activeItem={activeFilter}
        onChange={setActiveFilter}
      />

      <div className="grid gap-6 xl:grid-cols-[1fr_420px]">
        <TableShell label="Evidence library">
          <TableHead>
            <tr>
              <Th>Evidence</Th>
              <Th>System</Th>
              <Th>Type</Th>
              <Th>Source</Th>
              <Th>Collected</Th>
              <Th>Links</Th>
            </tr>
          </TableHead>
          <tbody className="divide-y divide-white/10">
            {visibleEvidence.map((record) => (
              <tr
                key={record.id}
                onClick={() => setSelectedId(record.id)}
                className={`cursor-pointer hover:bg-white/[0.035] ${
                  selectedId === record.id ? "bg-cyan-300/[0.04]" : ""
                }`}
              >
                <Td>
                  <div className="min-w-80">
                    <p className="font-mono text-xs text-zinc-500">{record.id.slice(0, 8)}</p>
                    <p className="mt-1 font-medium text-zinc-50">{record.title}</p>
                    <p className="mt-1 text-sm leading-5 text-zinc-500">
                      {record.description ?? record.raw_text?.slice(0, 120) ?? "No summary recorded"}
                    </p>
                  </div>
                </Td>
                <Td>
                  {record.system_id ? (
                    <Link href={`/systems/${record.system_id}`} className="font-medium text-cyan-100">
                      {systemById.get(record.system_id)?.system_name ?? "Unknown system"}
                    </Link>
                  ) : (
                    "Not linked"
                  )}
                </Td>
                <Td>
                  <StatusPill value={record.evidence_type} />
                </Td>
                <Td>{record.created_by}</Td>
                <Td>{formatDate(record.created_at)}</Td>
                <Td>
                  <span className="font-mono text-sm text-zinc-300">
                    {[record.finding_id, record.assessment_id, record.metadata_json?.scanner_run_id].filter(Boolean).length}
                  </span>
                </Td>
              </tr>
            ))}
            {!visibleEvidence.length ? (
              <tr>
                <td colSpan={6} className="px-4 py-3">
                  <p className="py-6 text-center text-sm text-zinc-500">No evidence collected.</p>
                </td>
              </tr>
            ) : null}
          </tbody>
        </TableShell>

        <aside className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="flex items-center gap-2">
            <ScrollText className="size-5 text-cyan-100" aria-hidden="true" />
            <h2 className="text-base font-semibold text-zinc-50">Evidence Detail</h2>
          </div>
          {selected ? (
            <div className="mt-4 space-y-4">
              <div>
                <p className="font-medium text-zinc-100">{selected.title}</p>
                <p className="mt-2 text-sm leading-6 text-zinc-400">
                  {selected.description ?? "No operator description recorded."}
                </p>
              </div>
              <div className="flex flex-wrap gap-2">
                <StatusPill value={selected.evidence_type} />
                <StatusPill value={selected.metadata_json?.scanner_run_id ? "scanner_generated" : "operator_or_workflow"} />
                {selected.raw_text ? <StatusPill value="raw_or_prompt_text" /> : null}
              </div>
              <div className="grid gap-3 sm:grid-cols-2">
                <Info label="System" value={selected.system_id ? systemById.get(selected.system_id)?.system_name : "Not linked"} />
                <Info
                  label="Assessment"
                  value={selected.assessment_id ? assessmentById.get(selected.assessment_id)?.assessment_type : "Not linked"}
                />
                <Info
                  label="Finding"
                  value={selected.finding_id ? findingById.get(selected.finding_id)?.title : "Not linked"}
                />
                <Info label="Hash" value={selected.hash ?? "Not recorded"} mono />
              </div>
              <div className="rounded-lg border border-white/10 bg-black/20 p-3">
                <div className="flex items-center gap-2">
                  <FileJson className="size-4 text-zinc-400" aria-hidden="true" />
                  <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Artifact references</p>
                </div>
                <p className="mt-2 break-all font-mono text-xs text-zinc-400">
                  {selected.file_path ?? selectedRun?.raw_output_path ?? "No file path recorded"}
                </p>
                {selectedRun?.log_path ? (
                  <p className="mt-2 break-all font-mono text-xs text-zinc-500">{selectedRun.log_path}</p>
                ) : null}
              </div>
              <div className="rounded-lg border border-white/10 bg-black/20 p-3">
                <div className="flex items-center gap-2">
                  <Link2 className="size-4 text-zinc-400" aria-hidden="true" />
                  <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Chain of evidence</p>
                </div>
                <ol className="mt-3 space-y-2 text-sm text-zinc-400">
                  <li>Created by {selected.created_by}</li>
                  {selectedRun ? <li>Generated by scanner run {selectedRun.id.slice(0, 8)}</li> : null}
                  {selected.finding_id ? <li>Supports finding {selected.finding_id.slice(0, 8)}</li> : null}
                  {selected.assessment_id ? <li>Belongs to assessment {selected.assessment_id.slice(0, 8)}</li> : null}
                </ol>
              </div>
              {selected.raw_text ? (
                <pre className="max-h-72 overflow-auto rounded-lg border border-white/10 bg-black/30 p-3 text-xs leading-5 text-zinc-300">
                  {selected.raw_text}
                </pre>
              ) : null}
            </div>
          ) : (
            <p className="mt-4 text-sm text-zinc-500">No evidence collected.</p>
          )}
        </aside>
      </div>
    </AppShell>
  );
}

function Info({
  label,
  value,
  mono = false,
}: {
  label: string;
  value: string | undefined;
  mono?: boolean;
}) {
  return (
    <div className="rounded-lg border border-white/10 bg-black/20 p-3">
      <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">{label}</p>
      <p className={`mt-2 text-sm text-zinc-100 ${mono ? "break-all font-mono text-xs" : ""}`}>
        {value ?? "Unknown"}
      </p>
    </div>
  );
}
