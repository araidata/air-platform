"use client";

import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  CheckCircle2,
  FileJson,
  Play,
  Radar,
  ShieldCheck,
  TriangleAlert,
} from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { TableHead, TableShell, Td, Th } from "@/components/data-table";
import { MetricCard } from "@/components/metric-card";
import { PageHeader } from "@/components/page-header";
import {
  type ApiAssessment,
  type ApiAssessmentProfile,
  type ApiEvidence,
  type ApiFinding,
  type ApiScanRecommendations,
  type ApiScanType,
  type ApiScannerDefinition,
  type ApiScannerRun,
  type ApiSystem,
  apiClient,
} from "@/lib/api-client";

const toneForStatus = (status: string) => {
  if (status === "completed") return "border-emerald-300/20 bg-emerald-300/10 text-emerald-100";
  if (status === "failed") return "border-red-300/20 bg-red-300/10 text-red-100";
  if (status === "running") return "border-cyan-300/20 bg-cyan-300/10 text-cyan-100";
  return "border-zinc-500/20 bg-zinc-500/10 text-zinc-300";
};

const labelize = (value: string) =>
  value
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");

export default function ScannerEcosystemPage() {
  const [systems, setSystems] = useState<ApiSystem[]>([]);
  const [assessments, setAssessments] = useState<ApiAssessment[]>([]);
  const [scanners, setScanners] = useState<ApiScannerDefinition[]>([]);
  const [scanTypes, setScanTypes] = useState<ApiScanType[]>([]);
  const [profiles, setProfiles] = useState<ApiAssessmentProfile[]>([]);
  const [runs, setRuns] = useState<ApiScannerRun[]>([]);
  const [findings, setFindings] = useState<ApiFinding[]>([]);
  const [evidence, setEvidence] = useState<ApiEvidence[]>([]);
  const [recommendations, setRecommendations] = useState<ApiScanRecommendations | null>(null);
  const [selectedSystemId, setSelectedSystemId] = useState("");
  const [selectedProfileId, setSelectedProfileId] = useState("");
  const [selectedScanTypeId, setSelectedScanTypeId] = useState("");
  const [selectedScannerId, setSelectedScannerId] = useState("");
  const [selectedRun, setSelectedRun] = useState<ApiScannerRun | null>(null);
  const [isExecuting, setIsExecuting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [
          systemRecords,
          assessmentRecords,
          scannerRecords,
          scanTypeRecords,
          profileRecords,
          runRecords,
          findingRecords,
          evidenceRecords,
        ] = await Promise.all([
          apiClient.systems(),
          apiClient.assessments(),
          apiClient.scannerDefinitions(),
          apiClient.scanTypes(),
          apiClient.assessmentProfiles(),
          apiClient.scannerRuns(),
          apiClient.findings(),
          apiClient.evidence(),
        ]);
        setSystems(systemRecords);
        setAssessments(assessmentRecords);
        setScanners(scannerRecords);
        setScanTypes(scanTypeRecords);
        setProfiles(profileRecords);
        setRuns(runRecords);
        setFindings(findingRecords);
        setEvidence(evidenceRecords);
        setSelectedSystemId(systemRecords[0]?.id ?? "");
        setSelectedProfileId(profileRecords[0]?.id ?? "");
        setSelectedScanTypeId(scanTypeRecords[0]?.id ?? "");
        setSelectedScannerId(scannerRecords.find((scanner) => scanner.enabled)?.id ?? "");
        setSelectedRun(runRecords[0] ?? null);
      } catch (caught) {
        setError(caught instanceof Error ? caught.message : "Unable to load scanner data");
      }
    }
    void loadData();
  }, []);

  useEffect(() => {
    if (!selectedSystemId) return;
    async function loadRecommendations() {
      try {
        setRecommendations(await apiClient.recommendedScans(selectedSystemId, selectedProfileId));
      } catch (caught) {
        setError(caught instanceof Error ? caught.message : "Unable to load recommendations");
      }
    }
    void loadRecommendations();
  }, [selectedSystemId, selectedProfileId]);

  const selectedSystem = systems.find((system) => system.id === selectedSystemId);
  const selectedScanType = scanTypes.find((scanType) => scanType.id === selectedScanTypeId);
  const enabledScanners = useMemo(
    () => scanners.filter((scanner) => scanner.enabled),
    [scanners],
  );
  const compatibleScanners = useMemo(
    () =>
      selectedScanType
        ? enabledScanners.filter(
        (scanner) =>
          scanner.supported_scan_types.length === 0 ||
          scanner.supported_scan_types.includes(selectedScanType.name),
      )
        : enabledScanners,
    [enabledScanners, selectedScanType],
  );
  const selectedSystemAssessments = assessments.filter(
    (assessment) => assessment.system_id === selectedSystemId,
  );
  const latestAssessment = selectedSystemAssessments[0];
  const selectedRunFindings = selectedRun
    ? findings.filter(
        (finding) =>
          finding.scanner_name === selectedRun.scanner_name &&
          finding.assessment_id === selectedRun.assessment_id,
      )
    : [];
  const selectedRunEvidence = selectedRun
    ? evidence.filter((record) => record.metadata_json?.scanner_run_id === selectedRun.id)
    : [];
  const activeScannerId = compatibleScanners.some((scanner) => scanner.id === selectedScannerId)
    ? selectedScannerId
    : compatibleScanners[0]?.id;

  async function runMockAssessment() {
    if (!selectedSystemId || !activeScannerId || !selectedScanTypeId) return;
    setIsExecuting(true);
    setError(null);
    try {
      const created = await apiClient.createScannerRun({
        system_id: selectedSystemId,
        assessment_id: latestAssessment?.id,
        scanner_definition_id: activeScannerId,
        scan_type_id: selectedScanTypeId,
        assessment_profile_id: selectedProfileId || undefined,
        initiated_by: "frontend-operator",
      });
      const executed = await apiClient.executeScannerRun(created.id, "frontend-operator");
      const [runRecords, findingRecords, evidenceRecords] = await Promise.all([
        apiClient.scannerRuns(),
        apiClient.findings(),
        apiClient.evidence(),
      ]);
      setRuns(runRecords);
      setFindings(findingRecords);
      setEvidence(evidenceRecords);
      setSelectedRun(executed);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Mock scanner execution failed");
    } finally {
      setIsExecuting(false);
    }
  }

  return (
    <AppShell>
      <PageHeader
        title="Scanner Ecosystem"
        description="Operational scan registry, assessment profile controls, evidence-preserving mock execution, and normalized scanner findings."
        actions={<Radar className="size-6 text-cyan-100" aria-hidden="true" />}
      />

      {error ? (
        <div className="mb-4 rounded-lg border border-red-300/20 bg-red-300/10 p-3 text-sm text-red-100">
          {error}
        </div>
      ) : null}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <MetricCard
          label="Enabled scanners"
          value={enabledScanners.length}
          detail={`${scanners.length} registered assessment tools`}
          tone="neutral"
          badgeLabel="Phase 4"
        />
        <MetricCard
          label="Scan controls"
          value={scanTypes.filter((scanType) => scanType.enabled).length}
          detail="Active scan types across governance domains"
          tone="neutral"
          badgeLabel="Phase 4"
        />
        <MetricCard
          label="Profiles"
          value={profiles.filter((profile) => profile.enabled).length}
          detail="Assessment profiles available for operator selection"
          tone="neutral"
          badgeLabel="Phase 4"
        />
        <MetricCard
          label="Completed runs"
          value={runs.filter((run) => run.execution_status === "completed").length}
          detail="Scanner runs with preserved output"
          tone="good"
          badgeLabel="Phase 4"
        />
        <MetricCard
          label="Failed runs"
          value={runs.filter((run) => run.execution_status === "failed").length}
          detail="Visible execution failures"
          tone="warn"
          badgeLabel="Phase 4"
        />
      </div>

      <section className="mt-6 rounded-lg border border-white/10 bg-white/[0.045] p-4">
        <div className="grid gap-3 lg:grid-cols-[1fr_1fr_1fr_auto]">
          <label className="block">
            <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">System</span>
            <select
              value={selectedSystemId}
              onChange={(event) => setSelectedSystemId(event.target.value)}
              className="mt-2 h-10 w-full rounded-md border border-white/10 bg-black/30 px-3 text-sm text-zinc-100"
            >
              {systems.map((system) => (
                <option key={system.id} value={system.id}>
                  {system.system_name}
                </option>
              ))}
            </select>
          </label>
          <label className="block">
            <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Profile</span>
            <select
              value={selectedProfileId}
              onChange={(event) => setSelectedProfileId(event.target.value)}
              className="mt-2 h-10 w-full rounded-md border border-white/10 bg-black/30 px-3 text-sm text-zinc-100"
            >
              {profiles.map((profile) => (
                <option key={profile.id} value={profile.id}>
                  {profile.profile_name}
                </option>
              ))}
            </select>
          </label>
          <label className="block">
            <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Scan type</span>
            <select
              value={selectedScanTypeId}
              onChange={(event) => setSelectedScanTypeId(event.target.value)}
              className="mt-2 h-10 w-full rounded-md border border-white/10 bg-black/30 px-3 text-sm text-zinc-100"
            >
              {scanTypes.map((scanType) => (
                <option key={scanType.id} value={scanType.id}>
                  {scanType.display_name}
                </option>
              ))}
            </select>
          </label>
          <button
            type="button"
            onClick={runMockAssessment}
            disabled={isExecuting || !compatibleScanners.length}
            className="mt-6 inline-flex h-10 items-center justify-center gap-2 rounded-md border border-cyan-300/25 bg-cyan-300/10 px-4 text-sm font-medium text-cyan-50 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <Play className="size-4" aria-hidden="true" />
            {isExecuting ? "Running" : "Run Mock"}
          </button>
        </div>
        <div className="mt-3">
          <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Scanner</span>
          <div className="mt-2 flex flex-wrap gap-2">
            {compatibleScanners.map((scanner) => (
              <button
                key={scanner.id}
                type="button"
                onClick={() => setSelectedScannerId(scanner.id)}
                className={`rounded-md border px-3 py-2 text-sm ${
                  activeScannerId === scanner.id
                    ? "border-cyan-300/30 bg-cyan-300/10 text-cyan-50"
                    : "border-white/10 bg-black/20 text-zinc-300 hover:border-cyan-300/20"
                }`}
              >
                {scanner.display_name}
              </button>
            ))}
          </div>
        </div>
      </section>

      <div className="mt-6 grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="mb-4 flex items-center gap-2">
            <ShieldCheck className="size-5 text-emerald-100" aria-hidden="true" />
            <h2 className="text-base font-semibold text-zinc-50">Recommended Scans</h2>
          </div>
          <div className="space-y-3">
            {[...(recommendations?.required_scans ?? []), ...(recommendations?.optional_scans ?? [])]
              .slice(0, 8)
              .map((item) => (
                <div key={item.scan_type.id} className="rounded-lg border border-white/10 bg-black/20 p-3">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="font-medium text-zinc-100">{item.scan_type.display_name}</p>
                      <p className="mt-1 text-sm text-zinc-500">{item.reason}</p>
                    </div>
                    <span className="rounded-md border border-white/10 px-2 py-1 text-xs text-zinc-300">
                      {item.required ? "Required" : "Optional"}
                    </span>
                  </div>
                  <p className="mt-2 text-xs uppercase tracking-[0.08em] text-zinc-500">
                    {labelize(item.scan_type.domain)} · {item.available_scanners.length} enabled scanner
                  </p>
                </div>
              ))}
          </div>
        </section>

        <section>
          <TableShell label="Scanner runs">
            <TableHead>
              <tr>
                <Th>Run</Th>
                <Th>Status</Th>
                <Th>Findings</Th>
                <Th>Artifacts</Th>
              </tr>
            </TableHead>
            <tbody className="divide-y divide-white/10">
              {runs.slice(0, 8).map((run) => (
                <tr
                  key={run.id}
                  className="cursor-pointer hover:bg-white/[0.03]"
                  onClick={() => setSelectedRun(run)}
                >
                  <Td>
                    <p className="font-medium text-zinc-100">{labelize(run.scanner_name)}</p>
                    <p className="mt-1 font-mono text-xs text-zinc-500">{run.id.slice(0, 8)}</p>
                  </Td>
                  <Td>
                    <span className={`rounded-md border px-2 py-1 text-xs ${toneForStatus(run.execution_status)}`}>
                      {labelize(run.execution_status)}
                    </span>
                  </Td>
                  <Td>{run.finding_count}</Td>
                  <Td>
                    <div className="flex items-center gap-2 text-zinc-400">
                      <FileJson className="size-4" aria-hidden="true" />
                      <span>{run.raw_output_path ? "Preserved" : "Pending"}</span>
                    </div>
                  </Td>
                </tr>
              ))}
            </tbody>
          </TableShell>
        </section>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <div className="mb-4 flex items-center gap-2">
            <Activity className="size-5 text-cyan-100" aria-hidden="true" />
            <h2 className="text-base font-semibold text-zinc-50">Scanner Registry</h2>
          </div>
          <div className="grid gap-3 md:grid-cols-2">
            {scanners.slice(0, 8).map((scanner) => (
              <div key={scanner.id} className="rounded-lg border border-white/10 bg-black/20 p-3">
                <div className="flex items-start justify-between gap-3">
                  <p className="font-medium text-zinc-100">{scanner.display_name}</p>
                  {scanner.enabled ? (
                    <CheckCircle2 className="size-4 text-emerald-100" aria-hidden="true" />
                  ) : (
                    <TriangleAlert className="size-4 text-amber-100" aria-hidden="true" />
                  )}
                </div>
                <p className="mt-2 text-sm text-zinc-500">{labelize(scanner.scanner_category)}</p>
                <p className="mt-2 font-mono text-xs text-zinc-600">
                  {scanner.execution_mode} · {scanner.adapter_name}
                </p>
              </div>
            ))}
          </div>
        </section>

        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <h2 className="text-base font-semibold text-zinc-50">Run Detail</h2>
          {selectedRun ? (
            <div className="mt-4 space-y-4">
              <div className="grid gap-3 sm:grid-cols-2">
                <div className="rounded-lg border border-white/10 bg-black/20 p-3">
                  <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Status</p>
                  <p className="mt-2 text-sm text-zinc-100">{labelize(selectedRun.execution_status)}</p>
                </div>
                <div className="rounded-lg border border-white/10 bg-black/20 p-3">
                  <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">System</p>
                  <p className="mt-2 text-sm text-zinc-100">
                    {systems.find((system) => system.id === selectedRun.system_id)?.system_name ?? selectedSystem?.system_name}
                  </p>
                </div>
                <div className="rounded-lg border border-white/10 bg-black/20 p-3">
                  <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Raw output</p>
                  <p className="mt-2 break-all font-mono text-xs text-zinc-400">
                    {selectedRun.raw_output_path ?? "pending"}
                  </p>
                </div>
                <div className="rounded-lg border border-white/10 bg-black/20 p-3">
                  <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Log</p>
                  <p className="mt-2 break-all font-mono text-xs text-zinc-400">
                    {selectedRun.log_path ?? selectedRun.error_message ?? "pending"}
                  </p>
                </div>
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Normalized findings</p>
                <div className="mt-2 space-y-2">
                  {selectedRunFindings.slice(0, 4).map((finding) => (
                    <div key={finding.id} className="rounded-md border border-white/10 bg-black/20 p-3">
                      <p className="font-medium text-zinc-100">{finding.title}</p>
                      <p className="mt-1 text-sm text-zinc-500">
                        {labelize(finding.domain)} · {labelize(finding.severity)}
                      </p>
                    </div>
                  ))}
                  {!selectedRunFindings.length ? (
                    <p className="text-sm text-zinc-500">No normalized findings for this run.</p>
                  ) : null}
                </div>
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">Generated evidence</p>
                <p className="mt-2 text-sm text-zinc-300">{selectedRunEvidence.length} linked evidence records</p>
              </div>
            </div>
          ) : (
            <p className="mt-4 text-sm text-zinc-500">No scanner run selected.</p>
          )}
        </section>
      </div>
    </AppShell>
  );
}
