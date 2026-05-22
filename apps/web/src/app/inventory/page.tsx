import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { TableHead, TableShell, Td, Th } from "@/components/data-table";
import { FilterBar } from "@/components/filter-bar";
import { PageHeader } from "@/components/page-header";
import { ScoreRing } from "@/components/score-ring";
import {
  ApprovalBadge,
  AssessmentBadge,
  ReviewStatusBadge,
  RiskTierBadge,
} from "@/components/status-badge";
import { formatDate, systems } from "@/lib/mock-data";

export default function InventoryPage() {
  return (
    <AppShell>
      <PageHeader
        title="AI Inventory"
        description="Registered county AI systems with owners, risk tier, assessment status, approval posture, and evidence readiness."
      />

      <FilterBar
        items={[
          "All systems",
          "High risk",
          "Public-facing",
          "Rights-impacting",
          "Evidence missing",
          "Approval blocked",
        ]}
      />

      <TableShell label="AI inventory">
        <TableHead>
          <tr>
            <Th>System</Th>
            <Th>Department</Th>
            <Th>Risk</Th>
            <Th>Approval</Th>
            <Th>Assessment</Th>
            <Th>Review</Th>
            <Th>Evidence</Th>
            <Th>Next review</Th>
          </tr>
        </TableHead>
        <tbody className="divide-y divide-white/10">
          {systems.map((system) => (
            <tr key={system.id} className="hover:bg-white/[0.035]">
              <Td>
                <div className="min-w-72">
                  <Link
                    href={`/systems/${system.id}`}
                    className="inline-flex items-center gap-1 font-medium text-zinc-50 hover:text-cyan-100"
                  >
                    {system.name}
                    <ArrowUpRight className="size-3.5" aria-hidden="true" />
                  </Link>
                  <p className="mt-1 text-sm leading-5 text-zinc-500">
                    {system.purpose}
                  </p>
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {system.dataTypes.map((type) => (
                      <span
                        key={type}
                        className="rounded-md border border-white/10 bg-black/20 px-2 py-1 text-xs text-zinc-400"
                      >
                        {type}
                      </span>
                    ))}
                  </div>
                </div>
              </Td>
              <Td>
                <p className="font-medium text-zinc-200">{system.department}</p>
                <p className="mt-1 text-sm text-zinc-500">{system.owner}</p>
              </Td>
              <Td>
                <div className="space-y-2">
                  <RiskTierBadge riskTier={system.riskTier} />
                  <ScoreRing score={system.riskScore} label="Score" />
                </div>
              </Td>
              <Td>
                <ApprovalBadge status={system.approvalStatus} />
                <p className="mt-2 text-sm text-zinc-500">{system.deploymentStatus}</p>
              </Td>
              <Td>
                <AssessmentBadge status={system.assessmentStatus} />
                <p className="mt-2 text-sm text-zinc-500">
                  Last assessed {formatDate(system.lastAssessed)}
                </p>
              </Td>
              <Td>
                <ReviewStatusBadge status={system.reviewStatus} />
              </Td>
              <Td>
                <span className="font-mono text-sm text-zinc-200">
                  {system.evidenceCompleteness}%
                </span>
              </Td>
              <Td>
                <span className="whitespace-nowrap text-sm text-zinc-300">
                  {formatDate(system.nextReview)}
                </span>
              </Td>
            </tr>
          ))}
        </tbody>
      </TableShell>
    </AppShell>
  );
}
