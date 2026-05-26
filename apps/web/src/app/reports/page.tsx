"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { ArrowUpRight, FileText, Gauge } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { PageHeader } from "@/components/page-header";
import { ScoreRing } from "@/components/score-ring";
import { type ApiAirbReview, type ApiScore, type ApiSystem, apiClient } from "@/lib/api-client";
import { labelize, StatusPill } from "@/lib/format";

export default function ReportsPage() {
  const [systems, setSystems] = useState<ApiSystem[]>([]);
  const [scores, setScores] = useState<ApiScore[]>([]);
  const [reviews, setReviews] = useState<ApiAirbReview[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      const [systemRecords, scoreRecords, reviewRecords] = await Promise.all([
        apiClient.systems(),
        apiClient.scores(),
        apiClient.airbReviews(),
      ]);
      setSystems(systemRecords);
      setScores(scoreRecords);
      setReviews(reviewRecords);
    }
    loadData().catch((caught) => setError(caught instanceof Error ? caught.message : "Unable to load reports"));
  }, []);

  const scoresBySystem = useMemo(() => {
    const map = new Map<string, ApiScore[]>();
    for (const score of scores) {
      map.set(score.system_id, [...(map.get(score.system_id) ?? []), score]);
    }
    return map;
  }, [scores]);
  const reviewsBySystem = useMemo(() => new Map(reviews.map((review) => [review.system_id, review])), [reviews]);
  const overallScores = scores.filter((score) => score.score_domain === "overall_governance");
  const lowestScore = overallScores.length ? Math.min(...overallScores.map((score) => Math.round(score.score_value))) : null;
  const explanationCount = scores.reduce((sum, score) => sum + (score.explanations?.length ?? 0), 0);

  return (
    <AppShell>
      <PageHeader
        title="Governance Reports"
        description="Report workspace for real scores, AIRB status, evidence-backed findings, and audit-ready exports."
      />

      {error ? (
        <div className="mb-4 rounded-lg border border-red-300/20 bg-red-300/10 p-3 text-sm text-red-100">{error}</div>
      ) : null}

      <div className="mb-6 grid gap-4 md:grid-cols-3">
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="flex items-center gap-3">
            <Gauge className="size-5 text-cyan-100" aria-hidden="true" />
            <div>
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Lowest system score</p>
              <p className="mt-1 font-mono text-3xl font-semibold text-zinc-100">{lowestScore ?? "No scores"}</p>
            </div>
          </div>
        </section>
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="flex items-center gap-3">
            <FileText className="size-5 text-amber-100" aria-hidden="true" />
            <div>
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Score explanations</p>
              <p className="mt-1 font-mono text-3xl font-semibold text-amber-100">{explanationCount}</p>
            </div>
          </div>
        </section>
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Report scope</p>
          <p className="mt-2 text-sm leading-6 text-zinc-300">
            Reports only reflect records produced by real workflows. No demo findings, scanner runs, evidence, or score impacts are fabricated.
          </p>
        </section>
      </div>

      {!scores.length ? (
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-6">
          <p className="font-medium text-zinc-100">No governance scores available.</p>
          <p className="mt-2 text-sm text-zinc-500">Run a real assessment or recalculate scores after evidence and findings exist.</p>
        </section>
      ) : null}

      <div className="mt-6 grid gap-4">
        {systems.map((system) => {
          const systemScores = scoresBySystem.get(system.id) ?? [];
          const overall = systemScores.find((score) => score.score_domain === "overall_governance");
          if (!systemScores.length) return null;
          return (
            <section key={system.id} className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
              <div className="grid gap-4 xl:grid-cols-[280px_1fr_220px]">
                <div>
                  <Link href={`/systems/${system.id}`} className="inline-flex items-center gap-1 text-lg font-semibold text-zinc-50 hover:text-cyan-100">
                    {system.system_name}
                    <ArrowUpRight className="size-4" aria-hidden="true" />
                  </Link>
                  <p className="mt-1 text-sm text-zinc-500">{system.department_owner}</p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    <StatusPill value={system.risk_tier} />
                    {reviewsBySystem.get(system.id) ? <StatusPill value={reviewsBySystem.get(system.id)?.review_status ?? "pending"} /> : null}
                  </div>
                </div>

                <div className="grid gap-3 md:grid-cols-5">
                  {systemScores
                    .filter((score) => score.score_domain !== "overall_governance")
                    .slice(0, 5)
                    .map((score) => (
                      <div key={score.id} className="rounded-lg border border-white/10 bg-black/20 p-3">
                        <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">{labelize(score.score_domain)}</p>
                        <p className="mt-2 font-mono text-2xl font-semibold text-zinc-100">{Math.round(score.score_value)}</p>
                      </div>
                    ))}
                </div>

                <div className="rounded-lg border border-white/10 bg-black/20 p-3">
                  <ScoreRing score={Math.round(overall?.score_value ?? 0)} label="Overall" />
                </div>
              </div>
            </section>
          );
        })}
      </div>
    </AppShell>
  );
}
