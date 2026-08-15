import { CheckCircle2, TrendingUp, DollarSign, Beaker } from "lucide-react";

const INK = "#1c2a3a";
const GOOD = "#3b7a6b";
const MUTE = "#8a94a3";
const ACCENT = "#c65d3b";

function StatCard({ icon: Icon, label, value, sub }) {
  return (
    <div style={{ background: "#fff", borderRadius: 10, padding: "18px 20px", border: "1px solid #e7e5df", flex: 1, minWidth: 150 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10 }}>
        <Icon size={16} color={GOOD} strokeWidth={2.25} />
        <span style={{ fontSize: 12, color: MUTE, letterSpacing: "0.04em", textTransform: "uppercase", fontWeight: 600 }}>{label}</span>
      </div>
      <div style={{ fontSize: 24, fontWeight: 700, color: INK, fontFamily: "'IBM Plex Mono', monospace" }}>{value}</div>
      <div style={{ fontSize: 12.5, color: MUTE, marginTop: 4 }}>{sub}</div>
    </div>
  );
}

function ConversionBar({ label, value, n, isControl }) {
  const pct = (value * 100).toFixed(2);
  return (
    <div style={{ marginBottom: 14 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12.5, marginBottom: 5 }}>
        <span style={{ fontWeight: 600, color: INK }}>{label} {isControl && <span style={{ color: MUTE, fontWeight: 400 }}>(control)</span>}</span>
        <span style={{ color: MUTE, fontFamily: "'IBM Plex Mono', monospace" }}>{pct}% (n={n.toLocaleString()})</span>
      </div>
      <div style={{ background: "#eee", borderRadius: 6, height: 20, overflow: "hidden" }}>
        <div style={{ width: `${(value / 0.16) * 100}%`, height: "100%", background: isControl ? MUTE : GOOD, borderRadius: 6 }} />
      </div>
    </div>
  );
}

export default function ABTestDashboard() {
  return (
    <div style={{ fontFamily: "'Inter', -apple-system, sans-serif", background: "#f6f4ef", padding: 24, borderRadius: 12, maxWidth: 720, margin: "0 auto" }}>
      <div style={{ marginBottom: 20 }}>
        <div style={{ fontSize: 11, fontWeight: 700, color: ACCENT, letterSpacing: "0.08em", textTransform: "uppercase" }}>Experiment Results</div>
        <h2 style={{ margin: "4px 0 2px", fontSize: 22, color: INK, fontWeight: 700 }}>Checkout Redesign A/B Test</h2>
        <div style={{ fontSize: 13, color: MUTE }}>9,200 users · 2 variants · 30-day test window</div>
      </div>

      <div style={{ display: "flex", gap: 12, marginBottom: 20, flexWrap: "wrap" }}>
        <StatCard icon={TrendingUp} label="Observed lift" value="+2.02 pts" sub="12.20% → 14.22% conversion" />
        <StatCard icon={Beaker} label="p-value" value="0.0042" sub="significant at α=0.05" />
        <StatCard icon={CheckCircle2} label="95% CI on lift" value="[+0.6%, +3.4%]" sub="entirely positive → real effect" />
        <StatCard icon={DollarSign} label="Est. annual impact" value="$2.18M" sub="projected incremental revenue" />
      </div>

      <div style={{ background: "#fff", borderRadius: 10, border: "1px solid #e7e5df", padding: "18px 20px", marginBottom: 16 }}>
        <div style={{ fontSize: 13.5, fontWeight: 600, color: INK, marginBottom: 14 }}>Conversion rate by variant</div>
        <ConversionBar label="Variant A — current checkout" value={0.1220} n={4600} isControl />
        <ConversionBar label="Variant B — redesigned checkout" value={0.1422} n={4600} />
      </div>

      <div style={{ background: "#fff", borderRadius: 10, border: "1px solid #e7e5df", padding: "18px 20px", marginBottom: 16 }}>
        <div style={{ fontSize: 13.5, fontWeight: 600, color: INK, marginBottom: 12 }}>Segment consistency check</div>
        <div style={{ display: "flex", gap: 24 }}>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 12, color: MUTE, marginBottom: 4 }}>Mobile</div>
            <div style={{ fontSize: 18, fontWeight: 700, color: GOOD, fontFamily: "'IBM Plex Mono', monospace" }}>+2.11 pts</div>
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 12, color: MUTE, marginBottom: 4 }}>Desktop</div>
            <div style={{ fontSize: 18, fontWeight: 700, color: GOOD, fontFamily: "'IBM Plex Mono', monospace" }}>+1.85 pts</div>
          </div>
        </div>
        <div style={{ fontSize: 12, color: MUTE, marginTop: 10 }}>Lift holds across both device segments — not driven by one group masking a loss in another.</div>
      </div>

      <div style={{ background: INK, borderRadius: 10, padding: "16px 20px", color: "#fff" }}>
        <div style={{ fontSize: 12, letterSpacing: "0.04em", textTransform: "uppercase", color: "#a8b3c2", marginBottom: 6, fontWeight: 600 }}>Recommendation</div>
        <div style={{ fontSize: 14, lineHeight: 1.5 }}>
          Ship Variant B. The lift is statistically significant, the confidence interval is
          entirely positive, and the effect holds consistently across mobile and desktop.
        </div>
      </div>
    </div>
  );
}
