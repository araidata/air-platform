"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { ArrowLeft, FileSearch, Radar, Scale } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { TableHead, TableShell, Td, Th } from "@/components/data-table";
import { PageHeader } from "@/components/page-header";
import { ScoreRing } from "@/components/score-ring";
import {
  type ApiAirbReview,
  type ApiAssessment,
  type ApiEvidence,
  type ApiFinding,
  type ApiScore,
  type ApiScannerRun,
  type ApiSystem,
  apiClient,
} from "@/lib/api-client";
import { formatDate, labelize, StatusPill } from "@/lib/format";

export default function SystemDetailPage() {
  const params = useParams<{ id: string }>();
  const id = params.id;
  const [system, setSystem] = useState<ApiSystem | null>(null);
  const [assessments, setAssessments] = useState<ApiAssessment[]>([]);
  const [findings, setFindings] = useState<ApiFinding[]>([]);
  const [evidence, setEvidence] = useState<ApiEvidence[]>([]);
  const [scores, setScores] = useState<ApiScore[]>([]);
  const [runs, setRuns] = useState<ApiScannerRun[]>([]);
  const [reviews, setReviews] = useState<ApiAirbReview[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      const [systemRecord, assessmentRecords, findingRecords, evidenceRecords, scoreRecords, runRecords, reviewRecords] =
        await Promise.all([
          apiClient.system(id),
          apiClient.assessments(),
          apiClient.findings(),
          apiClient.evidence(),
          apiClient.systemScores(id),
          apiClient.systemScannerRuns(id),
          apiClient.airbReviews(),
        ]);
      setSystem(systemRecord);
      setAssessments(assessmentRecords.filter((assessment) => assessment.system_id === id));
      setFindings(findingRecords.filter((finding) => finding.system_id === id));
      setEvidence(evidenceRecords.filter((record) => record.system_id === id));
      setScores(scoreRecords);
      setRuns(runRecords);
      setReviews(reviewRecords.filter((review) => review.system_id === id));
    }
    loadData().catch((caught) =>
      setError(caught instanceof Error ? caught.message : "Unable to load system detail"),
    );
  }, [id]);

  const scoreByDomain = useMemo(
    () => new Map(scores.map((score) => [score.score_domain, score.score_value])),
    [scores],
  );
  const overallScore = Math.round(scoreByDomain.get("overall_governance") ?? 0);
  const hasScores = scores.length > 0;
  const activeFindings = findings.filter((finding) => !["closed", "false_positive"].includes(finding.status));
  const latestReview = reviews[0];

  return (
    <AppShell>
      <Link
        href="/inventory"
        className="mb-4 inline-flex items-center gap-2 text-sm font-medium text-cyan-100 hover:text-cyan-50"
      >
        <ArrowLeft className="size-4" aria-hidden="true" />
        AI Inventory
      </Link>

      {error ? (
        <div className="mb-4 rounded-lg border border-red-300/20 bg-red-300/10 p-3 text-sm text-red-100">
          {error}
        </div>
      ) : null}

      <PageHeader
        title={system?.system_name ?? "System Detail"}
        description={system?.business_purpose ?? "Loading system record."}
        actions={system ? <StatusPill value={system.approval_status} /> : null}
      />

      {system ? (
        <>
          <div className="grid gap-4 lg:grid-cols-[1fr_360px]">
            <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
              <div className="grid gap-4 md:grid-cols-4">
                <Info label="Department / owner" value={system.department_owner} />
                <Info label="Risk tier" value={labelize(system.risk_tier)} />
                <Info label="Environment" value={labelize(system.deployment_environment)} />
                <Info label="Model" value={`${system.model_provider ?? "Provider not set"} / ${system.model_version ?? "version not set"}`} />
              </div>
              <div className="mt-4 grid gap-4 md:grid-cols-4">
                <Info label="Target type" value={labelize(system.target_type)} />
                <Info label="Target location" value={system.target_location} />
                <Info label="Authentication" value={labelize(system.authentication_type)} />
                <Info label="Assessment method" value={labelize(system.assessment_method)} />
              </div>
              <div className="mt-5 grid gap-4 md:grid-cols-[240px_1fr]">
                <div className="rounded-lg border border-white/10 bg-black/20 p-4">
                  {hasScores ? (
                    <ScoreRing score={overallScore} />
                  ) : (
                    <p className="text-sm text-zinc-500">No governance scores available.</p>
                  )}
                  <div className="mt-4 flex flex-wrap gap-2">
                    {system.public_facing ? <StatusPill value="public_facing" /> : null}
                    {system.rights_impacting ? <StatusPill value="rights_impacting" /> : null}
                    {system.safety_impacting ? <StatusPill value="safety_impacting" /> : null}
                    {system.uses_pii ? <StatusPill value="pii" /> : null}
                    {system.uses_phi ? <StatusPill value="phi" /> : null}
                    {system.uses_cjis ? <StatusPill value="cjis" /> : null}
                  </div>
                </div>
                <div className="rounded-lg border border-white/10 bg-black/20 p-4">
                  <h2 className="text-base font-semibold text-zinc-50">Domain Scores</h2>
                  <div className="mt-4 grid gap-3 sm:grid-cols-2">
                    {hasScores ? ["security", "privacy", "bias_civil_rights", "explainability", "governance_evidence"].map(
                      (domain) => {
                        const value = Math.round(scoreByDomain.get(domain) ?? 0);
                        return (
                          <div key={domain} className="rounded-md border border-white/10 p-3">
                            <div className="flex items-center justify-between gap-3">
                              <span className="text-sm text-zinc-300">{labelize(domain)}</span>
                              <span className="font-mono text-sm text-zinc-100">{value}</span>
                            </div>
                            <div className="mt-2 h-2 rounded-full bg-white/10">
                              <div className="h-2 rounded-full bg-emerald-300" style={{ width: `${value}%` }} />
                            </div>
                          </div>
                        );
                      },
                    ) : <p className="text-sm text-zinc-500">No real assessment has produced score records for this system.</p>}
                  </div>
                </div>
              </div>
            </section>

            <aside className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
              <div className="flex items-center gap-2">
                <Scale className="size-5 text-cyan-100" aria-hidden="true" />
                <h2 className="text-base font-semibold text-zinc-50">Review Board Packet</h2>
              </div>
              {latestReview ? (
                <div className="mt-4 space-y-4">
                  <StatusPill value={latestReview.review_status} />
                  <p className="text-sm leading-6 text-zinc-400">
                    {latestReview.decision_notes ?? "No decision notes recorded."}
                  </p>
                  <Info label="Exception expiration" value={formatDate(latestReview.expiration_date)} />
                  <Info label="Evidence records" value={`${evidence.length}`} />
                  <Info label="Open findings" value={`${activeFindings.length}`} />
                </div>
              ) : (
                <div className="mt-4">
                  <p className="text-sm text-zinc-500">No AIRB review has been created for this system.</p>
                  <Link
                    href="/review-board"
                    className="mt-3 inline-flex h-10 items-center rounded-md border border-cyan-300/25 bg-cyan-300/10 px-3 text-sm font-medium text-cyan-50"
                  >
                    Create AIRB review
                  </Link>
                </div>
              )}
            </aside>
          </div>

          <div className="mt-6 grid gap-6 xl:grid-cols-2">
            <section>
              <h2 className="mb-3 text-base font-semibold text-zinc-50">Linked Findings</h2>
              <TableShell label="System findings">
                <TableHead>
                  <tr>
                    <Th>Finding</Th>
                    <Th>Severity</Th>
                    <Th>Status</Th>
                    <Th>Domain</Th>
                  </tr>
                </TableHead>
                <tbody className="divide-y divide-white/10">
                  {findings.slice(0, 8).map((finding) => (
                    <tr key={finding.id}>
                      <Td>
                        <p className="font-mono text-xs text-zinc-500">{finding.id.slice(0, 8)}</p>
                        <p className="mt-1 font-medium text-zinc-100">{finding.title}</p>
                      </Td>
                      <Td>
                        <StatusPill value={finding.severity} />
                      </Td>
                      <Td>
                        <StatusPill value={finding.status} />
                      </Td>
                      <Td>{labelize(finding.domain)}</Td>
                    </tr>
                  ))}
                  {!findings.length ? (
                    <tr>
                      <td colSpan={4} className="px-4 py-3">
                        <p className="py-6 text-center text-sm text-zinc-500">No findings generated.</p>
                      </td>
                    </tr>
                  ) : null}
                </tbody>
              </TableShell>
            </section>

            <section>
              <h2 className="mb-3 text-base font-semibold text-zinc-50">Evidence Records</h2>
              <TableShell label="System evidence">
                <TableHead>
                  <tr>
                    <Th>Evidence</Th>
                    <Th>Type</Th>
                    <Th>Source</Th>
                  </tr>
                </TableHead>
                <tbody className="divide-y divide-white/10">
                  {evidence.slice(0, 8).map((record) => (
                    <tr key={record.id}>
                      <Td>
                        <p className="font-mono text-xs text-zinc-500">{record.id.slice(0, 8)}</p>
                        <p className="mt-1 font-medium text-zinc-100">{record.title}</p>
                      </Td>
                      <Td>{labelize(record.evidence_type)}</Td>
                      <Td>{record.created_by}</Td>
                    </tr>
                  ))}
                  {!evidence.length ? (
                    <tr>
                      <td colSpan={3} className="px-4 py-3">
                        <p className="py-6 text-center text-sm text-zinc-500">No evidence collected.</p>
                      </td>
                    </tr>
                  ) : null}
                </tbody>
              </TableShell>
            </section>
          </div>

          <div className="mt-6 grid gap-6 xl:grid-cols-2">
            <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
              <div className="flex items-center gap-2">
                <FileSearch className="size-5 text-cyan-100" aria-hidden="true" />
                <h2 className="text-base font-semibold text-zinc-50">Assessments</h2>
              </div>
              <div className="mt-3 grid gap-3">
                {assessments.map((assessment) => (
                  <div key={assessment.id} className="rounded-lg border border-white/10 bg-black/20 p-4">
                    <p className="font-mono text-xs text-zinc-500">{assessment.id.slice(0, 8)}</p>
                    <p className="mt-2 font-medium text-zinc-100">{assessment.assessment_type}</p>
                    <div className="mt-3">
                      <StatusPill value={assessment.status} />
                    </div>
                    <p className="mt-3 text-sm text-zinc-500">
                      {assessment.initiated_by} / {formatDate(assessment.created_at)}
                    </p>
                  </div>
                ))}
                {!assessments.length ? <p className="rounded-lg border border-white/10 bg-black/20 p-4 text-sm text-zinc-500">No assessments executed.</p> : null}
              </div>
            </section>

            <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
              <div className="flex items-center gap-2">
                <Radar className="size-5 text-cyan-100" aria-hidden="true" />
                <h2 className="text-base font-semibold text-zinc-50">Scanner Runs</h2>
              </div>
              <div className="mt-3 grid gap-3">
                {runs.map((run) => (
                  <div key={run.id} className="rounded-lg border border-white/10 bg-black/20 p-4">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <p className="font-mono text-xs text-zinc-500">{run.id.slice(0, 8)}</p>
                        <p className="mt-2 font-medium text-zinc-100">{labelize(run.scanner_name)}</p>
                      </div>
                      <StatusPill value={run.execution_status} />
                    </div>
                    <p className="mt-3 text-sm text-zinc-500">
                      {run.finding_count} findings / {run.raw_output_path ? "raw output preserved" : "pending output"}
                    </p>
                    {run.log_path ? (
                      <p className="mt-2 break-all font-mono text-xs text-zinc-500">{run.log_path}</p>
                    ) : null}
                    {run.error_message ? (
                      <p className="mt-2 text-sm text-red-200">{run.error_message}</p>
                    ) : null}
                  </div>
                ))}
                {!runs.length ? <p className="rounded-lg border border-white/10 bg-black/20 p-4 text-sm text-zinc-500">No scanner runs available.</p> : null}
              </div>
            </section>
          </div>
        </>
      ) : null}
    </AppShell>
  );
}

function Info({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-white/10 bg-black/20 p-4">
      <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">{label}</p>
      <p className="mt-2 text-sm font-medium text-zinc-100">{value}</p>
    </div>
  );
}
