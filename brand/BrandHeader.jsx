// BrandHeader.jsx
// Copyright © 2026 John Wellard (jw3b.dev). All rights reserved.
// Brand asset — NOT covered by the repository MIT license. See brand/LICENSE-BRAND.md.
export const BrandHeader = ({ mode = "full" }) => {
  return (
    <div className="font-mono flex items-center gap-2 select-none">
      {mode === "full" ? (
        <span className="text-emerald-400 font-bold tracking-tight">
          ~❯ <span className="text-slate-100">JW</span>
          <span className="text-cyan-400">3</span>
          <span className="text-slate-100">B</span>
          <span className="text-cyan-400">.</span>
          <span className="animate-pulse text-emerald-400">_</span>
        </span>
      ) : (
        <span className="text-slate-100 font-bold tracking-tight">
          JW<span className="text-cyan-400">3</span>B<span className="text-cyan-400">.</span>
        </span>
      )}
    </div>
  );
};
