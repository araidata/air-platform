import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { TableHead, TableShell, Td, Th } from "@/components/data-table";
import { FilterBar } from "@/components/filter-bar";
import { PageHeader } from "@/components/page-header";
import { EvidenceBadge } from "@/components/status-badge";
import {
  evidenceRecords,
  findings,
  formatDate,
  getSystemName,
} from "@/lib/mock-data";

export default function EvidencePage() {
  const auditPacketCount = evidenceRecords.filter((record) => record.auditPacket).length;
  const restrictedCount = evidenceRecords.filter(
    (record) => record.sensitivity === "Restricted",
  ).length;

  return (
    <AppShell>
      <PageHeader
        title="Evidence & Audit"
        description="Evidence library for raw outputs, assessments, policy records, decisions, retests, and audit packet inclusion."
      />

      <div className="mb-6 grid gap-4 md:grid-cols-3">
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">
            Evidence records
          </p>
          <p className="mt-2 font-mono text-3xl font-semibold text-zinc-50">
            {evidenceRecords.length}
          </p>
        </section>
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">
            Audit packet items
          </p>
          <p className="mt-2 font-mono text-3xl font-semibold text-emerald-100">
            {auditPacketCount}
          </p>
        </section>
        <section className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <p className="text-xs uppercase tracking-[0.08em] text-zinc-500">
            Restricted evidence
          </p>
          <p className="mt-2 font-mono text-3xl font-semibold text-red-100">
            {restrictedCount}
          </p>
        </section>
      </div>

      <FilterBar
        items={[
          "All evidence",
          "Audit packet",
          "Scanner output",
          "Retest",
          "Restricted",
          "Linked findings",
        ]}
      />

      <TableShell label="Evidence library">
        <TableHead>
          <tr>
            <Th>Evidence</Th>
            <Th>System</Th>
            <Th>Type</Th>
            <Th>Sensitivity</Th>
            <Th>Collected</Th>
            <Th>Audit</Th>
            <Th>Linked findings</Th>
          </tr>
        </TableHead>
        <tbody className="divide-y divide-white/10">
          {evidenceRecords.map((record) => (
            <tr key={record.id} className="hover:bg-white/[0.035]">
              <Td>
                <div className="min-w-80">
                  <p className="font-mono text-xs text-zinc-500">{record.id}</p>
                  <p className="mt-1 font-medium text-zinc-50">{record.title}</p>
                  <p className="mt-1 text-sm leading-5 text-zinc-500">
                    {record.summary}
                  </p>
                  <p className="mt-2 font-mono text-xs text-zinc-600">{record.hash}</p>
                </div>
              </Td>
              <Td>
                <Link
                  href={`/systems/${record.systemId}`}
                  className="font-medium text-cyan-100 hover:text-cyan-50"
                >
                  {getSystemName(record.systemId)}
                </Link>
                <p className="mt-1 text-sm text-zinc-500">{record.source}</p>
              </Td>
              <Td>
                <span className="whitespace-nowrap text-zinc-300">{record.type}</span>
              </Td>
              <Td>
                <span className="whitespace-nowrap text-zinc-300">
                  {record.sensitivity}
                </span>
              </Td>
              <Td>
                <span className="whitespace-nowrap text-zinc-300">
                  {formatDate(record.collectedAt)}
                </span>
              </Td>
              <Td>
                <EvidenceBadge record={record} />
              </Td>
              <Td>
                <div className="flex flex-wrap gap-1.5">
                  {record.linkedFindingIds.map((findingId) => (
                    <span
                      key={findingId}
                      className="rounded-md border border-white/10 bg-black/20 px-2 py-1 font-mono text-xs text-zinc-300"
                      title={
                        findings.find((finding) => finding.id === findingId)?.title
                      }
                    >
                      {findingId}
                    </span>
                  ))}
                </div>
              </Td>
            </tr>
          ))}
        </tbody>
      </TableShell>
    </AppShell>
  );
}
