"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { CheckCircle2, ClipboardCheck, RefreshCw, ShieldAlert } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { TableHead, TableShell, Td, Th } from "@/components/data-table";
import { FilterBar } from "@/components/filter-bar";
import { MetricCard } from "@/components/metric-card";
import { PageHeader } from "@/components/page-header";
import {
  type ApiEvidence,
  type ApiFinding,
  type ApiOwner,
  type ApiScore,
  type ApiSystem,
  apiClient,
} from "@/lib/api-client";
import { formatDate, labelize, StatusPill } from "@/lib/format";

const transitionsByStatus: Record<string, { label: string; status: string }[]> = {
  new: [{ label: "Move to under review", status: "under_review" }],
  under_review: [
    { label: "Move to remediation", status: "in_remediation" },
    { label: "Accept risk", status: "risk_accepted" },
    { label: "Mark false positive", status: "false_positive" },
  ],
  in_remediation: [{ label: "Request retest", status: "awaiting_retest" }],
  awaiting_retest: [
    { label: "Mark mitigated", status: "mitigated" },
    { label: "Return to remediation", status: "in_remediation" },
  ],
  mitigated: [{ label: "Close", status: "closed" }],
  risk_accepted: [{ label: "Close", status: "closed" }],
  false_positive: [{ label: "Close", status: "closed" }],
};

const fieldClass =
  "mt-2 h-10 w-full rounded-md border border-white/10 bg-black/30 px-3 text-sm text-zinc-100";
const textAreaClass =
  "mt-2 min-h-24 w-full rounded-md border border-white/10 bg-black/30 px-3 py-2 text-sm text-zinc-100";

export default function FindingsPage() {
  const [systems, setSystems] = useState<ApiSystem[]>([]);
  const [findings, setFindings] = useState<ApiFinding[]>([]);
  const [evidence, setEvidence] = useState<ApiEvidence[]>([]);
  const [owners, setOwners] = useState<ApiOwner[]>([]);
  const [scores, setScores] = useState<ApiScore[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [ownerId, setOwnerId] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [remediation, setRemediation] = useState("");
  const [notes, setNotes] = useState("");
  const [activeFilter, setActiveFilter] = useState("Open findings");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function loadData() {
    const [systemRecords, findingRecords, evidenceRecords, ownerRecords, scoreRecords] =
      await Promise.all([
        apiClient.systems(),
        apiClient.findings(),
        apiClient.evidence(),
        apiClient.owners(),
        apiClient.scores(),
      ]);
    setSystems(systemRecords);
    setFindings(findingRecords);
    setEvidence(evidenceRecords);
    setOwners(ownerRecords);
    setScores(scoreRecords);
    setSelectedId((current) => current ?? findingRecords[0]?.id ?? null);
  }

  useEffect(() => {
    async function loadInitialData() {
      try {
        await loadData();
      } catch (caught) {
        setError(caught instanceof Error ? caught.message : "Unable to load findings");
      }
    }
    void loadInitialData();
  }, []);

  const selectedFinding = findings.find((finding) => finding.id === selectedId) ?? null;

  useEffect(() => {
    // The detail form mirrors whichever finding the operator selects.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setOwnerId(selectedFinding?.owner_id ?? "");
    setDueDate(selectedFinding?.due_date ?? "");
    setRemediation(selectedFinding?.remediation ?? "");
    setNotes("");
  }, [selectedFinding]);

  const systemById = useMemo(
    () => new Map(systems.map((system) => [system.id, system])),
    [systems],
  );
  const ownerById = useMemo(() => new Map(owners.map((owner) => [owner.id, owner])), [owners]);
  const visibleFindings = useMemo(() => {
    return findings.filter((finding) => {
      if (activeFilter === "Open findings") return !["closed", "false_positive"].includes(finding.status);
      if (activeFilter === "Critical") return finding.severity === "critical";
      if (activeFilter === "Retest required") return finding.status === "awaiting_retest";
      if (activeFilter === "Civil rights") return finding.domain === "bias_civil_rights";
      if (activeFilter === "Security") return finding.domain === "security";
      if (activeFilter === "Risk accepted") return finding.risk_accepted;
      return true;
    });
  }, [activeFilter, findings]);
  const selectedEvidence = selectedFinding
    ? evidence.filter((record) => record.finding_id === selectedFinding.id)
    : [];
  const selectedScores = selectedFinding
    ? scores.filter((score) => score.system_id === selectedFinding.system_id)
    : [];
  const negativeScoreDrivers = selectedScores.flatMap((score) => score.explanations ?? []);
  const scoreImpact =
    selectedFinding && Object.keys(selectedFinding.score_impact).length
      ? Object.entries(selectedFinding.score_impact)
          .map(([key, value]) => `${labelize(key)} ${String(value)}`)
          .join(", ")
      : negativeScoreDrivers.length
        ? `${negativeScoreDrivers.length} score explanations`
        : "Calculated";

  async function saveTriage() {
    if (!selectedFinding) return;
    setError(null);
    try {
      const updated = await apiClient.updateFinding(selectedFinding.id, {
        owner_id: ownerId || null,
        due_date: dueDate || null,
        remediation,
        actor: "frontend-operator",
        notes: notes || "Finding triage updated from UI",
      });
      setMessage(`Updated ${updated.title}`);
      await loadData();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to update finding");
    }
  }

  async function transition(status: string) {
    if (!selectedFinding) return;
    setError(null);
    try {
      const updated = await apiClient.transitionFinding(selectedFinding.id, {
        status,
        actor: "frontend-operator",
        notes: notes || `Moved to ${labelize(status)} from UI`,
        risk_acceptance_rationale:
          status === "risk_accepted" ? notes || "Risk accepted by operator from findings queue." : undefined,
      });
      setMessage(`${updated.title} moved to ${labelize(updated.status)}`);
      await loadData();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to transition finding");
    }
  }

  async function requestRetest() {
    if (!selectedFinding) return;
    setError(null);
    try {
      await apiClient.createRetest(selectedFinding.id, {
        initiated_by: "frontend-operator",
        status: "pending",
        notes: notes || "Retest requested from findings queue.",
      });
      if (selectedFinding.status === "in_remediation") {
        await apiClient.transitionFinding(selectedFinding.id, {
          status: "awaiting_retest",
          actor: "frontend-operator",
          notes: "Retest requested from UI",
        });
      }
      setMessage("Retest initiated");
      await loadData();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to initiate retest");
    }
  }

  return (
    <AppShell>
      <PageHeader
        title="Findings Queue"
        description="Triage findings, assign owners, manage due dates, record remediation, request retests, accept risk, and close work."
      />

      {error ? (
        <div className="mb-4 rounded-lg border border-red-300/20 bg-red-300/10 p-3 text-sm text-red-100">
          {error}
        </div>
      ) : null}
      {message ? (
        <div className="mb-4 rounded-lg border border-emerald-300/20 bg-emerald-300/10 p-3 text-sm text-emerald-100">
          {message}
        </div>
      ) : null}

      <FilterBar
        items={[
          "Open findings",
          "Critical",
          "Retest required",
          "Civil rights",
          "Security",
          "Risk accepted",
          "All findings",
        ]}
        activeItem={activeFilter}
        onChange={setActiveFilter}
      />

      <div className="mb-6 grid gap-4 md:grid-cols-4">
        <MetricCard
          label="Open findings"
          value={findings.filter((finding) => !["closed", "false_positive"].includes(finding.status)).length}
          detail="Active queue items"
          tone="warn"
          badgeLabel="Triage"
        />
        <MetricCard
          label="Approval blocking"
          value={findings.filter((finding) => finding.approval_blocking).length}
          detail="Findings that can block governance approval"
          tone="bad"
          badgeLabel="AIRB"
        />
        <MetricCard
          label="Retest requested"
          value={findings.filter((finding) => finding.status === "awaiting_retest").length}
          detail="Findings waiting on validation"
          tone="neutral"
          badgeLabel="Retest"
        />
        <MetricCard
          label="Evidence-linked"
          value={findings.filter((finding) => evidence.some((record) => record.finding_id === finding.id)).length}
          detail="Findings with support records"
          tone="good"
          badgeLabel="Evidence"
        />
      </div>

      <div className="grid gap-6 xl:grid-cols-[1fr_420px]">
        <TableShell label="Findings triage queue">
          <TableHead>
            <tr>
              <Th>Finding</Th>
              <Th>System</Th>
              <Th>Severity</Th>
              <Th>Status</Th>
              <Th>Owner</Th>
              <Th>Due</Th>
              <Th>Evidence</Th>
            </tr>
          </TableHead>
          <tbody className="divide-y divide-white/10">
            {visibleFindings.map((finding) => (
              <tr
                key={finding.id}
                onClick={() => setSelectedId(finding.id)}
                className={`cursor-pointer hover:bg-white/[0.035] ${
                  selectedId === finding.id ? "bg-cyan-300/[0.04]" : ""
                }`}
              >
                <Td>
                  <div className="min-w-80">
                    <p className="font-mono text-xs text-zinc-500">{finding.id.slice(0, 8)}</p>
                    <p className="mt-1 font-medium text-zinc-50">{finding.title}</p>
                    <p className="mt-1 text-sm leading-5 text-zinc-500">{finding.evidence_summary}</p>
                  </div>
                </Td>
                <Td>
                  <Link
                    href={`/systems/${finding.system_id}`}
                    className="font-medium text-cyan-100 hover:text-cyan-50"
                  >
                    {systemById.get(finding.system_id)?.system_name ?? "Unknown system"}
                  </Link>
                </Td>
                <Td>
                  <StatusPill value={finding.severity} />
                </Td>
                <Td>
                  <StatusPill value={finding.status} />
                </Td>
                <Td>{finding.owner_id ? ownerById.get(finding.owner_id)?.display_name ?? "Assigned" : "Unassigned"}</Td>
                <Td>{formatDate(finding.due_date)}</Td>
                <Td>{evidence.filter((record) => record.finding_id === finding.id).length}</Td>
              </tr>
            ))}
            {!visibleFindings.length ? (
              <tr>
                <td colSpan={7} className="px-4 py-3">
                  <p className="py-6 text-center text-sm text-zinc-500">No findings generated.</p>
                </td>
              </tr>
            ) : null}
          </tbody>
        </TableShell>

        <aside className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="flex items-center gap-2">
            <ShieldAlert className="size-5 text-amber-100" aria-hidden="true" />
            <h2 className="text-base font-semibold text-zinc-50">Finding Detail</h2>
          </div>
          {selectedFinding ? (
            <div className="mt-4 space-y-4">
              <div>
                <p className="font-medium text-zinc-100">{selectedFinding.title}</p>
                <p className="mt-2 text-sm leading-6 text-zinc-400">{selectedFinding.description}</p>
              </div>
              <div className="flex flex-wrap gap-2">
                <StatusPill value={selectedFinding.severity} />
                <StatusPill value={selectedFinding.domain} />
                <StatusPill value={selectedFinding.status} />
                {selectedFinding.risk_accepted ? <StatusPill value="risk_accepted" /> : null}
                {selectedFinding.approval_blocking ? <StatusPill value="approval_blocking" /> : null}
              </div>
              <div className="grid gap-3 sm:grid-cols-2">
                <label>
                  <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Owner</span>
                  <select value={ownerId} onChange={(event) => setOwnerId(event.target.value)} className={fieldClass}>
                    <option value="">Unassigned</option>
                    {owners.map((owner) => (
                      <option key={owner.id} value={owner.id}>
                        {owner.display_name}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Due date</span>
                  <input
                    type="date"
                    value={dueDate}
                    onChange={(event) => setDueDate(event.target.value)}
                    className={fieldClass}
                  />
                </label>
              </div>
              <label className="block">
                <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Remediation notes</span>
                <textarea
                  value={remediation}
                  onChange={(event) => setRemediation(event.target.value)}
                  className={textAreaClass}
                />
              </label>
              <label className="block">
                <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Decision notes</span>
                <textarea value={notes} onChange={(event) => setNotes(event.target.value)} className={textAreaClass} />
              </label>
              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  onClick={saveTriage}
                  className="inline-flex h-10 items-center gap-2 rounded-md border border-cyan-300/25 bg-cyan-300/10 px-3 text-sm font-medium text-cyan-50"
                >
                  <ClipboardCheck className="size-4" aria-hidden="true" />
                  Save triage
                </button>
                <button
                  type="button"
                  onClick={requestRetest}
                  className="inline-flex h-10 items-center gap-2 rounded-md border border-amber-300/20 px-3 text-sm font-medium text-amber-100"
                >
                  <RefreshCw className="size-4" aria-hidden="true" />
                  Initiate retest
                </button>
                {(transitionsByStatus[selectedFinding.status] ?? []).map((action) => (
                  <button
                    key={action.status}
                    type="button"
                    onClick={() => transition(action.status)}
                    className="inline-flex h-10 items-center gap-2 rounded-md border border-white/10 px-3 text-sm font-medium text-zinc-100"
                  >
                    <CheckCircle2 className="size-4" aria-hidden="true" />
                    {action.label}
                  </button>
                ))}
              </div>
              <div className="rounded-lg border border-white/10 bg-black/20 p-3">
                <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Score impact</p>
                <p className="mt-2 text-sm text-zinc-300">{scoreImpact}</p>
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Linked evidence</p>
                <div className="mt-2 space-y-2">
                  {selectedEvidence.map((record) => (
                    <Link
                      key={record.id}
                      href="/evidence"
                      className="block rounded-md border border-white/10 bg-black/20 p-3 hover:border-cyan-300/20"
                    >
                      <p className="font-medium text-zinc-100">{record.title}</p>
                      <p className="mt-1 text-sm text-zinc-500">{labelize(record.evidence_type)}</p>
                      {record.metadata_json?.trace_id ? (
                        <p className="mt-1 font-mono text-xs text-zinc-500">
                          Trace {String(record.metadata_json.trace_id).slice(0, 8)}
                        </p>
                      ) : null}
                    </Link>
                  ))}
                  {!selectedEvidence.length ? (
                    <p className="text-sm text-zinc-500">No linked evidence records.</p>
                  ) : null}
                </div>
              </div>
            </div>
          ) : (
            <p className="mt-4 text-sm text-zinc-500">No finding selected. No findings generated.</p>
          )}
        </aside>
      </div>
    </AppShell>
  );
}
