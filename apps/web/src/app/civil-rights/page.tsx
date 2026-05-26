"use client";

import { useEffect, useMemo, useState } from "react";
import {
  Accessibility,
  FileCheck2,
  Gavel,
  Languages,
  Scale,
  TriangleAlert,
} from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { TableHead, TableShell, Td, Th } from "@/components/data-table";
import { MetricCard } from "@/components/metric-card";
import { PageHeader } from "@/components/page-header";
import {
  type ApiCivilRightsSummary,
  type ApiScore,
  type ApiSystem,
  apiClient,
} from "@/lib/api-client";

const labelize = (value: string) =>
  value
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");

const toneForStatus = (status: string) => {
  if (["validated", "complete", "approved"].includes(status)) {
    return "border-emerald-300/20 bg-emerald-300/10 text-emerald-100";
  }
  if (["gap_found", "blocked", "needs_evidence"].includes(status)) {
    return "border-amber-300/20 bg-amber-300/10 text-amber-100";
  }
  return "border-cyan-300/20 bg-cyan-300/10 text-cyan-100";
};

export default function CivilRightsPage() {
  const [systems, setSystems] = useState<ApiSystem[]>([]);
  const [scores, setScores] = useState<ApiScore[]>([]);
  const [summary, setSummary] = useState<ApiCivilRightsSummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [systemRecords, scoreRecords, civilRightsSummary] = await Promise.all([
          apiClient.systems(),
          apiClient.scores(),
          apiClient.civilRightsSummary(),
        ]);
        setSystems(systemRecords);
        setScores(scoreRecords);
        setSummary(civilRightsSummary);
      } catch (caught) {
        setError(caught instanceof Error ? caught.message : "Unable to load civil-rights data");
      }
    }
    void loadData();
  }, []);

  const rightsImpactingSystems = systems.filter((system) => system.rights_impacting);
  const publicSystems = systems.filter((system) => system.public_facing);
  const biasScores = scores.filter((score) => score.score_domain === "bias_civil_rights");
  const averageBiasScore = biasScores.length
    ? Math.round(biasScores.reduce((sum, score) => sum + score.score_value, 0) / biasScores.length)
    : null;
  const systemById = useMemo(
    () => new Map(systems.map((system) => [system.id, system.system_name])),
    [systems],
  );
  const activeFindings = summary?.fairness_findings.filter(
    (finding) => !["closed", "false_positive"].includes(finding.status),
  ) ?? [];
  const blockingFindings = activeFindings.filter((finding) => finding.approval_blocking);

  return (
    <AppShell>
      <PageHeader
        title="Civil Rights Review"
        description="Rights-impacting templates, language-access scenarios, appeal-path validation, fairness findings, and accessibility evidence."
        actions={<Scale className="size-6 text-cyan-100" aria-hidden="true" />}
      />

      {error ? (
        <div className="mb-4 rounded-lg border border-red-300/20 bg-red-300/10 p-3 text-sm text-red-100">
          {error}
        </div>
      ) : null}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <MetricCard
          label="Rights-impacting systems"
          value={rightsImpactingSystems.length}
          detail={`${publicSystems.length} public-facing systems need language/access review`}
          tone="neutral"
          badgeLabel="Phase 6"
        />
        <MetricCard
          label="Templates"
          value={summary?.templates.length ?? 0}
          detail="Civil-rights assessment templates"
          tone="neutral"
          badgeLabel="Profiles"
        />
        <MetricCard
          label="Language scenarios"
          value={summary?.language_access_scenarios.length ?? 0}
          detail="English/Spanish scenario checks"
          tone="neutral"
          badgeLabel="Review"
        />
        <MetricCard
          label="Blocking findings"
          value={blockingFindings.length}
          detail="Approval-blocking fairness or appeal gaps"
          tone="warn"
          badgeLabel="Findings"
        />
        <MetricCard
          label="Bias score"
          value={averageBiasScore ?? "No scores"}
          detail={averageBiasScore === null ? "No real score calculation available" : "Average current Bias & Civil Rights score"}
          tone={averageBiasScore !== null && averageBiasScore >= 75 ? "good" : "neutral"}
          badgeLabel="Scoring"
        />
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="mb-4 flex items-center gap-2">
            <FileCheck2 className="size-5 text-emerald-100" aria-hidden="true" />
            <h2 className="text-base font-semibold text-zinc-50">Assessment Templates</h2>
          </div>
          <div className="space-y-3">
            {(summary?.templates ?? []).map((template) => (
              <div key={template.id} className="rounded-lg border border-white/10 bg-black/20 p-3">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="font-medium text-zinc-100">{template.profile_name}</p>
                    <p className="mt-1 text-sm leading-5 text-zinc-500">
                      {template.description}
                    </p>
                  </div>
                  <span className="rounded-md border border-white/10 px-2 py-1 text-xs text-zinc-300">
                    {template.required_scan_types.length} controls
                  </span>
                </div>
                <div className="mt-3 flex flex-wrap gap-1.5">
                  {template.required_evidence_types.slice(0, 4).map((item) => (
                    <span
                      key={item}
                      className="rounded-md border border-white/10 bg-white/[0.04] px-2 py-1 text-xs text-zinc-400"
                    >
                      {item}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="mb-4 flex items-center gap-2">
            <Languages className="size-5 text-cyan-100" aria-hidden="true" />
            <h2 className="text-base font-semibold text-zinc-50">Language Access Review</h2>
          </div>
          <div className="space-y-3">
            {(summary?.language_access_scenarios ?? []).map((scenario) => (
              <div key={scenario.id} className="rounded-lg border border-white/10 bg-black/20 p-3">
                <div className="grid gap-3 lg:grid-cols-[1fr_180px]">
                  <div>
                    <p className="font-medium text-zinc-100">{scenario.name}</p>
                    <p className="mt-1 text-sm text-zinc-500">
                      {scenario.primary_language} vs {scenario.comparison_language} - {labelize(scenario.scenario_type)}
                    </p>
                    <p className="mt-2 text-sm leading-5 text-zinc-400">
                      {scenario.expected_behavior}
                    </p>
                  </div>
                  <div className="rounded-lg border border-white/10 bg-white/[0.035] p-3">
                    <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">System</p>
                    <p className="mt-2 text-sm text-zinc-100">
                      {scenario.system_id ? systemById.get(scenario.system_id) : "Template"}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        <section>
          <TableShell label="Human appeal path checks">
            <TableHead>
              <tr>
                <Th>Check</Th>
                <Th>System</Th>
                <Th>Status</Th>
                <Th>Evidence</Th>
              </tr>
            </TableHead>
            <tbody className="divide-y divide-white/10">
              {(summary?.appeal_path_checks ?? []).map((check) => (
                <tr key={check.id} className="hover:bg-white/[0.035]">
                  <Td>
                    <p className="font-medium text-zinc-100">{labelize(check.check_type)}</p>
                    <p className="mt-1 max-w-xl text-sm leading-5 text-zinc-500">
                      {check.required_control}
                    </p>
                  </Td>
                  <Td>{systemById.get(check.system_id) ?? "Unknown system"}</Td>
                  <Td>
                    <span className={`rounded-md border px-2 py-1 text-xs ${toneForStatus(check.status)}`}>
                      {labelize(check.status)}
                    </span>
                  </Td>
                  <Td>
                    <span className="font-mono text-sm text-zinc-300">
                      {check.evidence_ids.length}/{check.evidence_requirements.length}
                    </span>
                  </Td>
                </tr>
              ))}
            </tbody>
          </TableShell>
        </section>

        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="mb-4 flex items-center gap-2">
            <Accessibility className="size-5 text-emerald-100" aria-hidden="true" />
            <h2 className="text-base font-semibold text-zinc-50">Accessibility Evidence</h2>
          </div>
          <div className="space-y-3">
            {(summary?.fairness_evidence ?? []).slice(0, 8).map((record) => (
              <div key={record.id} className="rounded-lg border border-white/10 bg-black/20 p-3">
                <p className="font-medium text-zinc-100">{record.title}</p>
                <p className="mt-1 text-sm text-zinc-500">
                  {labelize(record.evidence_type)} - {record.created_by}
                </p>
                {record.description ? (
                  <p className="mt-2 text-sm leading-5 text-zinc-400">{record.description}</p>
                ) : null}
              </div>
            ))}
            {!(summary?.fairness_evidence ?? []).length ? (
              <p className="rounded-lg border border-white/10 bg-black/20 p-4 text-sm text-zinc-500">
                No evidence collected.
              </p>
            ) : null}
          </div>
        </section>
      </div>

      <section className="mt-6">
        <TableShell label="Fairness findings">
          <TableHead>
            <tr>
              <Th>Finding</Th>
              <Th>System</Th>
              <Th>Severity</Th>
              <Th>Status</Th>
              <Th>Score impact</Th>
            </tr>
          </TableHead>
          <tbody className="divide-y divide-white/10">
            {activeFindings.map((finding) => (
              <tr key={finding.id} className="hover:bg-white/[0.035]">
                <Td>
                  <div className="min-w-80">
                    <div className="flex items-center gap-2">
                      {finding.approval_blocking ? (
                        <TriangleAlert className="size-4 text-amber-100" aria-hidden="true" />
                      ) : (
                        <Gavel className="size-4 text-zinc-500" aria-hidden="true" />
                      )}
                      <p className="font-medium text-zinc-100">{finding.title}</p>
                    </div>
                    <p className="mt-1 text-sm leading-5 text-zinc-500">
                      {finding.evidence_summary}
                    </p>
                  </div>
                </Td>
                <Td>{systemById.get(finding.system_id) ?? "Unknown system"}</Td>
                <Td>{labelize(finding.severity)}</Td>
                <Td>{labelize(finding.status)}</Td>
                <Td>
                  <span className="font-mono text-red-100">
                    {Object.entries(finding.score_impact)
                      .map(([domain, value]) => `${domain}: ${String(value)}`)
                      .join(", ") || "calculated"}
                  </span>
                </Td>
              </tr>
            ))}
            {!activeFindings.length ? (
              <tr>
                <td colSpan={5} className="px-4 py-3">
                  <p className="py-6 text-center text-sm text-zinc-500">No findings generated.</p>
                </td>
              </tr>
            ) : null}
          </tbody>
        </TableShell>
      </section>
    </AppShell>
  );
}
