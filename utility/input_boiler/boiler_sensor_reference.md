# Boiler Sensor Reference Guide

> **System:** Industrial Hot Water Boiler Monitoring  
> **Document version:** 1.0  
> **Last updated:** 2026-05-25

---

## Overview

This document defines all sensors used in a boiler monitoring system, including measurement units, normal operating ranges, warning thresholds, failure thresholds, and sample data for each sensor.

### Sensor Categories

| Category | Description |
|----------|-------------|
| **INPUT** | Raw physical measurements entering the system |
| **OUTPUT** | Physical properties leaving the boiler |
| **DERIVED** | Calculated values computed from input sensors |

---

## Threshold Reference Summary

| Sensor | Unit | Min (Normal) | Max (Normal) | Warning | Failure / Shutdown |
|--------|------|:---:|:---:|---------|-------------------|
| Supply Temperature | °C | 60 | 80 | > 85 °C | > 95 °C |
| Return Temperature | °C | 40 | 60 | > 70 °C | > 80 °C |
| System Pressure | bar | 1.0 | 2.5 | < 0.8 or > 2.8 bar | < 0.5 or > 3.0 bar |
| Flow Rate | m³/h | 1.0 | 5.0 | < 0.5 m³/h | < 0.3 m³/h (while firing) |
| Delta T | °C | 15 | 25 | < 5 or > 35 °C | > 40 °C |
| Thermal Power | kW | Rated 20% | Rated 100% | < 20% rated | 0 kW while demand active |
| Flue Gas Temperature | °C | 120 | 200 | > 230 °C | > 280 °C |

---

## Sensor 1 — Supply Temperature (T_supply)

- **Category:** INPUT
- **Unit:** °C (degrees Celsius)
- **Measurement point:** Hot water outlet pipe, leaving the boiler
- **Sensor type:** RTD PT100 or Thermocouple type K
- **Normal range:** 60 – 80 °C
- **Warning threshold:** > 85 °C → reduce burner firing rate
- **Failure / Shutdown threshold:** > 95 °C → emergency burner cutoff
- **Cold start value:** ~10 – 30 °C (system warming up)

**Formula reference:** Used in ΔT and Thermal Power calculations.

### Sample Data — Supply Temperature

| # | Timestamp | Value (°C) | Status | Note |
|---|-----------|:----------:|--------|------|
| 1 | 2026-05-25 08:00:00 | 25.3 | NORMAL | Cold start, system warming |
| 2 | 2026-05-25 08:05:00 | 41.7 | NORMAL | Warming phase |
| 3 | 2026-05-25 08:10:00 | 62.4 | NORMAL | Reached operating range |
| 4 | 2026-05-25 08:15:00 | 71.8 | NORMAL | Steady state |
| 5 | 2026-05-25 08:20:00 | 74.2 | NORMAL | Steady state |
| 6 | 2026-05-25 08:25:00 | 78.9 | NORMAL | Near upper normal |
| 7 | 2026-05-25 08:30:00 | 83.1 | NORMAL | Slightly elevated, monitor |
| 8 | 2026-05-25 08:35:00 | 87.5 | **WARNING** | Exceeded 85 °C — reduce firing |
| 9 | 2026-05-25 08:40:00 | 93.2 | **WARNING** | Approaching shutdown threshold |
| 10 | 2026-05-25 08:45:00 | 96.8 | **FAILURE** | Exceeded 95 °C — emergency shutdown |

---

## Sensor 2 — Return Temperature (T_return)

- **Category:** INPUT
- **Unit:** °C (degrees Celsius)
- **Measurement point:** Return water pipe, entering the boiler
- **Sensor type:** RTD PT100
- **Normal range:** 40 – 60 °C
- **Warning threshold:** > 70 °C → ΔT too small, possible flow bypass
- **Failure / Shutdown threshold:** > 80 °C → critical — heat transfer failure
- **Note:** Return temp should always be lower than supply temp. If T_return ≈ T_supply, there is a circulation fault.

**Formula reference:** Used in ΔT = T_supply − T_return

### Sample Data — Return Temperature

| # | Timestamp | Value (°C) | Status | Note |
|---|-----------|:----------:|--------|------|
| 1 | 2026-05-25 08:00:00 | 22.1 | NORMAL | Cold start |
| 2 | 2026-05-25 08:05:00 | 35.4 | NORMAL | Warming up |
| 3 | 2026-05-25 08:10:00 | 44.6 | NORMAL | Reached operating range |
| 4 | 2026-05-25 08:15:00 | 51.2 | NORMAL | Steady state |
| 5 | 2026-05-25 08:20:00 | 53.7 | NORMAL | Steady state |
| 6 | 2026-05-25 08:25:00 | 57.9 | NORMAL | Near upper normal |
| 7 | 2026-05-25 08:30:00 | 63.4 | NORMAL | Slightly elevated |
| 8 | 2026-05-25 08:35:00 | 71.8 | **WARNING** | Exceeded 70 °C — check flow bypass |
| 9 | 2026-05-25 08:40:00 | 76.5 | **WARNING** | Approaching failure |
| 10 | 2026-05-25 08:45:00 | 81.3 | **FAILURE** | Exceeded 80 °C — heat transfer failure |

---

## Sensor 3 — System Pressure (P_system)

- **Category:** INPUT
- **Unit:** bar
- **Measurement point:** Main water circuit, boiler manifold
- **Sensor type:** Pressure transducer (4–20 mA output)
- **Normal range:** 1.0 – 2.5 bar
- **Warning threshold (low):** < 0.8 bar → possible leak or expansion vessel fault
- **Warning threshold (high):** > 2.8 bar → overpressure developing
- **Failure threshold (low):** < 0.5 bar → critical low pressure, shutdown
- **Failure threshold (high):** > 3.0 bar → pressure relief valve activates
- **Note:** Pressure and temperature are linked (PV = nRT). Pressure rising without temperature increase suggests expansion vessel failure.

### Sample Data — System Pressure

| # | Timestamp | Value (bar) | Status | Note |
|---|-----------|:-----------:|--------|------|
| 1 | 2026-05-25 08:00:00 | 1.20 | NORMAL | Cold system pressure |
| 2 | 2026-05-25 08:05:00 | 1.35 | NORMAL | Pressure rising with temp |
| 3 | 2026-05-25 08:10:00 | 1.58 | NORMAL | Normal operating range |
| 4 | 2026-05-25 08:15:00 | 1.72 | NORMAL | Steady state |
| 5 | 2026-05-25 08:20:00 | 1.80 | NORMAL | Steady state |
| 6 | 2026-05-25 08:25:00 | 0.75 | **WARNING** | Low pressure — possible minor leak |
| 7 | 2026-05-25 08:30:00 | 0.61 | **WARNING** | Pressure continues dropping |
| 8 | 2026-05-25 08:35:00 | 0.48 | **FAILURE** | Below 0.5 bar — shutdown triggered |
| 9 | 2026-05-25 09:00:00 | 2.85 | **WARNING** | High pressure — check expansion vessel |
| 10 | 2026-05-25 09:05:00 | 3.05 | **FAILURE** | Overpressure — relief valve activated |

---

## Sensor 4 — Water Flow Rate (Q)

- **Category:** INPUT
- **Unit:** m³/h (cubic metres per hour)
- **Measurement point:** Primary water circuit, supply pipe
- **Sensor type:** Electromagnetic flow meter or ultrasonic flow meter
- **Normal range:** 1.0 – 5.0 m³/h (varies by boiler rated capacity)
- **Warning threshold:** < 0.5 m³/h → low flow, check pump and valves
- **Failure / Shutdown threshold:** < 0.3 m³/h while burner is firing → immediate shutdown to prevent overheating
- **Note:** Flow is directly driven by differential pressure across the pump. ΔP ∝ Q². A flow drop with normal pressure = blockage.

**Formula reference:** Used in Thermal Power (kW) calculation.

### Sample Data — Water Flow Rate

| # | Timestamp | Value (m³/h) | Status | Note |
|---|-----------|:------------:|--------|------|
| 1 | 2026-05-25 08:00:00 | 0.00 | NORMAL | System off, pump not started |
| 2 | 2026-05-25 08:01:00 | 1.20 | NORMAL | Pump started |
| 3 | 2026-05-25 08:05:00 | 2.45 | NORMAL | Normal circulation |
| 4 | 2026-05-25 08:10:00 | 3.10 | NORMAL | Steady state |
| 5 | 2026-05-25 08:15:00 | 3.22 | NORMAL | Steady state |
| 6 | 2026-05-25 08:20:00 | 3.18 | NORMAL | Steady state |
| 7 | 2026-05-25 08:30:00 | 0.82 | NORMAL | Load reduced, flow lower |
| 8 | 2026-05-25 08:35:00 | 0.44 | **WARNING** | Flow below 0.5 m³/h — check pump |
| 9 | 2026-05-25 08:40:00 | 0.27 | **FAILURE** | No-flow condition while firing — shutdown |
| 10 | 2026-05-25 08:45:00 | 0.00 | **FAILURE** | Complete flow loss — emergency stop |

---

## Sensor 5 — Flue Gas Temperature (T_flue)

- **Category:** OUTPUT
- **Unit:** °C (degrees Celsius)
- **Measurement point:** Flue exhaust duct, after heat exchanger
- **Sensor type:** Thermocouple type K (high temperature range)
- **Normal range:** 120 – 200 °C (conventional boiler); 50 – 80 °C (condensing boiler)
- **Warning threshold:** > 230 °C → possible heat exchanger fouling (scale or soot)
- **Failure / Shutdown threshold:** > 280 °C → combustion fault or severe fouling
- **Note:** Every 15 °C rise above optimal flue temperature reduces boiler efficiency by ~1%. High flue temp with normal supply temp = heat exchanger needs cleaning.

**Efficiency estimate:** `Efficiency (%) ≈ 100 − (T_flue − T_ambient) × 0.11`

### Sample Data — Flue Gas Temperature

| # | Timestamp | Value (°C) | Efficiency Est. (%) | Status | Note |
|---|-----------|:----------:|:-------------------:|--------|------|
| 1 | 2026-05-25 08:00:00 | 30.0 | — | NORMAL | Burner off, ambient |
| 2 | 2026-05-25 08:02:00 | 85.4 | — | NORMAL | Burner just ignited |
| 3 | 2026-05-25 08:05:00 | 138.2 | 90.4 | NORMAL | Steady combustion |
| 4 | 2026-05-25 08:10:00 | 155.7 | 88.5 | NORMAL | Normal operation |
| 5 | 2026-05-25 08:15:00 | 162.3 | 87.8 | NORMAL | Normal operation |
| 6 | 2026-05-25 08:20:00 | 178.9 | 86.0 | NORMAL | Near upper normal |
| 7 | 2026-05-25 08:25:00 | 198.4 | 83.9 | NORMAL | Acceptable, monitor |
| 8 | 2026-05-25 08:30:00 | 234.1 | 79.5 | **WARNING** | Exceeded 230 °C — inspect heat exchanger |
| 9 | 2026-05-25 08:35:00 | 261.8 | 76.5 | **WARNING** | Severe fouling suspected |
| 10 | 2026-05-25 08:40:00 | 283.5 | — | **FAILURE** | Exceeded 280 °C — combustion fault |

---

## Derived Value 1 — Delta T (ΔT)

- **Category:** DERIVED (calculated, no physical sensor)
- **Unit:** °C
- **Formula:** `ΔT = T_supply − T_return`
- **Normal range:** 15 – 25 °C
- **Warning (low):** < 5 °C → possible flow short-circuit or pump overspeeding
- **Warning (high):** > 35 °C → very low flow, heat not distributed
- **Failure threshold:** > 40 °C → extremely low flow — danger of overheating

### Sample Data — Delta T

| # | Timestamp | T_supply (°C) | T_return (°C) | ΔT (°C) | Status | Note |
|---|-----------|:-------------:|:-------------:|:-------:|--------|------|
| 1 | 2026-05-25 08:00:00 | 25.3 | 22.1 | 3.2 | NORMAL | System cold, not meaningful |
| 2 | 2026-05-25 08:05:00 | 41.7 | 35.4 | 6.3 | NORMAL | Warming up |
| 3 | 2026-05-25 08:10:00 | 62.4 | 44.6 | 17.8 | NORMAL | Entered normal range |
| 4 | 2026-05-25 08:15:00 | 71.8 | 51.2 | 20.6 | NORMAL | Steady state |
| 5 | 2026-05-25 08:20:00 | 74.2 | 53.7 | 20.5 | NORMAL | Steady state |
| 6 | 2026-05-25 08:25:00 | 78.9 | 57.9 | 21.0 | NORMAL | Steady state |
| 7 | 2026-05-25 08:30:00 | 76.3 | 72.1 | 4.2 | **WARNING** | ΔT < 5 °C — possible bypass |
| 8 | 2026-05-25 08:35:00 | 83.1 | 44.2 | 38.9 | **WARNING** | ΔT > 35 °C — low flow |
| 9 | 2026-05-25 08:40:00 | 87.5 | 46.1 | 41.4 | **FAILURE** | ΔT > 40 °C — danger zone |
| 10 | 2026-05-25 08:45:00 | 71.8 | 71.2 | 0.6 | **FAILURE** | Near-zero ΔT — full short-circuit |

---

## Derived Value 2 — Thermal Power (kW)

- **Category:** DERIVED (calculated from Q, T_supply, T_return)
- **Unit:** kW (kilowatts)
- **Formula:** `kW = Q [m³/h] × 1000 [L/m³] × 4.18 [J/g·°C] × ΔT [°C] / 3600`
  - Simplified: `kW = Q × 1.161 × ΔT`
- **Normal range:** Depends on boiler rated capacity (e.g. 50 – 500 kW for industrial)
- **Warning threshold:** Output < 20% of rated capacity while firing
- **Failure threshold:** 0 kW output while burner is on and demand is active

### Sample Data — Thermal Power (example: 100 kW rated boiler)

| # | Timestamp | Q (m³/h) | ΔT (°C) | Power (kW) | % of Rated | Status | Note |
|---|-----------|:--------:|:-------:|:----------:|:----------:|--------|------|
| 1 | 2026-05-25 08:00:00 | 0.00 | 3.2 | 0.0 | 0% | NORMAL | System off |
| 2 | 2026-05-25 08:05:00 | 1.20 | 6.3 | 8.8 | 9% | NORMAL | Warming up |
| 3 | 2026-05-25 08:10:00 | 2.45 | 17.8 | 50.8 | 51% | NORMAL | Partial load |
| 4 | 2026-05-25 08:15:00 | 3.10 | 20.6 | 74.4 | 74% | NORMAL | Good load |
| 5 | 2026-05-25 08:20:00 | 3.22 | 20.5 | 76.9 | 77% | NORMAL | Steady state |
| 6 | 2026-05-25 08:25:00 | 3.18 | 21.0 | 77.6 | 78% | NORMAL | Steady state |
| 7 | 2026-05-25 08:30:00 | 3.10 | 22.4 | 80.9 | 81% | NORMAL | High efficiency |
| 8 | 2026-05-25 08:35:00 | 0.44 | 38.9 | 20.0 | 20% | **WARNING** | Low flow — power dropping |
| 9 | 2026-05-25 08:40:00 | 0.27 | 41.4 | 13.0 | 13% | **FAILURE** | Flow loss — near shutdown |
| 10 | 2026-05-25 08:45:00 | 0.00 | 0.6 | 0.0 | 0% | **FAILURE** | No output while demand active |

---

## Alarm & Status Code Reference

| Status Code | Color | Meaning | Action Required |
|-------------|-------|---------|----------------|
| `NORMAL` | Green | Value within operating range | None |
| `WARNING` | Amber | Value approaching limit — investigate | Log event, alert operator |
| `FAILURE` | Red | Value exceeded safe limit | Trigger interlock / shutdown |

---

## Key Sensor Relationships

### 1. Temperature ↔ Pressure (Gas Law)
```
P rises proportionally with T in a sealed system.
If P rises without T rising → expansion vessel fault or external pressure source.
If T rises without P rising → possible pressure leak.
```

### 2. Pressure → Flow (Pump Curve)
```
Q ∝ √(ΔP_pump)
Drop in flow with constant pressure → blockage or closed valve.
Drop in flow with drop in pressure → pump failure or leak.
```

### 3. T_supply + T_return → ΔT → Thermal Power
```
ΔT = T_supply − T_return
kW  = Q × 1.161 × ΔT

Primary efficiency KPI. Low kW with burner firing = heat transfer problem.
```

### 4. T_flue → Combustion Efficiency
```
Efficiency (%) ≈ 100 − (T_flue − T_ambient) × 0.11
High T_flue with normal T_supply = heat exchanger fouling (scale or soot).
```

---

## Implementation Notes for Dashboard / PoC

1. **Sample rate:** Minimum 1 sample per minute for all sensors; 10-second intervals recommended for T_supply and flow during transients.
2. **Priority alarms to implement first:**
   - No-flow shutdown: `if burner_on AND Q < 0.3 → emergency_stop`
   - Overtemperature: `if T_supply > 95 → emergency_stop`
   - Overpressure: `if P_system > 3.0 → emergency_stop`
3. **Recommended headline metrics for chart dashboard:** Thermal Power (kW) and ΔT as primary KPIs; raw sensor values in secondary panel.
4. **Data types for storage:**

| Field | Type | Example |
|-------|------|---------|
| `timestamp` | ISO 8601 datetime | `2026-05-25T08:15:00Z` |
| `sensor_id` | string | `T_supply`, `P_system` |
| `value` | float (2 decimal places) | `71.84` |
| `unit` | string | `°C`, `bar`, `m³/h`, `kW` |
| `status` | enum | `NORMAL`, `WARNING`, `FAILURE` |

---

*End of document — Boiler Sensor Reference v1.0*
