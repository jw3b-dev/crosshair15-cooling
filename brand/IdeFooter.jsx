// IdeFooter.jsx
// Copyright © 2026 John Wellard (jw3b.dev). All rights reserved.
// Brand asset — NOT covered by the repository MIT license. See brand/LICENSE-BRAND.md.
export const IdeFooter = () => {
  return (
    <footer className="h-6 w-full bg-slate-950 border-t border-slate-800 px-3 flex items-center justify-between text-xs font-mono text-slate-500">
      <div className="flex items-center gap-3">
        <span className="flex items-center gap-1 text-emerald-400">
          <span className="h-2 w-2 rounded-full bg-emerald-400 animate-ping" />
          KTHULHU_ORCHESTRATOR_ONLINE
        </span>
        <span>|</span>
        <span>ENV: PRODUCTION</span>
      </div>
      <div className="flex items-center gap-2 text-slate-400 hover:text-cyan-400 transition-colors">
        <span>// STAY WEIRD</span>
        <span className="text-sm">👽</span>
      </div>
    </footer>
  );
};
