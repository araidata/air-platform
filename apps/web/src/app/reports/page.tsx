import Link from "next/link";
import { ArrowUpRight, FileText, Gauge } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { PageHeader } from "@/components/page-header";
import { ScoreRing } from "@/components/score-ring";
import { ReviewStatusBadge, RiskTierBadge } from "@/components/status-badge";
import {
  getScoreExplanationsForSystem,
  getScoreHistoryForSystem,
  reviews,
  systems,
} from "@/lib/mock-data";

export default function ReportsPage() {
  const systemsByScore = [...systems].sort((a, b) => a.riskScore - b.riskScore);
  const reportRows = systemsByScore.map((system) => {
    const explanations = getScoreExplanationsForSystem(system.id);
    const history = getScoreHistoryForSystem(system.id);
    const current = history.at(-1);
    const previous = history.at(-2);
    const review = reviews.find((item) => item.systemId === system.id);

    return {
      system,
      explanations,
      review,
      trend: current && previous ? current.overall - previous.overall : 0,
    };
  });

  return (
    <AppShell>
      <PageHeader
        title="Governance Reports"
        description="Score-backed report workspace for executive summaries, board packets, remediation prioritization, and audit-ready exports."
      />

      <div className="mb-6 grid gap-4 md:grid-cols-3">
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="flex items-center gap-3">
            <Gauge className="size-5 text-cyan-100" aria-hidden="true" />
            <div>
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">
                Lowest system score
              </p>
              <p className="mt-1 font-mono text-3xl font-semibold text-red-100">
                {systemsByScore[0].riskScore}
              </p>
            </div>
          </div>
        </section>
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="flex items-center gap-3">
            <FileText className="size-5 text-amber-100" aria-hidden="true" />
            <div>
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">
                Score explanations
              </p>
              <p className="mt-1 font-mono text-3xl font-semibold text-amber-100">
                {reportRows.reduce((sum, row) => sum + row.explanations.length, 0)}
              </p>
            </div>
          </div>
        </section>
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">
            Report scope
          </p>
          <p className="mt-2 text-sm leading-6 text-zinc-300">
            Current scores, domain breakdowns, AIRB status, score movement, and top
            explanation records.
          </p>
        </section>
      </div>

      <div className="grid gap-4">
        {reportRows.map(({ system, explanations, review, trend }) => (
          <section
            key={system.id}
            className="rounded-lg border border-white/10 bg-white/[0.045] p-4"
          >
            <div className="grid gap-4 xl:grid-cols-[280px_1fr_280px]">
              <div>
                <Link
                  href={`/systems/${system.id}`}
                  className="inline-flex items-center gap-1 text-lg font-semibold text-zinc-50 hover:text-cyan-100"
                >
                  {system.name}
                  <ArrowUpRight className="size-4" aria-hidden="true" />
                </Link>
                <p className="mt-1 text-sm text-zinc-500">{system.department}</p>
                <div className="mt-3 flex flex-wrap gap-2">
                  <RiskTierBadge riskTier={system.riskTier} />
                  {review ? <ReviewStatusBadge status={review.status} /> : null}
                </div>
              </div>

              <div className="grid gap-3 md:grid-cols-5">
                {[
                  ["Security", system.domains.security],
                  ["Privacy", system.domains.privacy],
                  ["Civil Rights", system.domains.biasCivilRights],
                  ["Explainability", system.domains.explainability],
                  ["Evidence", system.domains.governanceEvidence],
                ].map(([label, value]) => (
                  <div key={label} className="rounded-lg border border-white/10 bg-black/20 p-3">
                    <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">
                      {label}
                    </p>
                    <p className="mt-2 font-mono text-2xl font-semibold text-zinc-100">
                      {value}
                    </p>
                  </div>
                ))}
              </div>

              <div className="rounded-lg border border-white/10 bg-black/20 p-3">
                <ScoreRing score={system.riskScore} label="Overall" />
                <p
                  className={`mt-3 font-mono text-sm ${
                    trend >= 0 ? "text-emerald-100" : "text-red-100"
                  }`}
                >
                  {trend >= 0 ? "+" : ""}
                  {trend} since prior snapshot
                </p>
              </div>
            </div>

            <div className="mt-4 grid gap-3 md:grid-cols-3">
              {explanations.slice(0, 3).map((explanation) => (
                <div
                  key={explanation.id}
                  className="rounded-lg border border-white/10 bg-black/20 p-3"
                >
                  <div className="flex items-start justify-between gap-3">
                    <p className="text-sm font-medium text-zinc-100">
                      {explanation.title}
                    </p>
                    <span
                      className={`font-mono text-sm ${
                        explanation.impact < 0 ? "text-red-100" : "text-emerald-100"
                      }`}
                    >
                      {explanation.impact > 0 ? `+${explanation.impact}` : explanation.impact}
                    </span>
                  </div>
                  <p className="mt-2 text-sm leading-5 text-zinc-500">
                    {explanation.description}
                  </p>
                </div>
              ))}
            </div>
          </section>
        ))}
      </div>
    </AppShell>
  );
}
