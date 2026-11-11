"""Scan für H14: starker Open-Interest-Aufbau bei Seitwärtskurs, dann Trade in Richtung des Ausbruchs aus der 24-h-Range.

Aufruf:  python -m scan.oi_kaskade_scan        (braucht data/raw/PF_XBTUSD_oi.parquet, In-Sample bis OOS_START)

Regeln laut Laborbuch. Einstieg per Stop-Market am Range-Rand (Fill zum Level oder bei Lücke zum Minuten-Open),
SL in der Range-Mitte, Ziel eine Range-Höhe jenseits des Ausbruchslevels, Zeitstopp 24 h, ein Setup zur Zeit.
"""
import numpy as np
import pandas as pd

from lab.config import MAKER_FEE, RAW_DIR, SYMBOL, TAKER_FEE
from lab.data import load_1m
from lab.report import add_funding, summary
from scan.minuten_sim import ausstieg

T_GRENZE = 2.24
TAG = 1440


def merkmale(df: pd.DataFrame) -> pd.DataFrame:
    """Je volle Stunde t: z_OI und z_Preis, nur aus Daten vor t."""
    ts = df.ts_open.to_numpy(np.int64)
    m = ts % 3_600_000 == 0
    p = pd.Series(df.open.to_numpy(float)[m], index=ts[m])
    r1 = p.pct_change()
    sig1 = r1.rolling(720).std().shift(24)
    z_p = (p / p.shift(24) - 1) / (sig1 * np.sqrt(24))
    oi = pd.read_parquet(RAW_DIR / f"{SYMBOL}_oi.parquet").set_index("ts").oi_close
    oi_vor = oi.reindex(p.index - 3_600_000).to_numpy()          # OI-Schluss der Stunde vor t
    d_oi = pd.Series(oi_vor, index=p.index) / pd.Series(oi.reindex(p.index - 25 * 3_600_000).to_numpy(), index=p.index) - 1
    z_oi = (d_oi - d_oi.rolling(720).mean().shift(1)) / d_oi.rolling(720).std().shift(1)
    return pd.DataFrame(dict(z_p=z_p, z_oi=z_oi)).dropna()


def simulieren(df: pd.DataFrame, setups: np.ndarray) -> pd.DataFrame:
    ts = df.ts_open.to_numpy(np.int64)
    o, h, l, c = (df[x].to_numpy(float) for x in ("open", "high", "low", "close"))
    t0 = ts[0]
    frei_ab = 0
    rows = []
    for t in setups:
        m0 = int((t - t0) // 60_000)
        if m0 < frei_ab or m0 < TAG or m0 + TAG >= len(o):
            continue
        RH, RL = h[m0 - TAG:m0].max(), l[m0 - TAG:m0].min()
        mitte, hoehe = (RH + RL) / 2, RH - RL
        i_aus = None
        for i in range(m0, m0 + TAG):
            hoch, tief = h[i] > RH, l[i] < RL
            if hoch and tief:
                i_aus = None
                frei_ab = i + 1
                break
            if hoch or tief:
                s = 1 if hoch else -1
                e = max(RH, o[i]) if s > 0 else min(RL, o[i])
                tp = RH + hoehe if s > 0 else RL - hoehe
                xi, x, art = ausstieg(o, h, l, c, i, s, mitte, tp, i + TAG)
                rows.append(dict(i=i, xi=xi, s=s, e=e, x=x, art=art, sl=mitte, tp=tp))
                frei_ab = xi + 1
                i_aus = i
                break
        else:
            frei_ab = m0 + TAG
    r = pd.DataFrame(rows)
    return r


def trades(r: pd.DataFrame, ts) -> pd.DataFrame:
    risk = (r.e - r.sl).abs()
    brutto = r.s * (r.x - r.e)
    fee = r.e * TAKER_FEE + r.x * np.where(r.art == 1, MAKER_FEE, TAKER_FEE)
    t = pd.DataFrame(dict(ts_open=ts[r.i] * 1_000_000, ts_close=(ts[r.xi] + 60_000) * 1_000_000,
                          side=np.where(r.s > 0, "long", "short"), entry=r.e, exit=r.x, risk_px=risk,
                          exit_reason=np.where(r.art == 1, "tp", np.where(r.art == -1, "sl", "zeit")),
                          r_gross=brutto / risk, r_net=(brutto - fee) / risk, pct_net=(brutto - fee) / r.e * 100))
    return add_funding(t)


def zufall(df: pd.DataFrame, r: pd.DataFrame, rng) -> float:
    """Gleiche Einstiegsminuten und Abstände, zufällige Richtung."""
    o, h, l, c = (df[x].to_numpy(float) for x in ("open", "high", "low", "close"))
    ts = df.ts_open.to_numpy(np.int64)
    rows = []
    for z in r.itertuples():
        s = rng.choice([-1, 1])
        d_sl, d_tp = abs(z.e - z.sl), abs(z.tp - z.e)
        sl, tp = z.e - s * d_sl, z.e + s * d_tp
        xi, x, art = ausstieg(o, h, l, c, z.i, s, sl, tp, z.i + TAG)
        rows.append(dict(i=z.i, xi=xi, s=s, e=z.e, x=x, art=art, sl=sl, tp=tp))
    return trades(pd.DataFrame(rows), ts).r_net.mean()


def kennzahlen(t: pd.DataFrame) -> dict:
    s = summary(t)
    s.update(long_anteil=float((t.side == "long").mean()), h_mittel=float(((t.ts_close - t.ts_open) / 3.6e12).mean()))
    return s


if __name__ == "__main__":
    pd.set_option("display.width", 250)
    df = load_1m()
    ts = df.ts_open.to_numpy(np.int64)
    mk = merkmale(df)
    seitwaerts = mk.z_p.abs() <= 1
    h14 = trades(simulieren(df, mk.index[(mk.z_oi >= 2) & seitwaerts].to_numpy()), ts)
    ohne = trades(simulieren(df, mk.index[seitwaerts].to_numpy()), ts)
    print(f"H14 ab {pd.to_datetime(mk.index[0], unit='ms')}, Setup-Stunden mit z_OI ≥ 2 und seitwärts: "
          f"{int(((mk.z_oi >= 2) & seitwaerts).sum())}")
    print(pd.DataFrame([dict(regel="H14 (mit OI)", **kennzahlen(h14)),
                        dict(regel="Kontrolle ohne OI", **kennzahlen(ohne))]).round(3).to_string(index=False))

    r14 = simulieren(df, mk.index[(mk.z_oi >= 2) & seitwaerts].to_numpy())
    rng = np.random.default_rng(42)
    werte = np.array([zufall(df, r14, rng) for _ in range(1000)])
    print(f"Zufallsrichtung, 1.000 Läufe: Mittel R netto {werte.mean():.4f}, 95-%-Quantil {np.quantile(werte, 0.95):.4f}, "
          f"H14 {h14.r_net.mean():.4f}, Anteil Läufe ≥ H14 {(werte >= h14.r_net.mean()).mean():.3f}")

    f = pd.read_parquet(RAW_DIR / f"{SYMBOL}_funding.parquet").set_index("ts").rate_rel
    st = (h14.ts_open // 1_000_000 // 3_600_000 * 3_600_000)
    h14["funding"] = f.reindex(st.to_numpy()).to_numpy()
    teil = h14.dropna(subset=["funding"])
    if len(teil):
        g = teil.groupby([teil.side, np.where(teil.funding > 0, "Funding positiv", "Funding ≤ 0")]).r_net.agg(["size", "mean"])
        print("\nab 2025-10 nach Funding beim Einstieg (beschreibend)\n" + g.round(3).to_string())
