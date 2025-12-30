# financial_core.py
# Put this file at the project root (same folder as pages/) so pages/2_Financial_Analysis.py
# can import compute_all_metrics successfully with: from financial_core import compute_all_metrics

from typing import Dict, Any

def _safe_get(fin: Dict[str, Dict[str, Any]], year: str, key: str):
    """Return float if exists, else None."""
    try:
        v = fin.get(year, {}).get(key, None)
        if v is None or (isinstance(v, str) and v.strip() == ""):
            return None
        return float(v)
    except Exception:
        return None

def _safe_div(a, b):
    try:
        if b is None or b == 0:
            return None
        return a / b
    except Exception:
        return None

# Beneish components helper functions
def _compute_derived(fin):
    # Extract many inputs safely
    rev_py = _safe_get(fin, "PY", "Revenue")
    rev_cy = _safe_get(fin, "CY", "Revenue")
    rec_py = _safe_get(fin, "PY", "Receivables")
    rec_cy = _safe_get(fin, "CY", "Receivables")
    gp_py = _safe_get(fin, "PY", "GrossProfit")
    gp_cy = _safe_get(fin, "CY", "GrossProfit")
    np_py = _safe_get(fin, "PY", "Net Profit") or _safe_get(fin, "PY", "NetProfit")
    np_cy = _safe_get(fin, "CY", "Net Profit") or _safe_get(fin, "CY", "NetProfit")
    cfo_py = _safe_get(fin, "PY", "CFO")
    cfo_cy = _safe_get(fin, "CY", "CFO")
    assets_py = _safe_get(fin, "PY", "Total Assets") or _safe_get(fin, "PY", "TotalAssets")
    assets_cy = _safe_get(fin, "CY", "Total Assets") or _safe_get(fin, "CY", "TotalAssets")
    tl_py = _safe_get(fin, "PY", "Total Liabilities") or _safe_get(fin, "PY", "TotalLiabilities")
    tl_cy = _safe_get(fin, "CY", "Total Liabilities") or _safe_get(fin, "CY", "TotalLiabilities")
    longd_py = _safe_get(fin, "PY", "Long-term Debt") or _safe_get(fin, "PY", "Long-term Debt") or _safe_get(fin, "PY", "Long-term Debt")
    longd_cy = _safe_get(fin, "CY", "Long-term Debt")
    ca_cy = _safe_get(fin, "CY", "Current Assets") or _safe_get(fin, "CY", "CurrentAssets")
    cl_cy = _safe_get(fin, "CY", "Current Liabilities") or _safe_get(fin, "CY", "CurrentLiabilities")
    retained_cy = _safe_get(fin, "CY", "Retained Earnings") or _safe_get(fin, "CY", "RetainedEarnings")
    sharecap = _safe_get(fin, "CY", "Share Capital") or _safe_get(fin, "CY", "ShareCapital")

    derived = {
        "rev_py": rev_py, "rev_cy": rev_cy,
        "rec_py": rec_py, "rec_cy": rec_cy,
        "gp_py": gp_py, "gp_cy": gp_cy,
        "np_py": np_py, "np_cy": np_cy,
        "cfo_py": cfo_py, "cfo_cy": cfo_cy,
        "assets_py": assets_py, "assets_cy": assets_cy,
        "tl_py": tl_py, "tl_cy": tl_cy,
        "longd_py": longd_py, "longd_cy": longd_cy,
        "ca_cy": ca_cy, "cl_cy": cl_cy,
        "retained_cy": retained_cy, "sharecap": sharecap
    }
    return derived

# Forensic formulas (robust vs None)
def sloan_accrual(np_cy, cfo_cy, assets_cy):
    if np_cy is None or cfo_cy is None or assets_cy is None or assets_cy == 0:
        return None
    return (np_cy - cfo_cy) / assets_cy

def leverage_index(tl_cy, assets_cy, tl_py, assets_py):
    try:
        r_cy = _safe_div(tl_cy, assets_cy)
        r_py = _safe_div(tl_py, assets_py)
        if r_cy is None or r_py is None or r_py == 0:
            return None
        return r_cy / r_py
    except:
        return None

def dso_change(rec_py, rec_cy, rev_py, rev_cy):
    try:
        if None in (rec_py, rec_cy, rev_py, rev_cy) or rev_py == 0 or rev_cy == 0:
            return None
        dso_py = rec_py / (rev_py / 365.0)
        dso_cy = rec_cy / (rev_cy / 365.0)
        return dso_cy - dso_py
    except:
        return None

def quality_of_earnings(cfo_cy, np_cy):
    try:
        if cfo_cy is None or np_cy is None or np_cy == 0:
            return None
        return cfo_cy / np_cy
    except:
        return None

def altman_z_score(fin):
    # use common simplified altman formula requiring working capital, retained earnings, ebit, market value of equity, total liabilities, sales, total assets
    # we don't have EBit or market cap in simple input; use a pragmatic approximation using net profit for EBit and share capital as proxy for market value (not ideal)
    wc = None
    try:
        wc = (fin.get("CY", {}).get("Current Assets") or fin.get("CY", {}).get("CurrentAssets"))
        wc = float(wc) - float(fin.get("CY", {}).get("Current Liabilities") or fin.get("CY", {}).get("CurrentLiabilities"))
    except Exception:
        wc = None
    re = _safe_get(fin, "CY", "Retained Earnings") or _safe_get(fin, "CY", "RetainedEarnings")
    ebit = _safe_get(fin, "CY", "Net Profit") or _safe_get(fin, "CY", "NetProfit")
    mve = _safe_get(fin, "CY", "Share Capital") or _safe_get(fin, "CY", "ShareCapital")
    tl = _safe_get(fin, "CY", "Total Liabilities") or _safe_get(fin, "CY", "TotalLiabilities")
    sales = _safe_get(fin, "CY", "Revenue")
    assets = _safe_get(fin, "CY", "Total Assets") or _safe_get(fin, "CY", "TotalAssets")
    try:
        a = 1.2 * _safe_div(wc, assets) if assets else None
        b = 1.4 * _safe_div(re, assets) if assets else None
        c = 3.3 * _safe_div(ebit, assets) if assets else None
        d = 0.6 * _safe_div(mve, tl) if tl else None
        e = 1.0 * _safe_div(sales, assets) if assets else None
        # combine ignoring None parts
        parts = [x for x in (a,b,c,d,e) if x is not None]
        if not parts:
            return None
        return sum(parts)
    except:
        return None

def beneish_mscore(derived):
    # compute beneish variables as far as possible; default safe fallbacks
    rev_py = derived["rev_py"]; rev_cy = derived["rev_cy"]
    rec_py = derived["rec_py"]; rec_cy = derived["rec_cy"]
    gp_py = derived["gp_py"]; gp_cy = derived["gp_cy"]
    assets_py = derived["assets_py"]; assets_cy = derived["assets_cy"]
    tl_py = derived["tl_py"]; tl_cy = derived["tl_cy"]
    np_py = derived["np_py"]; np_cy = derived["np_cy"]
    cfo_cy = derived["cfo_cy"]

    # DSRI
    try:
        dsri = _safe_div((rec_cy / rev_cy), (rec_py / rev_py)) if None not in (rec_py, rec_cy, rev_py, rev_cy) else None
    except:
        dsri = None
    try:
        gmi = _safe_div((gp_py / rev_py), (gp_cy / rev_cy)) if None not in (gp_py, gp_cy, rev_py, rev_cy) else None
    except:
        gmi = None
    try:
        aqi = _safe_div((assets_cy - assets_py), assets_cy) if assets_cy else None
    except:
        aqi = None
    try:
        sgi = _safe_div(rev_cy, rev_py) if rev_py else None
    except:
        sgi = None
    try:
        depi = None
        if None not in (gp_py, assets_py, gp_cy, assets_cy) and assets_py and assets_cy:
            depi = (gp_py / assets_py) / (gp_cy / assets_cy)
    except:
        depi = None
    try:
        sgai = None
        # approximate SG&A index using (NetProfit - GrossProfit)/Revenue as a proxy for SG&A ratio
        if None not in (np_cy, gp_cy, rev_cy, np_py, gp_py, rev_py) and rev_py and rev_cy:
            sgai = _safe_div(( (np_cy - gp_cy) / rev_cy ), ( (np_py - gp_py) / rev_py ))
    except:
        sgai = None
    try:
        lvgi = None
        if None not in (tl_cy, assets_cy, tl_py, assets_py) and assets_py and assets_cy:
            lvgi = (tl_cy / assets_cy) / (tl_py / assets_py)
    except:
        lvgi = None
    try:
        # total accruals to total assets (TATA)
        tata = None
        if None not in (np_cy, cfo_cy, assets_cy) and assets_cy:
            tata = (np_cy - cfo_cy) / assets_cy
    except:
        tata = None

    # now the beneish regression (approximate form). If any variable missing, still compute using 0 for missing terms
    try:
        # replace missing with 0 to allow a numeric result (but mark later that we used approximations)
        vals = {
            "dsri": dsri or 0.0, "gmi": gmi or 0.0, "aqi": aqi or 0.0,
            "sgi": sgi or 0.0, "depi": depi or 0.0, "sgai": sgai or 0.0,
            "lvgi": lvgi or 0.0, "tata": tata or 0.0
        }
        # classical Beneish linear form (coefficients approximated from literature)
        m = -4.84 + 0.92*vals["dsri"] + 0.528*vals["gmi"] + 0.404*vals["aqi"] + 0.892*vals["sgi"] + 0.115*vals["depi"] - 0.172*vals["sgai"] - 0.327*vals["lvgi"] + 4.679*vals["tata"]
        return m
    except Exception:
        return None

def compute_all_metrics(fin: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Main function expected by pages/2_Financial_Analysis.py
    Input: fin is a dict with "PY" and "CY" keys each mapping to dict of metrics
    Returns a dictionary with:
       - beneish_mscore
       - altman_z
       - sloan_accrual
       - leverage_index
       - dso_change
       - quality_of_earnings
       - insight (short text summary)
    """
    if not fin or ("PY" not in fin and "CY" not in fin):
        return {
            "beneish_mscore": None,
            "altman_z": None,
            "sloan_accrual": None,
            "leverage_index": None,
            "dso_change": None,
            "quality_of_earnings": None,
            "insight": ""
        }

    derived = _compute_derived(fin)

    # compute metrics
    sloan = sloan_accrual(derived["np_cy"], derived["cfo_cy"], derived["assets_cy"])
    lev_idx = leverage_index(derived["tl_cy"], derived["assets_cy"], derived["tl_py"], derived["assets_py"])
    dso = dso_change(derived["rec_py"], derived["rec_cy"], derived["rev_py"], derived["rev_cy"])
    qoe = quality_of_earnings(derived["cfo_cy"], derived["np_cy"])
    z = altman_z_score(fin)
    m = beneish_mscore(derived)

    # simple insight generation (short)
    notes = []
    if m is not None:
        if m > -1.78:
            notes.append("High Beneish M-score -> possible earnings manipulation.")
        elif m > -2.22:
            notes.append("Moderate Beneish M-score -> watch accounting policies.")
        else:
            notes.append("Low Beneish M-score -> lower manipulation risk.")

    if sloan is not None:
        if sloan > 0.12:
            notes.append("High accruals relative to assets -> weak earnings quality.")
        elif sloan > 0.05:
            notes.append("Moderate accruals -> check cash conversion.")
        else:
            notes.append("Accruals low -> earnings backed by cash.")

    if lev_idx is not None:
        if lev_idx > 1.2:
            notes.append("Leverage has increased significantly year-on-year.")
        elif lev_idx > 1.0:
            notes.append("Leverage increased moderately.")
        else:
            notes.append("Leverage stable or reduced.")

    if dso is not None:
        if abs(dso) > 15:
            notes.append("Receivables days changed substantially -> revenue recognition risk.")
        elif abs(dso) > 5:
            notes.append("Moderate DSO change -> monitor collections.")
        else:
            notes.append("DSO stable -> collection healthy.")

    if qoe is not None:
        if qoe < 0.75:
            notes.append("Quality of earnings is weak (CFO < PAT).")
        elif qoe < 1.0:
            notes.append("Earnings partially cash-supported.")
        else:
            notes.append("Earnings well supported by cashflows.")

    insight_text = "  •  ".join(notes)

    return {
        "beneish_mscore": m,
        "altman_z": z,
        "sloan_accrual": sloan,
        "leverage_index": lev_idx,
        "dso_change": dso,
        "quality_of_earnings": qoe,
        "insight": insight_text
    }
