import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { TableHead, TableShell, Td, Th } from "@/components/data-table";
import { FilterBar } from "@/components/filter-bar";
import { PageHeader } from "@/components/page-header";
import {
  FindingStatusBadge,
  SeverityBadge,
} from "@/components/status-badge";
import { findings, formatDate, getSystemName } from "@/lib/mock-data";

export default function FindingsPage() {
  const activeFindings = findings
    .filter((finding) => finding.status !== "Closed")
    .sort((a, b) => a.dueDate.localeCompare(b.dueDate));

  return (
    <AppShell>
      <PageHeader
        title="Findings Queue"
        description="Operational queue for triage, assignment, remediation, risk acceptance, retesting, and closure."
      />

      <FilterBar
        items={[
          "Open findings",
          "Critical",
          "Retest required",
          "Evidence missing",
          "Civil rights",
          "Security",
          "Overdue soon",
        ]}
      />

      <TableShell label="Findings queue">
        <TableHead>
          <tr>
            <Th>Finding</Th>
            <Th>System</Th>
            <Th>Severity</Th>
            <Th>Status</Th>
            <Th>Owner</Th>
            <Th>Due</Th>
            <Th>Domain</Th>
            <Th>Impact</Th>
          </tr>
        </TableHead>
        <tbody className="divide-y divide-white/10">
          {activeFindings.map((finding) => (
            <tr key={finding.id} className="hover:bg-white/[0.035]">
              <Td>
                <div className="min-w-80">
                  <p className="font-mono text-xs text-zinc-500">{finding.id}</p>
                  <p className="mt-1 font-medium text-zinc-50">{finding.title}</p>
                  <p className="mt-1 text-sm leading-5 text-zinc-500">
                    {finding.summary}
                  </p>
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {finding.frameworkMappings.map((mapping) => (
                      <span
                        key={mapping}
                        className="rounded-md border border-white/10 bg-black/20 px-2 py-1 text-xs text-zinc-400"
                      >
                        {mapping}
                      </span>
                    ))}
                  </div>
                </div>
              </Td>
              <Td>
                <Link
                  href={`/systems/${finding.systemId}`}
                  className="font-medium text-cyan-100 hover:text-cyan-50"
                >
                  {getSystemName(finding.systemId)}
                </Link>
              </Td>
              <Td>
                <SeverityBadge severity={finding.severity} />
              </Td>
              <Td>
                <FindingStatusBadge status={finding.status} />
              </Td>
              <Td>
                <span className="whitespace-nowrap text-zinc-300">{finding.owner}</span>
              </Td>
              <Td>
                <span className="whitespace-nowrap text-zinc-300">
                  {formatDate(finding.dueDate)}
                </span>
              </Td>
              <Td>
                <span className="whitespace-nowrap text-zinc-300">
                  {finding.domain}
                </span>
              </Td>
              <Td>
                <span className="font-mono text-red-100">{finding.scoreImpact}</span>
              </Td>
            </tr>
          ))}
        </tbody>
      </TableShell>
    </AppShell>
  );
}
