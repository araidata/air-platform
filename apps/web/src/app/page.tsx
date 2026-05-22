import Link from "next/link";
import { ArrowRight, CircleAlert, FileCheck2, ShieldAlert } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { MetricCard } from "@/components/metric-card";
import { PageHeader } from "@/components/page-header";
import { ScoreRing } from "@/components/score-ring";
import {
  ApprovalBadge,
  FindingStatusBadge,
  RiskTierBadge,
  SeverityBadge,
} from "@/components/status-badge";
import {
  dashboardMetrics,
  findings,
  getSystemName,
  riskHeatmap,
  scoreExplanations,
  scoreTrend,
  systems,
} from "@/lib/mock-data";

function HeatCell({ value }: { value: number }) {
  const color =
    value < 50
      ? "bg-red-500/20 text-red-100"
      : value < 70
        ? "bg-amber-400/20 text-amber-100"
        : value < 85
          ? "bg-cyan-400/16 text-cyan-100"
          : "bg-emerald-400/16 text-emerald-100";

  return (
    <td className="px-2 py-2">
      <div className={`rounded-md px-2 py-2 text-center font-mono text-sm ${color}`}>
        {value}
      </div>
    </td>
  );
}

export default function ExecutiveDashboard() {
  const highRiskSystems = systems
    .filter((system) => system.riskTier === "Critical" || system.riskTier === "High")
    .sort((a, b) => a.riskScore - b.riskScore);
  const activeFindings = findings.filter((finding) => finding.status !== "Closed");
  const strongestScoreDrivers = scoreExplanations
    .filter((explanation) => explanation.impact < 0)
    .sort((a, b) => a.impact - b.impact)
    .slice(0, 5);

  return (
    <AppShell>
      <PageHeader
        title="Executive Dashboard"
        description="Countywide operating view for AI system risk, approval blockers, open findings, evidence completeness, and review board readiness."
      />

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <MetricCard
          label="Average governance score"
          value={dashboardMetrics.averageRiskScore}
          detail="Weighted Phase 3 score across active systems."
          tone="warn"
        />
        <MetricCard
          label="Open findings"
          value={dashboardMetrics.openFindings}
          detail="Active issues requiring triage or evidence."
          tone="bad"
        />
        <MetricCard
          label="Blocked systems"
          value={dashboardMetrics.blockedSystems}
          detail="Deployments blocked by governance review."
          tone="bad"
        />
        <MetricCard
          label="Evidence complete"
          value={`${dashboardMetrics.evidenceCompleteness}%`}
          detail="Average audit packet completeness."
          tone="neutral"
        />
        <MetricCard
          label="Board items"
          value={dashboardMetrics.awaitingReview}
          detail="Items needing AI Review Board action."
          tone="warn"
        />
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="mb-4 flex items-center justify-between gap-3">
            <div>
              <h2 className="text-base font-semibold text-zinc-50">
                Risk Heatmap
              </h2>
              <p className="mt-1 text-sm text-zinc-500">
                Domain scores by department.
              </p>
            </div>
            <FileCheck2 className="size-5 text-cyan-100" aria-hidden="true" />
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm" aria-label="Risk heatmap">
              <thead className="text-xs uppercase tracking-[0.08em] text-zinc-500">
                <tr>
                  <th className="px-2 py-2 text-left font-semibold">Department</th>
                  <th className="px-2 py-2 font-semibold">Security</th>
                  <th className="px-2 py-2 font-semibold">Civil rights</th>
                  <th className="px-2 py-2 font-semibold">Privacy</th>
                  <th className="px-2 py-2 font-semibold">Explainability</th>
                  <th className="px-2 py-2 font-semibold">Evidence</th>
                </tr>
              </thead>
              <tbody>
                {riskHeatmap.map((row) => (
                  <tr key={row.department} className="border-t border-white/10">
                    <td className="whitespace-nowrap px-2 py-2 font-medium text-zinc-200">
                      {row.department}
                    </td>
                    <HeatCell value={row.security} />
                    <HeatCell value={row.biasCivilRights} />
                    <HeatCell value={row.privacy} />
                    <HeatCell value={row.explainability} />
                    <HeatCell value={row.governanceEvidence} />
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="mb-4 flex items-center justify-between gap-3">
            <div>
              <h2 className="text-base font-semibold text-zinc-50">
                Portfolio Trend
              </h2>
              <p className="mt-1 text-sm text-zinc-500">
                Phase 3 portfolio score movement for board reporting.
              </p>
            </div>
            <ScoreRing score={dashboardMetrics.averageRiskScore} label="Current" />
          </div>
          <div className="mt-5 grid h-44 grid-cols-4 items-end gap-3">
            {scoreTrend.map((point) => (
              <div key={point.label} className="flex h-full flex-col justify-end gap-2">
                <div
                  className="rounded-t-md border border-cyan-300/15 bg-cyan-300/15"
                  style={{ height: `${point.score}%` }}
                />
                <div className="flex items-center justify-between text-xs text-zinc-500">
                  <span>{point.label}</span>
                  <span className="font-mono">{point.score}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="mb-4 flex items-center gap-2">
            <ShieldAlert className="size-5 text-amber-100" aria-hidden="true" />
            <h2 className="text-base font-semibold text-zinc-50">
              High-Risk Systems
            </h2>
          </div>
          <div className="space-y-3">
            {highRiskSystems.map((system) => (
              <Link
                href={`/systems/${system.id}`}
                key={system.id}
                className="block rounded-lg border border-white/10 bg-black/20 p-3 transition-colors hover:border-cyan-300/25 hover:bg-cyan-300/5"
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="font-medium text-zinc-100">{system.name}</p>
                    <p className="mt-1 text-sm text-zinc-500">{system.department}</p>
                  </div>
                  <RiskTierBadge riskTier={system.riskTier} />
                </div>
                <div className="mt-3 flex items-center justify-between gap-3">
                  <ApprovalBadge status={system.approvalStatus} />
                  <span className="font-mono text-sm text-zinc-300">
                    Score {system.riskScore}
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </section>

        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="mb-4 flex items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <CircleAlert className="size-5 text-red-100" aria-hidden="true" />
              <h2 className="text-base font-semibold text-zinc-50">
                Findings Needing Action
              </h2>
            </div>
            <Link
              href="/findings"
              className="inline-flex items-center gap-1 text-sm font-medium text-cyan-100 hover:text-cyan-50"
            >
              Queue <ArrowRight className="size-4" aria-hidden="true" />
            </Link>
          </div>
          <div className="divide-y divide-white/10">
            {activeFindings.slice(0, 5).map((finding) => (
              <div key={finding.id} className="grid gap-3 py-3 md:grid-cols-[1fr_auto]">
                <div>
                  <p className="font-medium text-zinc-100">{finding.title}</p>
                  <p className="mt-1 text-sm text-zinc-500">
                    {finding.id} · {getSystemName(finding.systemId)}
                  </p>
                </div>
                <div className="flex flex-wrap items-center gap-2 md:justify-end">
                  <SeverityBadge severity={finding.severity} />
                  <FindingStatusBadge status={finding.status} />
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>

      <section className="mt-6 rounded-lg border border-white/10 bg-white/[0.045] p-4">
        <div className="mb-4 flex items-center justify-between gap-3">
          <div>
            <h2 className="text-base font-semibold text-zinc-50">
              Score Drivers
            </h2>
            <p className="mt-1 text-sm text-zinc-500">
              Highest-impact explanations behind current governance scores.
            </p>
          </div>
          <Link
            href="/reports"
            className="inline-flex items-center gap-1 text-sm font-medium text-cyan-100 hover:text-cyan-50"
          >
            Reports <ArrowRight className="size-4" aria-hidden="true" />
          </Link>
        </div>
        <div className="grid gap-3 lg:grid-cols-5">
          {strongestScoreDrivers.map((driver) => (
            <div
              key={driver.id}
              className="rounded-lg border border-white/10 bg-black/20 p-3"
            >
              <div className="flex items-start justify-between gap-3">
                <p className="text-sm font-medium text-zinc-100">{driver.title}</p>
                <span className="font-mono text-sm text-red-100">{driver.impact}</span>
              </div>
              <p className="mt-2 text-xs uppercase tracking-[0.08em] text-zinc-500">
                {driver.domain}
              </p>
              <p className="mt-2 text-sm leading-5 text-zinc-500">
                {getSystemName(driver.systemId)}
              </p>
            </div>
          ))}
        </div>
      </section>
    </AppShell>
  );
}
