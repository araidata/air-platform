import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, CheckCircle2, Clock3 } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { TableHead, TableShell, Td, Th } from "@/components/data-table";
import { PageHeader } from "@/components/page-header";
import { ScoreRing } from "@/components/score-ring";
import {
  ApprovalBadge,
  AssessmentBadge,
  EvidenceBadge,
  FindingStatusBadge,
  ReviewStatusBadge,
  RiskTierBadge,
  SeverityBadge,
} from "@/components/status-badge";
import {
  formatDate,
  getAssessmentsForSystem,
  getEvidenceForSystem,
  getFindingsForSystem,
  getReviewForSystem,
  getSystemById,
  systems,
} from "@/lib/mock-data";

export function generateStaticParams() {
  return systems.map((system) => ({ id: system.id }));
}

export default async function SystemDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const system = getSystemById(id);

  if (!system) {
    notFound();
  }

  const systemFindings = getFindingsForSystem(system.id);
  const systemEvidence = getEvidenceForSystem(system.id);
  const systemAssessments = getAssessmentsForSystem(system.id);
  const review = getReviewForSystem(system.id);

  return (
    <AppShell>
      <Link
        href="/inventory"
        className="mb-4 inline-flex items-center gap-2 text-sm font-medium text-cyan-100 hover:text-cyan-50"
      >
        <ArrowLeft className="size-4" aria-hidden="true" />
        AI Inventory
      </Link>
      <PageHeader
        title={system.name}
        description={system.purpose}
        actions={<ApprovalBadge status={system.approvalStatus} />}
      />

      <div className="grid gap-4 lg:grid-cols-[1fr_360px]">
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="grid gap-4 md:grid-cols-4">
            <div className="rounded-lg border border-white/10 bg-black/20 p-4">
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">
                Department
              </p>
              <p className="mt-2 font-medium text-zinc-100">{system.department}</p>
              <p className="mt-1 text-sm text-zinc-500">{system.owner}</p>
            </div>
            <div className="rounded-lg border border-white/10 bg-black/20 p-4">
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">
                Risk tier
              </p>
              <div className="mt-2">
                <RiskTierBadge riskTier={system.riskTier} />
              </div>
              <p className="mt-2 text-sm text-zinc-500">{system.deploymentStatus}</p>
            </div>
            <div className="rounded-lg border border-white/10 bg-black/20 p-4">
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">
                Assessment
              </p>
              <div className="mt-2">
                <AssessmentBadge status={system.assessmentStatus} />
              </div>
              <p className="mt-2 text-sm text-zinc-500">
                {formatDate(system.lastAssessed)}
              </p>
            </div>
            <div className="rounded-lg border border-white/10 bg-black/20 p-4">
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">
                Review status
              </p>
              <div className="mt-2">
                <ReviewStatusBadge status={system.reviewStatus} />
              </div>
              <p className="mt-2 text-sm text-zinc-500">
                Next {formatDate(system.nextReview)}
              </p>
            </div>
          </div>

          <div className="mt-5 grid gap-4 md:grid-cols-[260px_1fr]">
            <div className="rounded-lg border border-white/10 bg-black/20 p-4">
              <ScoreRing score={system.riskScore} />
              <div className="mt-4">
                <p className="text-sm font-medium text-zinc-200">
                  Evidence completeness
                </p>
                <div className="mt-2 h-2 rounded-full bg-white/10">
                  <div
                    className="h-2 rounded-full bg-cyan-300"
                    style={{ width: `${system.evidenceCompleteness}%` }}
                  />
                </div>
                <p className="mt-2 font-mono text-sm text-zinc-400">
                  {system.evidenceCompleteness}%
                </p>
              </div>
            </div>
            <div className="rounded-lg border border-white/10 bg-black/20 p-4">
              <h2 className="text-base font-semibold text-zinc-50">
                Domain Scores
              </h2>
              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                {[
                  ["Security", system.domains.security],
                  ["Bias and Civil Rights", system.domains.biasCivilRights],
                  ["Privacy", system.domains.privacy],
                  ["Governance", system.domains.governance],
                ].map(([label, value]) => (
                  <div key={label} className="rounded-md border border-white/10 p-3">
                    <div className="flex items-center justify-between gap-3">
                      <span className="text-sm text-zinc-300">{label}</span>
                      <span className="font-mono text-sm text-zinc-100">{value}</span>
                    </div>
                    <div className="mt-2 h-2 rounded-full bg-white/10">
                      <div
                        className="h-2 rounded-full bg-emerald-300"
                        style={{ width: `${value}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <aside className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <h2 className="text-base font-semibold text-zinc-50">
            Review Board Packet
          </h2>
          {review ? (
            <div className="mt-4 space-y-4">
              <ReviewStatusBadge status={review.status} />
              <p className="text-sm leading-6 text-zinc-400">{review.decision}</p>
              <div>
                <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">
                  Meeting
                </p>
                <p className="mt-1 text-sm text-zinc-200">
                  {formatDate(review.meetingDate)}
                </p>
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">
                  Blockers
                </p>
                <div className="mt-2 space-y-2">
                  {review.blockers.length ? (
                    review.blockers.map((blocker) => (
                      <div key={blocker} className="flex items-start gap-2 text-sm">
                        <Clock3 className="mt-0.5 size-4 text-amber-100" />
                        <span className="text-zinc-300">{blocker}</span>
                      </div>
                    ))
                  ) : (
                    <div className="flex items-start gap-2 text-sm">
                      <CheckCircle2 className="mt-0.5 size-4 text-emerald-100" />
                      <span className="text-zinc-300">No open blockers</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ) : null}
        </aside>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        <section>
          <h2 className="mb-3 text-base font-semibold text-zinc-50">
            Linked Findings
          </h2>
          <TableShell label="System findings">
            <TableHead>
              <tr>
                <Th>Finding</Th>
                <Th>Severity</Th>
                <Th>Status</Th>
                <Th>Owner</Th>
              </tr>
            </TableHead>
            <tbody className="divide-y divide-white/10">
              {systemFindings.map((finding) => (
                <tr key={finding.id}>
                  <Td>
                    <p className="font-mono text-xs text-zinc-500">{finding.id}</p>
                    <p className="mt-1 font-medium text-zinc-100">{finding.title}</p>
                  </Td>
                  <Td>
                    <SeverityBadge severity={finding.severity} />
                  </Td>
                  <Td>
                    <FindingStatusBadge status={finding.status} />
                  </Td>
                  <Td>{finding.owner}</Td>
                </tr>
              ))}
            </tbody>
          </TableShell>
        </section>

        <section>
          <h2 className="mb-3 text-base font-semibold text-zinc-50">
            Evidence Records
          </h2>
          <TableShell label="System evidence">
            <TableHead>
              <tr>
                <Th>Evidence</Th>
                <Th>Type</Th>
                <Th>Audit</Th>
              </tr>
            </TableHead>
            <tbody className="divide-y divide-white/10">
              {systemEvidence.map((record) => (
                <tr key={record.id}>
                  <Td>
                    <p className="font-mono text-xs text-zinc-500">{record.id}</p>
                    <p className="mt-1 font-medium text-zinc-100">{record.title}</p>
                  </Td>
                  <Td>{record.type}</Td>
                  <Td>
                    <EvidenceBadge record={record} />
                  </Td>
                </tr>
              ))}
            </tbody>
          </TableShell>
        </section>
      </div>

      <section className="mt-6 rounded-lg border border-white/10 bg-white/[0.045] p-4">
        <h2 className="text-base font-semibold text-zinc-50">Assessments</h2>
        <div className="mt-3 grid gap-3 lg:grid-cols-3">
          {systemAssessments.map((assessment) => (
            <div key={assessment.id} className="rounded-lg border border-white/10 bg-black/20 p-4">
              <p className="font-mono text-xs text-zinc-500">{assessment.id}</p>
              <p className="mt-2 font-medium text-zinc-100">{assessment.name}</p>
              <div className="mt-3">
                <AssessmentBadge status={assessment.status} />
              </div>
              <p className="mt-3 text-sm text-zinc-500">
                {assessment.assessor} · {formatDate(assessment.completedAt)}
              </p>
            </div>
          ))}
        </div>
      </section>
    </AppShell>
  );
}
