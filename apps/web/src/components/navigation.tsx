"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  ClipboardList,
  BarChart3,
  Database,
  FileSearch,
  Gauge,
  Library,
  Languages,
  ListChecks,
  Radar,
  Scale,
} from "lucide-react";

const navItems = [
  { href: "/", label: "Executive Dashboard", icon: Gauge },
  { href: "/workflows", label: "Guided Workflow", icon: ListChecks },
  { href: "/inventory", label: "AI Inventory", icon: Database },
  { href: "/findings", label: "Findings Queue", icon: ClipboardList },
  { href: "/systems/public-benefits-chatbot", label: "System Detail", icon: FileSearch },
  { href: "/evidence", label: "Evidence & Audit", icon: Library },
  { href: "/scanners", label: "Scanner Runs", icon: Radar },
  { href: "/civil-rights", label: "Civil Rights Review", icon: Languages },
  { href: "/review-board", label: "AI Review Board", icon: Scale },
  { href: "/reports", label: "Reports", icon: BarChart3 },
];

export function Navigation() {
  const pathname = usePathname();

  return (
    <nav className="space-y-1" aria-label="Primary navigation">
      {navItems.map((item) => {
        const Icon = item.icon;
        const isActive =
          pathname === item.href ||
          (item.href !== "/" && pathname.startsWith(item.href)) ||
          (item.href.startsWith("/systems") && pathname.startsWith("/systems"));

        return (
          <Link
            key={item.href}
            href={item.href}
            className={`flex min-h-10 items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors ${
              isActive
                ? "border border-cyan-300/20 bg-cyan-300/10 text-cyan-50"
                : "text-zinc-400 hover:bg-white/[0.06] hover:text-zinc-100"
            }`}
          >
            <Icon className="size-4 shrink-0" aria-hidden="true" />
            <span>{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
