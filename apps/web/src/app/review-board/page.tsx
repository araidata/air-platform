"use client";

import Link from "next/link";
import type { ReactNode } from "react";
import { useEffect, useMemo, useState } from "react";
import { CalendarDays, ClipboardCheck, LockKeyhole, Scale, Send } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { FilterBar } from "@/components/filter-bar";
import { MetricCard } from "@/components/metric-card";
import { PageHeader } from "@/components/page-header";
import {
  type ApiAirbReview,
  type ApiAssessment,
  type ApiEvidence,
  type ApiFinding,
  type ApiSystem,
  apiClient,
} from "@/lib/api-client";
import { formatDate, labelize, StatusPill } from "@/lib/format";

const fieldClass =
  "mt-2 h-10 w-full rounded-md border border-white/10 bg-black/30 px-3 text-sm text-zinc-100";
const textAreaClass =
  "mt-2 min-h-24 w-full rounded-md border border-white/10 bg-black/30 px-3 py-2 text-sm text-zinc-100";

export default function ReviewBoardPage() {
  const [systems, setSystems] = useState<ApiSystem[]>([]);
  const [assessments, setAssessments] = useState<ApiAssessment[]>([]);
  const [findings, setFindings] = useState<ApiFinding[]>([]);
  const [evidence, setEvidence] = useState<ApiEvidence[]>([]);
  const [reviews, setReviews] = useState<ApiAirbReview[]>([]);
  const [selectedReviewId, setSelectedReviewId] = useState<string | null>(null);
  const [selectedSystemId, setSelectedSystemId] = useState("");
  const [selectedAssessmentId, setSelectedAssessmentId] = useState("");
  const [decisionStatus, setDecisionStatus] = useState("under_review");
  const [decisionNotes, setDecisionNotes] = useState("");
  const [reviewedBy, setReviewedBy] = useState("AI assurance operator");
  const [exceptionDate, setExceptionDate] = useState("");
  const [civilRightsStatus, setCivilRightsStatus] = useState("not_started");
  const [accessibilityStatus, setAccessibilityStatus] = useState("not_started");
  const [languageStatus, setLanguageStatus] = useState("not_started");
  const [fairnessStatus, setFairnessStatus] = useState("not_started");
  const [humanReviewValidated, setHumanReviewValidated] = useState(false);
  const [appealPathValidated, setAppealPathValidated] = useState(false);
  const [activeFilter, setActiveFilter] = useState("All board items");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function loadData() {
    const [systemRecords, assessmentRecords, findingRecords, evidenceRecords, reviewRecords] =
      await Promise.all([
        apiClient.systems(),
        apiClient.assessments(),
        apiClient.findings(),
        apiClient.evidence(),
        apiClient.airbReviews(),
      ]);
    setSystems(systemRecords);
    setAssessments(assessmentRecords);
    setFindings(findingRecords);
    setEvidence(evidenceRecords);
    setReviews(reviewRecords);
    setSelectedSystemId((current) => current || systemRecords[0]?.id || "");
    setSelectedReviewId((current) => current ?? reviewRecords[0]?.id ?? null);
  }

  useEffect(() => {
    async function loadInitialData() {
      try {
        await loadData();
      } catch (caught) {
        setError(caught instanceof Error ? caught.message : "Unable to load AIRB workflow");
      }
    }
    void loadInitialData();
  }, []);

  const systemById = useMemo(
    () => new Map(systems.map((system) => [system.id, system])),
    [systems],
  );
  const assessmentById = useMemo(
    () => new Map(assessments.map((assessment) => [assessment.id, assessment])),
    [assessments],
  );
  const selectedReview = reviews.find((review) => review.id === selectedReviewId) ?? null;
  const selectedSystem = selectedReview
    ? systemById.get(selectedReview.system_id)
    : systems.find((system) => system.id === selectedSystemId);
  const systemAssessments = assessments.filter((assessment) => assessment.system_id === selectedSystemId);
  const reviewFindings = selectedReview
    ? findings.filter((finding) => finding.system_id === selectedReview.system_id)
    : [];
  const reviewEvidence = selectedReview
    ? evidence.filter(
        (record) =>
          record.system_id === selectedReview.system_id ||
          record.assessment_id === selectedReview.assessment_id,
      )
    : [];
  const visibleReviews = reviews.filter((review) => {
    if (activeFilter === "Ready for review") return ["pending", "under_review"].includes(review.review_status);
    if (activeFilter === "Blocked") return review.review_status === "blocked";
    if (activeFilter === "Approved exceptions") return review.exception_granted;
    if (activeFilter === "Civil-rights review") {
      return [
        review.civil_rights_review_status,
        review.accessibility_review_status,
        review.language_access_review_status,
        review.fairness_review_status,
      ].some((status) => status !== "not_started");
    }
    return true;
  });

  useEffect(() => {
    if (!selectedReview) return;
    // The decision form mirrors whichever AIRB review the operator selects.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setDecisionStatus(selectedReview.review_status);
    setDecisionNotes(selectedReview.decision_notes ?? "");
    setReviewedBy(selectedReview.reviewed_by ?? "AI assurance operator");
    setExceptionDate(selectedReview.expiration_date ?? "");
    setCivilRightsStatus(selectedReview.civil_rights_review_status);
    setAccessibilityStatus(selectedReview.accessibility_review_status);
    setLanguageStatus(selectedReview.language_access_review_status);
    setFairnessStatus(selectedReview.fairness_review_status);
    setHumanReviewValidated(selectedReview.human_review_validated);
    setAppealPathValidated(selectedReview.appeal_path_validated);
  }, [selectedReview]);

  async function createReview() {
    if (!selectedSystemId) return;
    setError(null);
    try {
      const created = await apiClient.createAirbReview({
        system_id: selectedSystemId,
        assessment_id: selectedAssessmentId || null,
        review_status: "under_review",
        decision_notes: "AIRB intake created from review board UI.",
        reviewed_by: reviewedBy,
        civil_rights_review_status: civilRightsStatus,
        accessibility_review_status: accessibilityStatus,
        language_access_review_status: languageStatus,
        fairness_review_status: fairnessStatus,
        human_review_validated: humanReviewValidated,
        appeal_path_validated: appealPathValidated,
        actor: "frontend-operator",
      });
      setSelectedReviewId(created.id);
      setMessage("AIRB intake created");
      await loadData();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to create AIRB review");
    }
  }

  async function updateDecision(status = decisionStatus) {
    if (!selectedReview) return;
    setError(null);
    try {
      const updated = await apiClient.updateAirbReview(selectedReview.id, {
        review_status: status,
        decision_notes: decisionNotes || `Decision updated to ${labelize(status)} from UI`,
        reviewed_by: reviewedBy,
        reviewed_at: new Date().toISOString(),
        exception_granted: status === "approved_with_exception",
        expiration_date: status === "approved_with_exception" ? exceptionDate || null : null,
        civil_rights_review_status: civilRightsStatus,
        accessibility_review_status: accessibilityStatus,
        language_access_review_status: languageStatus,
        fairness_review_status: fairnessStatus,
        human_review_validated: humanReviewValidated,
        appeal_path_validated: appealPathValidated,
        actor: "frontend-operator",
      });
      setMessage(`Review moved to ${labelize(updated.review_status)}`);
      await loadData();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to update AIRB decision");
    }
  }

  return (
    <AppShell>
      <PageHeader
        title="AI Review Board Queue"
        description="Create AIRB intake records, route review indicators, record approval decisions, exceptions, blockers, and evidence-backed notes."
        actions={<Scale className="size-6 text-cyan-100" aria-hidden="true" />}
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

      <div className="mb-6 grid gap-4 md:grid-cols-4">
        <MetricCard
          label="Pending board action"
          value={reviews.filter((review) => ["pending", "under_review"].includes(review.review_status)).length}
          detail="Reviews awaiting decision"
          tone="neutral"
          badgeLabel="AIRB"
        />
        <MetricCard
          label="Blocked systems"
          value={reviews.filter((review) => review.review_status === "blocked").length}
          detail="Board decisions blocking deployment"
          tone="bad"
          badgeLabel="Decision"
        />
        <MetricCard
          label="Exceptions"
          value={reviews.filter((review) => review.exception_granted).length}
          detail="Approved with expiration dates"
          tone="warn"
          badgeLabel="Exception"
        />
        <MetricCard
          label="Civil-rights routed"
          value={reviews.filter((review) => review.civil_rights_review_status !== "not_started").length}
          detail="Reviews with civil-rights indicators"
          tone="good"
          badgeLabel="Phase 6"
        />
      </div>

      <section className="mb-6 rounded-lg border border-white/10 bg-white/[0.045] p-4">
        <div className="flex items-center gap-2">
          <Send className="size-5 text-cyan-100" aria-hidden="true" />
          <h2 className="text-base font-semibold text-zinc-50">AIRB Intake</h2>
        </div>
        <div className="mt-4 grid gap-3 lg:grid-cols-3">
          <label>
            <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Linked system</span>
            <select value={selectedSystemId} onChange={(event) => setSelectedSystemId(event.target.value)} className={fieldClass}>
              {systems.map((system) => (
                <option key={system.id} value={system.id}>
                  {system.system_name}
                </option>
              ))}
            </select>
          </label>
          <label>
            <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Linked assessment</span>
            <select
              value={selectedAssessmentId}
              onChange={(event) => setSelectedAssessmentId(event.target.value)}
              className={fieldClass}
            >
              <option value="">No assessment selected</option>
              {systemAssessments.map((assessment) => (
                <option key={assessment.id} value={assessment.id}>
                  {assessment.assessment_type} / {labelize(assessment.status)}
                </option>
              ))}
            </select>
          </label>
          <label>
            <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Reviewer</span>
            <input value={reviewedBy} onChange={(event) => setReviewedBy(event.target.value)} className={fieldClass} />
          </label>
        </div>
        <div className="mt-4 flex flex-wrap gap-3">
          {[
            { label: "civil_rights", value: civilRightsStatus, setter: setCivilRightsStatus },
            { label: "accessibility", value: accessibilityStatus, setter: setAccessibilityStatus },
            { label: "language_access", value: languageStatus, setter: setLanguageStatus },
            { label: "fairness", value: fairnessStatus, setter: setFairnessStatus },
          ].map(({ label, value, setter }) => (
            <label key={label} className="block min-w-48">
              <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">{labelize(label)}</span>
              <select
                value={value}
                onChange={(event) => setter(event.target.value)}
                className={fieldClass}
              >
                {["not_started", "required", "under_review", "complete", "blocked"].map((item) => (
                  <option key={item} value={item}>
                    {labelize(item)}
                  </option>
                ))}
              </select>
            </label>
          ))}
          <label className="inline-flex items-center gap-2 rounded-md border border-white/10 bg-black/20 px-3 py-2 text-sm text-zinc-300">
            <input
              type="checkbox"
              checked={humanReviewValidated}
              onChange={(event) => setHumanReviewValidated(event.target.checked)}
            />
            Human review validated
          </label>
          <label className="inline-flex items-center gap-2 rounded-md border border-white/10 bg-black/20 px-3 py-2 text-sm text-zinc-300">
            <input
              type="checkbox"
              checked={appealPathValidated}
              onChange={(event) => setAppealPathValidated(event.target.checked)}
            />
            Appeal path validated
          </label>
          <button
            type="button"
            onClick={createReview}
            className="inline-flex h-10 items-center gap-2 rounded-md border border-cyan-300/25 bg-cyan-300/10 px-4 text-sm font-medium text-cyan-50"
          >
            <ClipboardCheck className="size-4" aria-hidden="true" />
            Create intake
          </button>
        </div>
      </section>

      <FilterBar
        items={["All board items", "Ready for review", "Blocked", "Civil-rights review", "Approved exceptions"]}
        activeItem={activeFilter}
        onChange={setActiveFilter}
      />

      <div className="grid gap-6 xl:grid-cols-[1fr_420px]">
        <div className="grid gap-4">
          {visibleReviews.map((review) => {
            const system = systemById.get(review.system_id);
            return (
              <section
                key={review.id}
                onClick={() => setSelectedReviewId(review.id)}
                className={`cursor-pointer rounded-lg border border-white/10 bg-white/[0.045] p-4 hover:border-cyan-300/20 ${
                  selectedReviewId === review.id ? "border-cyan-300/25" : ""
                }`}
              >
                <div className="grid gap-4 lg:grid-cols-[1fr_210px_220px]">
                  <div>
                    <p className="font-mono text-xs text-zinc-500">{review.id.slice(0, 8)}</p>
                    <Link
                      href={system ? `/systems/${system.id}` : "/inventory"}
                      className="mt-1 inline-block text-lg font-semibold text-zinc-50 hover:text-cyan-100"
                    >
                      {system?.system_name ?? "Unknown system"}
                    </Link>
                    <p className="mt-1 text-sm text-zinc-500">
                      {system?.department_owner ?? "Owner not set"} / {review.reviewed_by ?? "Reviewer not set"}
                    </p>
                    <p className="mt-3 max-w-3xl text-sm leading-6 text-zinc-400">
                      {review.decision_notes ?? "No decision notes recorded."}
                    </p>
                  </div>
                  <div className="space-y-2">
                    <StatusPill value={review.review_status} />
                    {review.exception_granted ? <StatusPill value="approved_with_exception" /> : null}
                    {system ? <StatusPill value={system.risk_tier} /> : null}
                  </div>
                  <div className="rounded-lg border border-white/10 bg-black/20 p-3">
                    <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Review indicators</p>
                    <div className="mt-2 flex flex-wrap gap-1.5">
                      {[review.civil_rights_review_status, review.accessibility_review_status, review.language_access_review_status, review.fairness_review_status]
                        .filter((status) => status !== "not_started")
                        .map((status, index) => (
                          <StatusPill key={`${status}-${index}`} value={status} />
                        ))}
                    </div>
                  </div>
                </div>
              </section>
            );
          })}
        </div>

        <aside className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="flex items-center gap-2">
            <LockKeyhole className="size-5 text-amber-100" aria-hidden="true" />
            <h2 className="text-base font-semibold text-zinc-50">Review Detail</h2>
          </div>
          {selectedReview ? (
            <div className="mt-4 space-y-4">
              <div>
                <p className="font-medium text-zinc-100">{selectedSystem?.system_name ?? "Unknown system"}</p>
                <p className="mt-1 text-sm text-zinc-500">
                  {assessmentById.get(selectedReview.assessment_id ?? "")?.assessment_type ?? "No linked assessment"}
                </p>
              </div>
              <div className="grid gap-3 sm:grid-cols-2">
                <label>
                  <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Decision</span>
                  <select value={decisionStatus} onChange={(event) => setDecisionStatus(event.target.value)} className={fieldClass}>
                    {["under_review", "approved", "approved_with_exception", "blocked"].map((item) => (
                      <option key={item} value={item}>
                        {labelize(item)}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Exception expiration</span>
                  <input
                    type="date"
                    value={exceptionDate}
                    onChange={(event) => setExceptionDate(event.target.value)}
                    className={fieldClass}
                  />
                </label>
              </div>
              <label className="block">
                <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Decision notes</span>
                <textarea value={decisionNotes} onChange={(event) => setDecisionNotes(event.target.value)} className={textAreaClass} />
              </label>
              <div className="flex flex-wrap gap-2">
                {["approved", "approved_with_exception", "blocked"].map((status) => (
                  <button
                    key={status}
                    type="button"
                    onClick={() => updateDecision(status)}
                    className="inline-flex h-10 items-center gap-2 rounded-md border border-white/10 px-3 text-sm font-medium text-zinc-100"
                  >
                    <Scale className="size-4" aria-hidden="true" />
                    {labelize(status)}
                  </button>
                ))}
                <button
                  type="button"
                  onClick={() => updateDecision()}
                  className="inline-flex h-10 items-center gap-2 rounded-md border border-cyan-300/25 bg-cyan-300/10 px-3 text-sm font-medium text-cyan-50"
                >
                  <ClipboardCheck className="size-4" aria-hidden="true" />
                  Save routing
                </button>
              </div>
              <div className="grid gap-3 sm:grid-cols-2">
                <Info icon={<CalendarDays className="size-4" />} label="Expiration" value={formatDate(selectedReview.expiration_date)} />
                <Info label="Linked findings" value={`${reviewFindings.length} findings`} />
                <Info label="Linked evidence" value={`${reviewEvidence.length} evidence records`} />
                <Info label="Open blockers" value={`${reviewFindings.filter((finding) => finding.approval_blocking).length} blockers`} />
              </div>
            </div>
          ) : (
            <p className="mt-4 text-sm text-zinc-500">Select a review to record a decision.</p>
          )}
        </aside>
      </div>
    </AppShell>
  );
}

function Info({
  label,
  value,
  icon,
}: {
  label: string;
  value: string;
  icon?: ReactNode;
}) {
  return (
    <div className="rounded-lg border border-white/10 bg-black/20 p-3">
      <div className="flex items-center gap-2 text-zinc-500">
        {icon}
        <p className="text-xs uppercase tracking-[0.08em]">{label}</p>
      </div>
      <p className="mt-2 text-sm text-zinc-100">{value}</p>
    </div>
  );
}
