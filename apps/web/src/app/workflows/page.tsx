"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import {
  CheckCircle2,
  ClipboardList,
  FileSearch,
  Play,
  RefreshCw,
  Route,
  Scale,
} from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { MetricCard } from "@/components/metric-card";
import { PageHeader } from "@/components/page-header";
import {
  type ApiAssessment,
  type ApiAssessmentProfile,
  type ApiRecommendedScan,
  type ApiScanRecommendations,
  type ApiScannerDefinition,
  type ApiScannerRun,
  type ApiSystem,
  apiClient,
} from "@/lib/api-client";
import { labelize, StatusPill } from "@/lib/format";

const governanceDomains = [
  "security",
  "privacy",
  "bias_civil_rights",
  "explainability",
  "governance_evidence",
  "rag_integrity",
  "agent_safety",
];

const fieldClass =
  "mt-2 h-10 w-full rounded-md border border-white/10 bg-black/30 px-3 text-sm text-zinc-100";

export default function GuidedWorkflowPage() {
  const [systems, setSystems] = useState<ApiSystem[]>([]);
  const [profiles, setProfiles] = useState<ApiAssessmentProfile[]>([]);
  const [scanners, setScanners] = useState<ApiScannerDefinition[]>([]);
  const [assessments, setAssessments] = useState<ApiAssessment[]>([]);
  const [runs, setRuns] = useState<ApiScannerRun[]>([]);
  const [recommendations, setRecommendations] = useState<ApiScanRecommendations | null>(null);
  const [selectedSystemId, setSelectedSystemId] = useState("");
  const [selectedProfileId, setSelectedProfileId] = useState("");
  const [selectedDomains, setSelectedDomains] = useState<string[]>([
    "security",
    "privacy",
    "bias_civil_rights",
  ]);
  const [selectedScanTypeIds, setSelectedScanTypeIds] = useState<string[]>([]);
  const [selectedScannerId, setSelectedScannerId] = useState("");
  const [createdAssessment, setCreatedAssessment] = useState<ApiAssessment | null>(null);
  const [createdRun, setCreatedRun] = useState<ApiScannerRun | null>(null);
  const [isWorking, setIsWorking] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      const [systemRecords, profileRecords, scannerRecords, assessmentRecords, runRecords] =
        await Promise.all([
          apiClient.systems(),
          apiClient.assessmentProfiles(),
          apiClient.scannerDefinitions(),
          apiClient.assessments(),
          apiClient.scannerRuns(),
        ]);
      setSystems(systemRecords);
      setProfiles(profileRecords);
      setScanners(scannerRecords);
      setAssessments(assessmentRecords);
      setRuns(runRecords);
      setSelectedSystemId(systemRecords[0]?.id ?? "");
      setSelectedProfileId(profileRecords[0]?.id ?? "");
      setSelectedScannerId(scannerRecords.find((scanner) => scanner.enabled)?.id ?? "");
    }
    loadData().catch((caught) =>
      setError(caught instanceof Error ? caught.message : "Unable to load workflow data"),
    );
  }, []);

  useEffect(() => {
    if (!selectedSystemId) return;
    async function loadRecommendations() {
      const next = await apiClient.recommendedScans(selectedSystemId, selectedProfileId || undefined);
      setRecommendations(next);
      const defaultScanIds = [...next.required_scans, ...next.optional_scans]
        .slice(0, 3)
        .map((item) => item.scan_type.id);
      setSelectedScanTypeIds((current) => current.length ? current : defaultScanIds);
    }
    loadRecommendations().catch((caught) =>
      setError(caught instanceof Error ? caught.message : "Unable to load recommended scans"),
    );
  }, [selectedProfileId, selectedSystemId]);

  const selectedSystem = systems.find((system) => system.id === selectedSystemId);
  const selectedProfile = profiles.find((profile) => profile.id === selectedProfileId);
  const selectedScans = useMemo(() => {
    const recommended = [...(recommendations?.required_scans ?? []), ...(recommendations?.optional_scans ?? [])];
    return selectedScanTypeIds
      .map((id) => recommended.find((item) => item.scan_type.id === id))
      .filter(Boolean) as ApiRecommendedScan[];
  }, [recommendations, selectedScanTypeIds]);
  const firstSelectedScan = selectedScans[0]?.scan_type;
  const compatibleScanners = useMemo(() => {
    if (selectedScans[0]) return selectedScans[0].available_scanners;
    const recommended = [...(recommendations?.required_scans ?? []), ...(recommendations?.optional_scans ?? [])];
    return recommended[0]?.available_scanners ?? scanners.filter((scanner) => scanner.enabled);
  }, [recommendations, scanners, selectedScans]);
  const activeScannerId = compatibleScanners.some((scanner) => scanner.id === selectedScannerId)
    ? selectedScannerId
    : compatibleScanners[0]?.id ?? "";
  const existingSystemAssessment = assessments.find((assessment) => assessment.system_id === selectedSystemId);
  const existingSystemRuns = runs.filter((run) => run.system_id === selectedSystemId);

  function toggleDomain(domain: string) {
    setSelectedDomains((current) =>
      current.includes(domain) ? current.filter((item) => item !== domain) : [...current, domain],
    );
  }

  function toggleScan(scanId: string) {
    setSelectedScanTypeIds((current) =>
      current.includes(scanId) ? current.filter((item) => item !== scanId) : [...current, scanId],
    );
  }

  async function launchAssessment(executeScanner: boolean) {
    if (!selectedSystem || !selectedProfile) return;
    setIsWorking(true);
    setError(null);
    try {
      const assessment = await apiClient.createAssessment({
        system_id: selectedSystem.id,
        assessment_type: selectedProfile.profile_name,
        initiated_by: "frontend-operator",
        status: executeScanner ? "running" : "under_review",
        started_at: new Date().toISOString(),
        summary: `Guided assessment for ${selectedSystem.system_name}`,
        notes: `Domains: ${selectedDomains.join(", ")}. Profile: ${selectedProfile.profile_name}. Target: ${selectedSystem.target_type} at ${selectedSystem.target_location}.`,
      });
      setCreatedAssessment(assessment);

      if (executeScanner && firstSelectedScan && activeScannerId) {
        const run = await apiClient.createScannerRun({
          system_id: selectedSystem.id,
          assessment_id: assessment.id,
          scanner_definition_id: activeScannerId,
          scan_type_id: firstSelectedScan.id,
          assessment_profile_id: selectedProfile.id,
          initiated_by: "frontend-operator",
        });
        const executed = await apiClient.executeScannerRun(run.id, "frontend-operator");
        setCreatedRun(executed);
        setMessage("Assessment created and scanner executed");
      } else {
        setMessage("Assessment created");
      }

      const [nextAssessments, nextRuns] = await Promise.all([
        apiClient.assessments(),
        apiClient.scannerRuns(),
      ]);
      setAssessments(nextAssessments);
      setRuns(nextRuns);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to launch assessment");
    } finally {
      setIsWorking(false);
    }
  }

  async function routeToAirb() {
    const assessment = createdAssessment ?? existingSystemAssessment;
    if (!selectedSystem) return;
    setIsWorking(true);
    setError(null);
    try {
      await apiClient.createAirbReview({
        system_id: selectedSystem.id,
        assessment_id: assessment?.id,
        review_status: "under_review",
        decision_notes: "Routed from guided operator workflow.",
        civil_rights_review_status: selectedDomains.includes("bias_civil_rights") ? "required" : "not_started",
        accessibility_review_status: selectedSystem.public_facing ? "required" : "not_started",
        language_access_review_status: selectedSystem.public_facing ? "required" : "not_started",
        fairness_review_status: selectedSystem.rights_impacting ? "required" : "not_started",
        actor: "frontend-operator",
      });
      setMessage("AIRB review created");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to route AIRB review");
    } finally {
      setIsWorking(false);
    }
  }

  return (
    <AppShell>
      <PageHeader
        title="Guided Operator Workflow"
        description="Add or select a system, choose an assessment profile, review recommended scans, execute scanner work, and route governance review."
        actions={<Route className="size-6 text-cyan-100" aria-hidden="true" />}
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

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard
          label="Systems"
          value={systems.length}
          detail="Registered inventory records"
          tone="neutral"
          badgeLabel="Intake"
        />
        <MetricCard
          label="Profiles"
          value={profiles.length}
          detail="Assessment templates available"
          tone="neutral"
          badgeLabel="Plan"
        />
        <MetricCard
          label="Recommended scans"
          value={(recommendations?.required_scans.length ?? 0) + (recommendations?.optional_scans.length ?? 0)}
          detail="Required and optional controls"
          tone="neutral"
          badgeLabel="Scans"
        />
        <MetricCard
          label="Prior runs"
          value={existingSystemRuns.length}
          detail="Scanner history for selected system"
          tone="good"
          badgeLabel="Evidence"
        />
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[1fr_360px]">
        <section className="space-y-4">
          <div className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
            <div className="flex items-center gap-2">
              <span className="grid size-7 place-items-center rounded-md border border-cyan-300/20 text-sm text-cyan-100">
                1
              </span>
              <h2 className="text-base font-semibold text-zinc-50">Add or Select AI System</h2>
              <Link href="/inventory" className="ml-auto text-sm font-medium text-cyan-100">
                Manage inventory
              </Link>
            </div>
            <label className="mt-4 block">
              <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Target system</span>
              <select
                value={selectedSystemId}
                onChange={(event) => setSelectedSystemId(event.target.value)}
                className={fieldClass}
              >
                {systems.map((system) => (
                  <option key={system.id} value={system.id}>
                    {system.system_name}
                  </option>
                ))}
              </select>
            </label>
            {selectedSystem ? (
              <div className="mt-3 space-y-3">
                <div className="flex flex-wrap gap-2">
                  <StatusPill value={selectedSystem.risk_tier} />
                  <StatusPill value={selectedSystem.approval_status} />
                  <StatusPill value={selectedSystem.target_type} />
                  <StatusPill value={selectedSystem.assessment_method} />
                  {selectedSystem.public_facing ? <StatusPill value="public_facing" /> : null}
                  {selectedSystem.rights_impacting ? <StatusPill value="rights_impacting" /> : null}
                </div>
                <div className="grid gap-3 md:grid-cols-2">
                  <Info label="Target location" value={selectedSystem.target_location} />
                  <Info label="Authentication" value={labelize(selectedSystem.authentication_type)} />
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {(selectedSystem.scanner_compatible.length
                    ? selectedSystem.scanner_compatible
                    : ["no scanner compatibility set"]
                  ).map((item) => (
                    <span
                      key={item}
                      className="rounded-md border border-white/10 bg-black/20 px-2 py-1 text-xs text-zinc-300"
                    >
                      {labelize(item)}
                    </span>
                  ))}
                </div>
              </div>
            ) : null}
          </div>

          <div className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
            <div className="flex items-center gap-2">
              <span className="grid size-7 place-items-center rounded-md border border-cyan-300/20 text-sm text-cyan-100">
                2
              </span>
              <h2 className="text-base font-semibold text-zinc-50">Choose Assessment Profile</h2>
            </div>
            <label className="mt-4 block">
              <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Assessment template</span>
              <select
                value={selectedProfileId}
                onChange={(event) => setSelectedProfileId(event.target.value)}
                className={fieldClass}
              >
                {profiles.map((profile) => (
                  <option key={profile.id} value={profile.id}>
                    {profile.profile_name}
                  </option>
                ))}
              </select>
            </label>
            {selectedProfile ? (
              <p className="mt-3 text-sm leading-6 text-zinc-400">{selectedProfile.description}</p>
            ) : null}
          </div>

          <div className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
            <div className="flex items-center gap-2">
              <span className="grid size-7 place-items-center rounded-md border border-cyan-300/20 text-sm text-cyan-100">
                3
              </span>
              <h2 className="text-base font-semibold text-zinc-50">Select Governance Domains</h2>
            </div>
            <div className="mt-4 flex flex-wrap gap-2">
              {governanceDomains.map((domain) => (
                <button
                  key={domain}
                  type="button"
                  onClick={() => toggleDomain(domain)}
                  className={`rounded-md border px-3 py-2 text-sm ${
                    selectedDomains.includes(domain)
                      ? "border-cyan-300/30 bg-cyan-300/10 text-cyan-50"
                      : "border-white/10 bg-black/20 text-zinc-400"
                  }`}
                >
                  {labelize(domain)}
                </button>
              ))}
            </div>
          </div>

          <div className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
            <div className="flex items-center gap-2">
              <span className="grid size-7 place-items-center rounded-md border border-cyan-300/20 text-sm text-cyan-100">
                4
              </span>
              <h2 className="text-base font-semibold text-zinc-50">Review Recommended Scans</h2>
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              {[...(recommendations?.required_scans ?? []), ...(recommendations?.optional_scans ?? [])].map(
                (item) => (
                  <button
                    key={item.scan_type.id}
                    type="button"
                    onClick={() => toggleScan(item.scan_type.id)}
                    className={`rounded-lg border p-3 text-left ${
                      selectedScanTypeIds.includes(item.scan_type.id)
                        ? "border-cyan-300/25 bg-cyan-300/10"
                        : "border-white/10 bg-black/20"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-3">
                      <p className="font-medium text-zinc-100">{item.scan_type.display_name}</p>
                      <span className="rounded-md border border-white/10 px-2 py-1 text-xs text-zinc-300">
                        {item.required ? "Required" : "Optional"}
                      </span>
                    </div>
                    <p className="mt-2 text-sm leading-5 text-zinc-500">{item.reason}</p>
                    <p className="mt-2 text-xs uppercase tracking-[0.08em] text-zinc-500">
                      {labelize(item.scan_type.domain)} / {item.available_scanners.length} scanners
                    </p>
                  </button>
                ),
              )}
            </div>
          </div>

          <div className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
            <div className="flex items-center gap-2">
              <span className="grid size-7 place-items-center rounded-md border border-cyan-300/20 text-sm text-cyan-100">
                5
              </span>
              <h2 className="text-base font-semibold text-zinc-50">Choose Scanner and Launch</h2>
            </div>
            <div className="mt-4 flex flex-wrap gap-2">
              {compatibleScanners.map((scanner) => (
                <button
                  key={scanner.id}
                  type="button"
                  onClick={() => setSelectedScannerId(scanner.id)}
                  className={`rounded-md border px-3 py-2 text-sm ${
                    activeScannerId === scanner.id
                      ? "border-cyan-300/30 bg-cyan-300/10 text-cyan-50"
                      : "border-white/10 bg-black/20 text-zinc-400"
                  }`}
                >
                  {scanner.display_name}
                </button>
              ))}
              {!compatibleScanners.length ? (
                <p className="text-sm text-zinc-500">
                  No automated scanner is compatible with this target configuration.
                </p>
              ) : null}
            </div>
            <div className="mt-4 flex flex-wrap gap-3">
              <button
                type="button"
                disabled={isWorking || !selectedSystem || !selectedProfile}
                onClick={() => launchAssessment(false)}
                className="inline-flex h-10 items-center gap-2 rounded-md border border-white/10 px-4 text-sm font-medium text-zinc-100 disabled:opacity-50"
              >
                <ClipboardList className="size-4" aria-hidden="true" />
                Create assessment
              </button>
              <button
                type="button"
                disabled={isWorking || !selectedSystem || !firstSelectedScan || !activeScannerId}
                onClick={() => launchAssessment(true)}
                className="inline-flex h-10 items-center gap-2 rounded-md border border-cyan-300/25 bg-cyan-300/10 px-4 text-sm font-medium text-cyan-50 disabled:opacity-50"
              >
                {isWorking ? <RefreshCw className="size-4 animate-spin" /> : <Play className="size-4" />}
                Create and run first scan
              </button>
              <button
                type="button"
                disabled={isWorking || !selectedSystem}
                onClick={routeToAirb}
                className="inline-flex h-10 items-center gap-2 rounded-md border border-emerald-300/20 bg-emerald-300/10 px-4 text-sm font-medium text-emerald-100 disabled:opacity-50"
              >
                <Scale className="size-4" aria-hidden="true" />
                Send to AIRB
              </button>
            </div>
          </div>
        </section>

        <aside className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="flex items-center gap-2">
            <FileSearch className="size-5 text-cyan-100" aria-hidden="true" />
            <h2 className="text-base font-semibold text-zinc-50">Assessment Plan</h2>
          </div>
          <div className="mt-4 space-y-4 text-sm">
            <div>
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">System</p>
              <p className="mt-1 text-zinc-100">{selectedSystem?.system_name ?? "Select a system"}</p>
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Assessment target</p>
              <p className="mt-1 text-zinc-100">
                {selectedSystem ? `${labelize(selectedSystem.target_type)} / ${selectedSystem.target_location}` : "Select a system"}
              </p>
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Profile</p>
              <p className="mt-1 text-zinc-100">{selectedProfile?.profile_name ?? "Select a profile"}</p>
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Governance implications</p>
              <div className="mt-2 flex flex-wrap gap-1.5">
                {selectedDomains.map((domain) => (
                  <StatusPill key={domain} value={domain} />
                ))}
              </div>
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Expected evidence</p>
              <ul className="mt-2 space-y-2 text-zinc-400">
                {(selectedProfile?.required_evidence_types ?? []).slice(0, 6).map((item) => (
                  <li key={item} className="flex gap-2">
                    <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-emerald-100" />
                    <span>{labelize(item)}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Selected scanners</p>
              <p className="mt-1 text-zinc-100">
                {scanners.find((scanner) => scanner.id === activeScannerId)?.display_name ?? "No compatible scanner"}
              </p>
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Latest outcome</p>
              {createdAssessment ? (
                <div className="mt-2 rounded-lg border border-white/10 bg-black/20 p-3">
                  <p className="font-mono text-xs text-zinc-500">{createdAssessment.id}</p>
                  <p className="mt-1 text-zinc-100">{labelize(createdAssessment.status)}</p>
                  {createdRun ? (
                    <p className="mt-2 text-sm text-zinc-400">
                      Scanner run {labelize(createdRun.execution_status)} with {createdRun.finding_count} findings.
                    </p>
                  ) : null}
                </div>
              ) : (
                <p className="mt-1 text-zinc-500">No assessment launched in this session.</p>
              )}
            </div>
          </div>
        </aside>
      </div>
    </AppShell>
  );
}

function Info({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-white/10 bg-black/20 p-3">
      <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">{label}</p>
      <p className="mt-2 break-all text-sm text-zinc-200">{value}</p>
    </div>
  );
}
