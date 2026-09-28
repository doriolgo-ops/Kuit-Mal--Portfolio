"""NORMALISED CLAIM layer: units and formats, never the meaning.

Returns dict(norm_value, norm_min, norm_max, norm_unit, norm_text, norm_note). Values that
cannot be parsed keep norm_text only and are flagged; nothing is guessed.
"""
import re

from .common import find_cas


def _num(s):
    s = s.replace(" ", "").replace(",", ".")
    s = re.sub(r"[eE]\+?", "e", s)
    try:
        return float(s)
    except ValueError:
        return None


VP_FACTORS = {"pa": 1.0, "hpa": 100.0, "kpa": 1000.0, "mmhg": 133.322, "torr": 133.322}


PLAUSIBLE = {"vapour_pressure": (1e-7, 5000), "flash_point": (-20, 320), "boiling_point": (100, 480),
             "density": (0.65, 1.6), "refractive_index": (1.33, 1.70), "logp": (-2, 11), "molecular_weight": (30, 800),
             "tenacity": (0.1, 5000)}
NUMERIC_FIELDS = set(PLAUSIBLE) | {"use_level"}


def normalize(field, raw):
    out = _normalize(field, raw)
    if field in PLAUSIBLE and re.fullmatch(r"\s*0(?:[.,]0+)?\s*", str(raw)):
        out["norm_note"] = "placeholder zero in source"
        out["implausible"] = True
    v = next((out[k] for k in ("norm_value", "norm_max", "norm_min") if out[k] is not None), None)
    if field in PLAUSIBLE and v is not None and not (PLAUSIBLE[field][0] <= v <= PLAUSIBLE[field][1]):
        out["norm_note"] = (out["norm_note"] + f"; IMPLAUSIBLE for {field} (outside {PLAUSIBLE[field]})").strip("; ")
        out["implausible"] = True
    b = re.match(r"\s*([<>]=?)", str(raw))
    if b and field in PLAUSIBLE:
        out["bound"] = b.group(1)[0]
    elif out.get("norm_note") and "bound >" in out["norm_note"]:
        out["bound"] = ">"
    elif out.get("norm_note") and "bound <" in out["norm_note"]:
        out["bound"] = "<"
    return out


def _normalize(field, raw):
    raw = str(raw)
    out = {"norm_value": None, "norm_min": None, "norm_max": None, "norm_unit": None, "norm_text": raw, "norm_note": ""}
    low = raw.lower()
    if field in ("cas", "cas_mentioned", "sds_component_cas"):
        cas = find_cas(raw)
        out["norm_text"] = cas[0] if cas else raw
        return out
    if field == "vapour_pressure":
        m = None
        for mm in re.finditer(r"(\d*[.,]?\d+(?:\s*[eE]\s*-?\d+)?)\s*(hpa|kpa|pa|mm ?hg|mmhg|torr)\b", low):
            if (_num(mm.group(1).replace(" ", "")) or 0) > 0:
                m = mm
                break
        if m:
            v = _num(m.group(1).replace(" ", ""))
            unit = m.group(2).replace(" ", "")
            if v is not None:
                out.update(norm_value=round(v * VP_FACTORS[unit], 6), norm_unit="Pa")
                t = re.search(r"(\d{1,3})\s*°?\s*c", low[m.end():])
                out["norm_note"] = f"converted from {m.group(1)} {m.group(2)}" + (f" at {t.group(1)} C" if t else " (temperature not stated)")
        return out
    if field == "flash_point":
        m = re.search(r"([<>]=?)?\s*(\d+(?:[.,]\d+)?)\s*°?\s*([cf])\b", low)
        if m:
            v = _num(m.group(2))
            if m.group(3) == "f":
                v = round((v - 32) * 5 / 9, 1)
                out["norm_note"] = f"converted from {m.group(2)} F"
            out.update(norm_value=v, norm_unit="C")
            if m.group(1):
                out["norm_note"] = (out["norm_note"] + f"; bound {m.group(1)}").strip("; ")
        return out
    if field == "boiling_point":
        m = re.search(r"(\d{2,3}(?:[.,]\d+)?)", low)
        if m:
            out.update(norm_value=_num(m.group(1)), norm_unit="C")
        return out
    if field == "density" and re.search(r"kg\s*/\s*m", low):
        m = re.search(r"(\d{3,4}(?:[.,]\d+)?)\s*kg", low)
        if m:
            v = _num(m.group(1)) / 1000
            out.update(norm_value=round(v, 4), norm_min=v, norm_max=v, norm_unit="g/cm3", norm_note="converted from kg/m3")
        return out
    if field in ("density", "refractive_index"):
        nums = [_num(x) for x in re.findall(r"\d[.,]\d{2,5}", raw)]
        nums = [n for n in nums if n is not None and (0.6 < n < 1.8)]
        if nums:
            out.update(norm_min=min(nums), norm_max=max(nums), norm_value=round(sum(nums) / len(nums), 4),
                       norm_unit="g/cm3 (or SG, ~equal at 20-25 C)" if field == "density" else "nD")
        return out
    if field == "logp":
        m = re.search(r"-?\d+(?:[.,]\d+)?", raw)
        v = _num(m.group(0)) if m else None
        if v is not None and -3 < v < 12:
            out.update(norm_value=v, norm_unit="log10")
        return out
    if field == "use_level":
        nums = [_num(x) for x in re.findall(r"\d+(?:[.,]\d+)?", raw)]
        nums = [n for n in nums if n is not None]
        if not nums:
            if re.search(r"trace", low):
                out.update(norm_min=0.0, norm_unit="%", norm_note="traces")
            return out
        if "up to" in low or "max" in low or "<" in low:
            out.update(norm_max=nums[-1], norm_value=None, norm_unit="%")
            if re.search(r"trace", low):
                out["norm_min"] = 0.0
        elif len(nums) >= 2:
            out.update(norm_min=min(nums[:2]), norm_max=max(nums[:2]), norm_unit="%")
        else:
            out.update(norm_value=nums[0], norm_unit="%")
        if "%" not in raw:
            out["norm_note"] = "unit not printed; assumed %"
        out["norm_note"] = (out["norm_note"] + "; denominator not stated by source").strip("; ")
        return out
    if field == "tenacity":
        m = re.search(r"([<>])?\s*(\d+(?:[.,]\d+)?)\s*(hours?|hrs?|h\b|days?|weeks?|months?)", low)
        if m:
            v = _num(m.group(2))
            mult = {"h": 1, "d": 24, "w": 168, "m": 720}[m.group(3)[0]]
            out.update(norm_value=v * mult, norm_unit="hours")
            out["norm_note"] = "substrate: blotter unless stated" + (f"; bound {m.group(1)}" if m.group(1) else "")
        return out
    if field in ("substantivity_application", "performance_application"):
        m = re.search(r"(\d)/5", raw)
        if m:
            out.update(norm_value=float(m.group(1)), norm_unit="stars (0-5, manufacturer scale)")
        return out
    if field == "molecular_weight":
        m = re.search(r"\d+(?:[.,]\d+)?", raw)
        if m:
            out.update(norm_value=_num(m.group(0)), norm_unit="g/mol")
        return out
    if field.startswith("composition:"):
        nums = [_num(x) for x in re.findall(r"\d+(?:[.,]\d+)?", raw)]
        nums = [n for n in nums if n is not None and n <= 100]
        if nums:
            out.update(norm_min=min(nums), norm_max=max(nums), norm_value=nums[0] if len(nums) == 1 else None,
                       norm_unit="% (relative peak area unless stated)")
        return out
    if field in ("odour_description", "physical_state", "solubility", "stability_text", "storage", "botanical_name",
                 "plant_part", "extraction_method", "origin", "odour_family", "chemical_name"):
        out["norm_text"] = re.sub(r"\s+", " ", raw).strip()
    return out
