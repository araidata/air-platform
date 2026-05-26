"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { ArrowRight, CircleAlert, FileCheck2, Radar, ShieldAlert } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { MetricCard } from "@/components/metric-card";
import { PageHeader } from "@/components/page-header";
import { type ApiEvidence, type ApiFinding, type ApiScannerRun, type ApiScore, type ApiSystem, apiClient } from "@/lib/api-client";
import { labelize, StatusPill } from "@/lib/format";

export default function ExecutiveDashboard() {
  const [systems, setSystems] = useState<ApiSystem[]>([]);
  const [findings, setFindings] = useState<ApiFinding[]>([]);
  const [evidence, setEvidence] = useState<ApiEvidence[]>([]);
  const [scores, setScores] = useState<ApiScore[]>([]);
  const [runs, setRuns] = useState<ApiScannerRun[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      const [systemRecords, findingRecords, evidenceRecords, scoreRecords, runRecords] = await Promise.all([
        apiClient.systems(),
        apiClient.findings(),
        apiClient.evidence(),
        apiClient.scores(),
        apiClient.scannerRuns(),
      ]);
      setSystems(systemRecords);
      setFindings(findingRecords);
      setEvidence(evidenceRecords);
      setScores(scoreRecords);
      setRuns(runRecords);
    }
    loadData().catch((caught) => setError(caught instanceof Error ? caught.message : "Unable to load dashboard"));
  }, []);

  const openFindings = findings.filter((finding) => !["closed", "false_positive"].includes(finding.status));
  const completedRuns = runs.filter((run) => run.execution_status === "completed");
  const failedRuns = runs.filter((run) => run.execution_status === "failed");
  const overallScores = scores.filter((score) => score.score_domain === "overall_governance");
  const averageScore = overallScores.length
    ? Math.round(overallScores.reduce((sum, score) => sum + score.score_value, 0) / overallScores.length)
    : null;
  const systemsById = useMemo(() => new Map(systems.map((system) => [system.id, system])), [systems]);
  const highRiskSystems = systems.filter((system) => ["critical", "high"].includes(system.risk_tier));

  return (
    <AppShell>
      <PageHeader
        title="Executive Dashboard"
        description="Countywide operating view from real inventory, scanner runs, findings, evidence, and scores."
      />

      {error ? (
        <div className="mb-4 rounded-lg border border-red-300/20 bg-red-300/10 p-3 text-sm text-red-100">{error}</div>
      ) : null}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <MetricCard label="Governance score" value={averageScore ?? "No scores"} detail={averageScore === null ? "No real score calculation available" : "Average current overall score"} tone="neutral" />
        <MetricCard label="Open findings" value={openFindings.length} detail={openFindings.length ? "Active real findings" : "No findings generated"} tone={openFindings.length ? "warn" : "good"} />
        <MetricCard label="Scanner runs" value={runs.length} detail={runs.length ? `${completedRuns.length} completed / ${failedRuns.length} failed` : "No scanner runs available"} tone="neutral" />
        <MetricCard label="Evidence records" value={evidence.length} detail={evidence.length ? "Collected evidence records" : "No evidence collected"} tone="neutral" />
        <MetricCard label="AI systems" value={systems.length} detail="Inventory records" tone="neutral" />
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="mb-4 flex items-center gap-2">
            <ShieldAlert className="size-5 text-amber-100" aria-hidden="true" />
            <h2 className="text-base font-semibold text-zinc-50">High-Risk Systems</h2>
          </div>
          <div className="space-y-3">
            {highRiskSystems.map((system) => (
              <Link key={system.id} href={`/systems/${system.id}`} className="block rounded-lg border border-white/10 bg-black/20 p-3 transition-colors hover:border-cyan-300/25 hover:bg-cyan-300/5">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="font-medium text-zinc-100">{system.system_name}</p>
                    <p className="mt-1 text-sm text-zinc-500">{system.department_owner}</p>
                  </div>
                  <StatusPill value={system.risk_tier} />
                </div>
                <div className="mt-3 flex flex-wrap gap-2">
                  <StatusPill value={system.approval_status} />
                  <StatusPill value={system.assessment_method} />
                </div>
              </Link>
            ))}
            {!highRiskSystems.length ? <EmptyState text="No high-risk systems in inventory." /> : null}
          </div>
        </section>

        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="mb-4 flex items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <CircleAlert className="size-5 text-amber-100" aria-hidden="true" />
              <h2 className="text-base font-semibold text-zinc-50">Findings Needing Action</h2>
            </div>
            <Link href="/findings" className="inline-flex items-center gap-1 text-sm font-medium text-cyan-100 hover:text-cyan-50">
              Queue <ArrowRight className="size-4" aria-hidden="true" />
            </Link>
          </div>
          <div className="divide-y divide-white/10">
            {openFindings.slice(0, 5).map((finding) => (
              <div key={finding.id} className="grid gap-3 py-3 md:grid-cols-[1fr_auto]">
                <div>
                  <p className="font-medium text-zinc-100">{finding.title}</p>
                  <p className="mt-1 text-sm text-zinc-500">
                    {finding.id.slice(0, 8)} / {systemsById.get(finding.system_id)?.system_name ?? "Unknown system"}
                  </p>
                </div>
                <div className="flex flex-wrap items-center gap-2 md:justify-end">
                  <StatusPill value={finding.severity} />
                  <StatusPill value={finding.status} />
                </div>
              </div>
            ))}
            {!openFindings.length ? <EmptyState text="No findings generated." /> : null}
          </div>
        </section>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="flex items-center gap-2">
            <Radar className="size-5 text-cyan-100" aria-hidden="true" />
            <h2 className="text-base font-semibold text-zinc-50">Scanner Run Status</h2>
          </div>
          <div className="mt-4 space-y-3">
            {runs.slice(0, 6).map((run) => (
              <div key={run.id} className="rounded-lg border border-white/10 bg-black/20 p-3">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="font-medium text-zinc-100">{labelize(run.scanner_name)}</p>
                    <p className="mt-1 font-mono text-xs text-zinc-500">{run.id.slice(0, 8)}</p>
                  </div>
                  <StatusPill value={run.execution_status} />
                </div>
                <p className="mt-2 text-sm text-zinc-500">{run.finding_count} findings generated from this run</p>
              </div>
            ))}
            {!runs.length ? <EmptyState text="No scanner runs available." /> : null}
          </div>
        </section>

        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="flex items-center gap-2">
            <FileCheck2 className="size-5 text-cyan-100" aria-hidden="true" />
            <h2 className="text-base font-semibold text-zinc-50">Evidence Collection</h2>
          </div>
          <div className="mt-4">
            {evidence.length ? (
              <div className="grid gap-3 sm:grid-cols-2">
                {evidence.slice(0, 4).map((record) => (
                  <Link key={record.id} href="/evidence" className="rounded-lg border border-white/10 bg-black/20 p-3 hover:border-cyan-300/20">
                    <p className="font-medium text-zinc-100">{record.title}</p>
                    <p className="mt-1 text-sm text-zinc-500">{labelize(record.evidence_type)}</p>
                  </Link>
                ))}
              </div>
            ) : (
              <EmptyState text="No evidence collected." />
            )}
          </div>
        </section>
      </div>
    </AppShell>
  );
}

function EmptyState({ text }: { text: string }) {
  return <p className="rounded-lg border border-white/10 bg-black/20 p-4 text-sm text-zinc-500">{text}</p>;
}
