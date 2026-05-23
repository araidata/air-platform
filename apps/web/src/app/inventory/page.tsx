"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { Archive, Edit3, Plus, Save } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { TableHead, TableShell, Td, Th } from "@/components/data-table";
import { FilterBar } from "@/components/filter-bar";
import { PageHeader } from "@/components/page-header";
import { type ApiSystem, apiClient } from "@/lib/api-client";
import { formatDate, labelize, StatusPill } from "@/lib/format";

const emptyForm = {
  system_name: "",
  department_owner: "",
  business_purpose: "",
  public_facing: false,
  rights_impacting: false,
  safety_impacting: false,
  uses_pii: false,
  uses_phi: false,
  uses_cjis: false,
  model_provider: "",
  model_version: "",
  deployment_environment: "pilot",
  risk_tier: "moderate",
  approval_status: "pending",
  target_type: "web_chatbot",
  target_location: "",
  authentication_type: "none",
  authentication_reference: "",
  assessment_method: "hybrid",
  scanner_compatible: ["prompt_injection"],
  manual_review_only: false,
  uploaded_artifact_supported: true,
};

type SystemForm = typeof emptyForm;

const fromSystem = (system: ApiSystem): SystemForm => ({
  system_name: system.system_name,
  department_owner: system.department_owner,
  business_purpose: system.business_purpose,
  public_facing: system.public_facing,
  rights_impacting: system.rights_impacting,
  safety_impacting: system.safety_impacting,
  uses_pii: system.uses_pii,
  uses_phi: system.uses_phi,
  uses_cjis: system.uses_cjis,
  model_provider: system.model_provider ?? "",
  model_version: system.model_version ?? "",
  deployment_environment: system.deployment_environment,
  risk_tier: system.risk_tier,
  approval_status: system.approval_status,
  target_type: system.target_type,
  target_location: system.target_location,
  authentication_type: system.authentication_type,
  authentication_reference: system.authentication_reference ?? "",
  assessment_method: system.assessment_method,
  scanner_compatible: system.scanner_compatible ?? [],
  manual_review_only: system.manual_review_only,
  uploaded_artifact_supported: system.uploaded_artifact_supported,
});

const fieldClass =
  "mt-2 h-10 w-full rounded-md border border-white/10 bg-black/30 px-3 text-sm text-zinc-100";
const textAreaClass =
  "mt-2 min-h-24 w-full rounded-md border border-white/10 bg-black/30 px-3 py-2 text-sm text-zinc-100";

const targetTypes = [
  "web_chatbot",
  "rest_api",
  "rag_endpoint",
  "agent",
  "local_model",
  "vendor_ai",
  "uploaded_prompts",
  "uploaded_documents",
  "manual_review_only",
];

const authenticationTypes = ["none", "bearer_token", "api_key", "session_auth", "uploaded_credentials"];
const assessmentMethods = ["automated_scan", "manual_governance_review", "hybrid"];
const scannerCompatibilityOptions = [
  "garak",
  "prompt_injection",
  "jailbreak",
  "toxicity",
  "rag_integrity",
  "civil_rights",
  "manual_only",
];

export default function InventoryPage() {
  const [systems, setSystems] = useState<ApiSystem[]>([]);
  const [form, setForm] = useState<SystemForm>(emptyForm);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [activeFilter, setActiveFilter] = useState("All systems");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function loadSystems() {
    const records = await apiClient.systems();
    setSystems(records);
  }

  useEffect(() => {
    async function loadInitialSystems() {
      try {
        const records = await apiClient.systems();
        setSystems(records);
      } catch (caught) {
        setError(caught instanceof Error ? caught.message : "Unable to load systems");
      }
    }
    void loadInitialSystems();
  }, []);

  const visibleSystems = useMemo(() => {
    return systems.filter((system) => {
      if (activeFilter === "High risk") return ["high", "critical"].includes(system.risk_tier);
      if (activeFilter === "Public-facing") return system.public_facing;
      if (activeFilter === "Rights-impacting") return system.rights_impacting;
      if (activeFilter === "Approval blocked") return system.approval_status === "blocked";
      if (activeFilter === "Archived") return system.approval_status === "archived";
      return true;
    });
  }, [activeFilter, systems]);

  function updateForm<K extends keyof SystemForm>(key: K, value: SystemForm[K]) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  function startEdit(system: ApiSystem) {
    setEditingId(system.id);
    setForm(fromSystem(system));
    setMessage(`Editing ${system.system_name}`);
  }

  function resetForm() {
    setEditingId(null);
    setForm(emptyForm);
  }

  async function saveSystem() {
    setError(null);
    const payload = {
      ...form,
      model_provider: form.model_provider || null,
      model_version: form.model_version || null,
      authentication_reference: form.authentication_reference || null,
    };
    try {
      if (editingId) {
        await apiClient.updateSystem(editingId, payload);
        setMessage("System updated");
      } else {
        await apiClient.createSystem(payload);
        setMessage("System added");
      }
      resetForm();
      await loadSystems();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to save system");
    }
  }

  async function archiveSystem(system: ApiSystem) {
    setError(null);
    try {
      await apiClient.updateSystem(system.id, { approval_status: "archived" });
      setMessage(`${system.system_name} archived`);
      await loadSystems();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to archive system");
    }
  }

  function toggleScannerCompatibility(value: string) {
    setForm((current) => ({
      ...current,
      scanner_compatible: current.scanner_compatible.includes(value)
        ? current.scanner_compatible.filter((item) => item !== value)
        : [...current.scanner_compatible, value],
    }));
  }

  return (
    <AppShell>
      <PageHeader
        title="AI Inventory"
        description="Create, update, archive, and review county AI systems without leaving the operations UI."
        actions={
          <Link
            href="/workflows"
            className="inline-flex h-10 items-center gap-2 rounded-md border border-cyan-300/25 bg-cyan-300/10 px-3 text-sm font-medium text-cyan-50"
          >
            <Plus className="size-4" aria-hidden="true" />
            Start assessment
          </Link>
        }
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

      <section className="mb-6 rounded-lg border border-white/10 bg-white/[0.045] p-4">
        <div className="mb-4 flex items-center justify-between gap-3">
          <div>
            <h2 className="text-base font-semibold text-zinc-50">
              {editingId ? "Edit System" : "Add System"}
            </h2>
            <p className="mt-1 text-sm text-zinc-500">
              Capture ownership, deployment, risk tier, assessment target, scanner fit, and governance posture.
            </p>
          </div>
          {editingId ? (
            <button
              type="button"
              onClick={resetForm}
              className="rounded-md border border-white/10 px-3 py-2 text-sm text-zinc-300"
            >
              Cancel edit
            </button>
          ) : null}
        </div>
        <div className="grid gap-3 lg:grid-cols-3">
          <label>
            <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">System name</span>
            <input
              value={form.system_name}
              onChange={(event) => updateForm("system_name", event.target.value)}
              className={fieldClass}
            />
          </label>
          <label>
            <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Department / owner</span>
            <input
              value={form.department_owner}
              onChange={(event) => updateForm("department_owner", event.target.value)}
              className={fieldClass}
            />
          </label>
          <label>
            <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Deployment environment</span>
            <select
              value={form.deployment_environment}
              onChange={(event) => updateForm("deployment_environment", event.target.value)}
              className={fieldClass}
            >
              {["pilot", "production", "sandbox", "retired"].map((item) => (
                <option key={item} value={item}>
                  {labelize(item)}
                </option>
              ))}
            </select>
          </label>
          <label>
            <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Risk tier</span>
            <select
              value={form.risk_tier}
              onChange={(event) => updateForm("risk_tier", event.target.value)}
              className={fieldClass}
            >
              {["low", "moderate", "medium", "high", "critical"].map((item) => (
                <option key={item} value={item}>
                  {labelize(item)}
                </option>
              ))}
            </select>
          </label>
          <label>
            <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Approval status</span>
            <select
              value={form.approval_status}
              onChange={(event) => updateForm("approval_status", event.target.value)}
              className={fieldClass}
            >
              {["pending", "under_review", "approved", "approved_with_exception", "blocked", "archived"].map(
                (item) => (
                  <option key={item} value={item}>
                    {labelize(item)}
                  </option>
                ),
              )}
            </select>
          </label>
          <label>
            <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Model provider</span>
            <input
              value={form.model_provider}
              onChange={(event) => updateForm("model_provider", event.target.value)}
              className={fieldClass}
            />
          </label>
          <label>
            <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Model version</span>
            <input
              value={form.model_version}
              onChange={(event) => updateForm("model_version", event.target.value)}
              className={fieldClass}
            />
          </label>
          <label className="lg:col-span-2">
            <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Business purpose</span>
            <textarea
              value={form.business_purpose}
              onChange={(event) => updateForm("business_purpose", event.target.value)}
              className={textAreaClass}
            />
          </label>
        </div>
        <div className="mt-5 border-t border-white/10 pt-4">
          <h3 className="text-sm font-semibold text-zinc-100">Assessment Target</h3>
          <div className="mt-3 grid gap-3 lg:grid-cols-4">
            <label>
              <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Target type</span>
              <select
                value={form.target_type}
                onChange={(event) => updateForm("target_type", event.target.value)}
                className={fieldClass}
              >
                {targetTypes.map((item) => (
                  <option key={item} value={item}>
                    {labelize(item)}
                  </option>
                ))}
              </select>
            </label>
            <label className="lg:col-span-2">
              <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Target location</span>
              <input
                value={form.target_location}
                onChange={(event) => updateForm("target_location", event.target.value)}
                placeholder="https://chat.county.gov or uploaded prompts"
                className={fieldClass}
              />
            </label>
            <label>
              <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Authentication type</span>
              <select
                value={form.authentication_type}
                onChange={(event) => updateForm("authentication_type", event.target.value)}
                className={fieldClass}
              >
                {authenticationTypes.map((item) => (
                  <option key={item} value={item}>
                    {labelize(item)}
                  </option>
                ))}
              </select>
            </label>
            <label className="lg:col-span-2">
              <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Authentication reference</span>
              <input
                value={form.authentication_reference}
                onChange={(event) => updateForm("authentication_reference", event.target.value)}
                placeholder="Optional credential record or test account reference"
                className={fieldClass}
              />
            </label>
            <label>
              <span className="text-xs uppercase tracking-[0.08em] text-zinc-500">Assessment method</span>
              <select
                value={form.assessment_method}
                onChange={(event) => updateForm("assessment_method", event.target.value)}
                className={fieldClass}
              >
                {assessmentMethods.map((item) => (
                  <option key={item} value={item}>
                    {labelize(item)}
                  </option>
                ))}
              </select>
            </label>
          </div>
        </div>
        <div className="mt-5 border-t border-white/10 pt-4">
          <h3 className="text-sm font-semibold text-zinc-100">Scanner Compatibility</h3>
          <div className="mt-3 flex flex-wrap gap-2">
            {scannerCompatibilityOptions.map((item) => (
              <label
                key={item}
                className="inline-flex items-center gap-2 rounded-md border border-white/10 bg-black/20 px-3 py-2 text-sm text-zinc-300"
              >
                <input
                  type="checkbox"
                  checked={form.scanner_compatible.includes(item)}
                  onChange={() => toggleScannerCompatibility(item)}
                />
                {labelize(item)}
              </label>
            ))}
          </div>
        </div>
        <div className="mt-4 flex flex-wrap gap-3">
          {[
            ["public_facing", "Public-facing"],
            ["rights_impacting", "Rights-impacting"],
            ["safety_impacting", "Safety-impacting"],
            ["uses_pii", "PII"],
            ["uses_phi", "PHI"],
            ["uses_cjis", "CJIS"],
            ["manual_review_only", "Manual review only"],
            ["uploaded_artifact_supported", "Uploaded artifacts supported"],
          ].map(([key, label]) => (
            <label
              key={key}
              className="inline-flex items-center gap-2 rounded-md border border-white/10 bg-black/20 px-3 py-2 text-sm text-zinc-300"
            >
              <input
                type="checkbox"
                checked={Boolean(form[key as keyof SystemForm])}
                onChange={(event) =>
                  setForm((current) => ({ ...current, [key]: event.target.checked }))
                }
              />
              {label}
            </label>
          ))}
          <button
            type="button"
            onClick={saveSystem}
            disabled={!form.system_name || !form.department_owner || !form.business_purpose || !form.target_location}
            className="inline-flex h-10 items-center gap-2 rounded-md border border-cyan-300/25 bg-cyan-300/10 px-4 text-sm font-medium text-cyan-50 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <Save className="size-4" aria-hidden="true" />
            {editingId ? "Save changes" : "Add system"}
          </button>
        </div>
      </section>

      <FilterBar
        items={[
          "All systems",
          "High risk",
          "Public-facing",
          "Rights-impacting",
          "Approval blocked",
          "Archived",
        ]}
        activeItem={activeFilter}
        onChange={setActiveFilter}
      />

      <TableShell label="AI inventory management">
        <TableHead>
          <tr>
            <Th>System</Th>
            <Th>Owner</Th>
            <Th>Risk</Th>
            <Th>Governance Flags</Th>
            <Th>Approval</Th>
            <Th>Updated</Th>
            <Th>Actions</Th>
          </tr>
        </TableHead>
        <tbody className="divide-y divide-white/10">
          {visibleSystems.map((system) => (
            <tr key={system.id} className="hover:bg-white/[0.035]">
              <Td>
                <div className="min-w-80">
                  <Link
                    href={`/systems/${system.id}`}
                    className="font-medium text-zinc-50 hover:text-cyan-100"
                  >
                    {system.system_name}
                  </Link>
                  <p className="mt-1 text-sm leading-5 text-zinc-500">
                    {system.business_purpose}
                  </p>
                  <p className="mt-2 font-mono text-xs text-zinc-600">
                    {system.model_provider ?? "Provider not set"} / {system.model_version ?? "version not set"}
                  </p>
                  <p className="mt-1 font-mono text-xs text-cyan-100/70">
                    {labelize(system.target_type)} / {system.target_location}
                  </p>
                </div>
              </Td>
              <Td>{system.department_owner}</Td>
              <Td>
                <StatusPill value={system.risk_tier} />
              </Td>
              <Td>
                <div className="flex max-w-72 flex-wrap gap-1.5">
                  {[
                    system.public_facing && "Public",
                    system.rights_impacting && "Rights",
                    system.safety_impacting && "Safety",
                    system.uses_pii && "PII",
                    system.uses_phi && "PHI",
                    system.uses_cjis && "CJIS",
                  ]
                    .filter((flag): flag is string => Boolean(flag))
                    .map((flag) => (
                      <span
                        key={flag}
                        className="rounded-md border border-white/10 bg-black/20 px-2 py-1 text-xs text-zinc-300"
                      >
                        {flag}
                      </span>
                    ))}
                </div>
              </Td>
              <Td>
                <StatusPill value={system.approval_status} />
                <p className="mt-2 text-sm text-zinc-500">{labelize(system.deployment_environment)}</p>
                <p className="mt-1 text-xs text-zinc-500">{labelize(system.assessment_method)}</p>
              </Td>
              <Td>{formatDate(system.updated_at)}</Td>
              <Td>
                <div className="flex flex-wrap gap-2">
                  <button
                    type="button"
                    onClick={() => startEdit(system)}
                    className="inline-flex h-9 items-center gap-2 rounded-md border border-white/10 px-3 text-sm text-zinc-200"
                  >
                    <Edit3 className="size-4" aria-hidden="true" />
                    Edit
                  </button>
                  <button
                    type="button"
                    onClick={() => archiveSystem(system)}
                    className="inline-flex h-9 items-center gap-2 rounded-md border border-amber-300/20 px-3 text-sm text-amber-100"
                  >
                    <Archive className="size-4" aria-hidden="true" />
                    Archive
                  </button>
                </div>
              </Td>
            </tr>
          ))}
        </tbody>
      </TableShell>
    </AppShell>
  );
}
