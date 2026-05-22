import { Search, ShieldCheck } from "lucide-react";
import { Navigation } from "@/components/navigation";

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-[#0d1114] text-zinc-100">
      <div className="grid min-h-screen lg:grid-cols-[280px_1fr]">
        <aside className="border-b border-white/10 bg-[#0a0d10] px-4 py-4 lg:border-b-0 lg:border-r">
          <div className="mb-7 flex items-center gap-3">
            <div className="grid size-10 place-items-center rounded-md border border-cyan-300/20 bg-cyan-300/10 text-cyan-100">
              <ShieldCheck className="size-5" aria-hidden="true" />
            </div>
            <div>
              <p className="text-sm font-semibold text-zinc-50">
                County AI Assurance
              </p>
              <p className="text-xs text-zinc-500">Operations Center</p>
            </div>
          </div>
          <Navigation />
          <div className="mt-8 rounded-lg border border-white/10 bg-white/[0.04] p-3">
            <p className="text-xs font-medium uppercase tracking-[0.08em] text-zinc-500">
              Operating mode
            </p>
            <p className="mt-2 text-sm text-zinc-200">Phase 6 civil-rights workflow</p>
            <p className="mt-1 text-xs leading-5 text-zinc-500">
              Evidence-backed fairness, language access, and appeal-path review.
            </p>
          </div>
        </aside>
        <div className="min-w-0">
          <header className="sticky top-0 z-20 border-b border-white/10 bg-[#0d1114]/95 px-4 py-3 backdrop-blur md:px-6">
            <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <div>
                <p className="text-xs font-medium uppercase tracking-[0.1em] text-zinc-500">
                  Internal governance workspace
                </p>
                <p className="mt-1 text-sm text-zinc-300">
                  Findings, evidence, assessments, and AI Review Board workflow
                </p>
              </div>
              <div className="flex items-center gap-3">
                <div className="hidden h-9 min-w-72 items-center gap-2 rounded-md border border-white/10 bg-white/[0.045] px-3 text-sm text-zinc-500 md:flex">
                  <Search className="size-4" aria-hidden="true" />
                  <span>Search systems, findings, evidence</span>
                </div>
                <div className="rounded-md border border-emerald-300/20 bg-emerald-300/10 px-3 py-2 text-xs font-medium text-emerald-100">
                  Local operational runtime
                </div>
              </div>
            </div>
          </header>
          <main className="px-4 py-6 md:px-6 lg:px-8">{children}</main>
        </div>
      </div>
    </div>
  );
}
