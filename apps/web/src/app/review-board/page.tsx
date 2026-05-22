import Link from "next/link";
import { CalendarDays, ClipboardCheck, LockKeyhole } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { FilterBar } from "@/components/filter-bar";
import { PageHeader } from "@/components/page-header";
import { ScoreRing } from "@/components/score-ring";
import {
  ApprovalBadge,
  ReviewStatusBadge,
  RiskTierBadge,
} from "@/components/status-badge";
import {
  formatDate,
  getScoreExplanationsForSystem,
  getSystemById,
  reviews,
} from "@/lib/mock-data";

export default function ReviewBoardPage() {
  const blocked = reviews.filter((review) => review.status === "Blocked").length;
  const ready = reviews.filter((review) =>
    [
      "Ready for review",
      "Security review required",
      "Bias review required",
      "Privacy review required",
    ].includes(review.status),
  ).length;

  return (
    <AppShell>
      <PageHeader
        title="AI Review Board Queue"
        description="Board-ready systems, blocked approvals, approved exceptions, decision history, and evidence packet coverage."
      />

      <div className="mb-6 grid gap-4 md:grid-cols-3">
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="flex items-center gap-3">
            <ClipboardCheck className="size-5 text-cyan-100" aria-hidden="true" />
            <div>
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">
                Pending board action
              </p>
              <p className="mt-1 font-mono text-3xl font-semibold text-zinc-50">
                {ready}
              </p>
            </div>
          </div>
        </section>
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="flex items-center gap-3">
            <LockKeyhole className="size-5 text-red-100" aria-hidden="true" />
            <div>
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">
                Blocked systems
              </p>
              <p className="mt-1 font-mono text-3xl font-semibold text-red-100">
                {blocked}
              </p>
            </div>
          </div>
        </section>
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="flex items-center gap-3">
            <CalendarDays className="size-5 text-emerald-100" aria-hidden="true" />
            <div>
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">
                Scheduled reviews
              </p>
              <p className="mt-1 font-mono text-3xl font-semibold text-emerald-100">
                {reviews.length}
              </p>
            </div>
          </div>
        </section>
      </div>

      <FilterBar
        items={[
          "All board items",
          "Ready for review",
          "Blocked",
          "Security review",
          "Bias review",
          "Approved exceptions",
        ]}
      />

      <div className="grid gap-4">
        {reviews.map((review) => {
          const system = getSystemById(review.systemId);
          if (!system) {
            return null;
          }
          const topScoreDriver = getScoreExplanationsForSystem(system.id)
            .filter((explanation) => explanation.impact < 0)
            .sort((a, b) => a.impact - b.impact)[0];

          return (
            <section
              key={review.id}
              className="rounded-lg border border-white/10 bg-white/[0.045] p-4"
            >
              <div className="grid gap-4 lg:grid-cols-[1fr_240px_260px_220px]">
                <div>
                  <p className="font-mono text-xs text-zinc-500">{review.id}</p>
                  <Link
                    href={`/systems/${system.id}`}
                    className="mt-1 inline-block text-lg font-semibold text-zinc-50 hover:text-cyan-100"
                  >
                    {system.name}
                  </Link>
                  <p className="mt-1 text-sm text-zinc-500">
                    {system.department} · requested by {review.requestedBy}
                  </p>
                  <p className="mt-3 max-w-3xl text-sm leading-6 text-zinc-400">
                    {review.decision}
                  </p>
                </div>

                <div className="space-y-2">
                  <ReviewStatusBadge status={review.status} />
                  <ApprovalBadge status={system.approvalStatus} />
                  <RiskTierBadge riskTier={system.riskTier} />
                </div>

                <div className="rounded-lg border border-white/10 bg-black/20 p-3">
                  <ScoreRing score={system.riskScore} label="Governance" />
                  {topScoreDriver ? (
                    <p className="mt-3 text-sm leading-5 text-zinc-500">
                      {topScoreDriver.title}
                    </p>
                  ) : null}
                </div>

                <div className="rounded-lg border border-white/10 bg-black/20 p-3">
                  <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">
                    Meeting date
                  </p>
                  <p className="mt-1 font-medium text-zinc-100">
                    {formatDate(review.meetingDate)}
                  </p>
                  <p className="mt-3 text-xs uppercase tracking-[0.08em] text-zinc-500">
                    Evidence records
                  </p>
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {review.evidenceIds.map((evidenceId) => (
                      <span
                        key={evidenceId}
                        className="rounded-md border border-white/10 bg-white/[0.05] px-2 py-1 font-mono text-xs text-zinc-300"
                      >
                        {evidenceId}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {review.blockers.length ? (
                <div className="mt-4 rounded-lg border border-amber-300/15 bg-amber-300/10 p-3">
                  <p className="text-xs uppercase tracking-[0.08em] text-amber-100">
                    Approval blockers
                  </p>
                  <div className="mt-2 flex flex-wrap gap-2">
                    {review.blockers.map((blocker) => (
                      <span
                        key={blocker}
                        className="rounded-md border border-amber-300/20 bg-black/20 px-2 py-1 text-xs text-amber-50"
                      >
                        {blocker}
                      </span>
                    ))}
                  </div>
                </div>
              ) : null}
            </section>
          );
        })}
      </div>
    </AppShell>
  );
}
