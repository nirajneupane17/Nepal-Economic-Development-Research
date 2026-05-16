# Nepal Economic Development Research

**Economic Research for Global South**
*Researcher: Niraj Neupane, Economist*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Districts Covered](https://img.shields.io/badge/Districts-1%20of%2077-blue.svg)](#district-profiles)
[![Language](https://img.shields.io/badge/Language-English%20%7C%20नेपाली-orange.svg)](#)
[![Data Source](https://img.shields.io/badge/Data-World%20Bank%20%7C%20CBS%20Nepal%20%7C%20MoF-lightgrey.svg)](#data-sources)

---

## Overview

This repository contains district-level and constituency-level economic development research for Nepal — mapping existing income sources, development possibilities, priority interventions, financing pathways, and market opportunities for all 77 districts and 165 House of Representatives constituencies.

The work draws on Nepal's **Economic Survey 2081/82**, the **World Bank Nepal Development Update (April 2026)**, the **Ministry of Finance Economic Status Report (April 2026)**, and district-level data from CBS Nepal, Invest Nepal, and Nepal Rastra Bank.

> **Goal:** Translate national macroeconomic data into actionable, district-specific development frameworks — practical enough for local governments, investors, and policymakers to act on.

---

## National Context (2026)

| Indicator | Value | Trend |
|---|---|---|
| GDP (FY2025/26 estimate) | Rs. 6,600 billion | ↑ 3.85% real growth |
| GDP per capita | USD 1,517 | Steady improvement |
| Remittances (% of GDP) | 33% | Highest on record |
| Electricity installed capacity | 3,602 MW | ↑ Fastest-growing sector (21%) |
| Public debt | Rs. 2.929 trillion (43.8% GDP) | Manageable but rising |
| Revenue collection vs target | 50.5% (H1 FY26) | Consistently below target |
| Tourism arrivals (April 2026) | 107,934 | Slight decline (geopolitical) |

**Key structural challenge:** Population outmigration is accelerating — 839,000 labor approvals in FY2024/25 alone, growing at 28.6% annually. Every district profile in this repository addresses this directly.

---

## Repository Structure

```
Nepal-Economic-Development-Research/
│
├── README.md                          ← This file
├── LICENSE
│
├── macro/                             ← National-level analysis
│   ├── README.md
│   └── regime_comparison/            ← Development indicators across political regimes
│       ├── nepal_development_indicators_chart.png
│       └── nepal_development_indicators_table.png
│
├── policy/                            ← National policy recommendations
│   ├── short_policy_recommendations_2026.md
│   └── Nepal_Policy_Recommendation.png
│
├── data/                              ← Master datasets
│   ├── Nepal_Districts_Constituencies_Development.xlsx
│   ├── nepal_development_regime_comparison.csv
│   └── SOURCES.md
│
├── districts/                         ← District-level profiles (77 total)
│   ├── README.md                      ← District index
│   ├── 01_Bhojpur/
│   │   ├── README.md                  ← Full district development profile
│   │   └── assets/
│   │       ├── bhojpur_summary.png
│   │       ├── bhojpur_animated_en.gif
│   │       └── bhojpur_animated_np.gif
│   └── ...
│
└── notebooks/                         ← Jupyter notebooks (coming soon)
```

---

## District Profiles

Each district profile covers:
- **Snapshot** — population, area, literacy, ecological belt, key ethnicity
- **Existing income sources** — agriculture, remittances, crafts, tourism, hydropower
- **Infrastructure gaps** — roads, cold chain, processing, cooperatives
- **Priority interventions** — what to build, when, and at what priority level
- **Employment potential** — 6-year job creation outlook
- **Market opportunities** — domestic and export markets with pricing data
- **Financing sources** — ADB/World Bank, federal grants, BOOT funds, NIFRA, cooperatives

| # | District | Province | Ecological Belt | Status |
|---|---|---|---|---|
| 01 | [Bhojpur](districts/01_Bhojpur/README.md) | Koshi | Hill | ✅ Complete |
| 02 | Dhankuta | Koshi | Hill | 🔄 Upcoming |
| 03 | Ilam | Koshi | Hill | 🔄 Upcoming |
| … | … | … | … | … |
| 77 | Darchula | Sudurpaschim | Mountain | 🔄 Upcoming |

---

## Macro Analysis

### Nepal Development Indicators Across Political Regimes

![Nepal Development Indicators Chart](macro/regime_comparison/nepal_development_indicators_chart.png)

| Indicator | 1960 (Panchayat) | 1990 (Bahudal) | 2008 (Ganatantra) | Latest |
|---|---|---|---|---|
| GDP per capita (USD) | 50 | 186 | 465 | 1,447 |
| Life expectancy (years) | 38.6 | 54.7 | 66.4 | 70.3 |
| Infant mortality | 217 | 101 | 43 | 23 |
| Literacy (%) | NA | 33 | NA | 71.2 |
| Electricity capacity (MW) | NA | 240 | 700 | 2,190+ |
| Forex reserves (USD bn) | NA | 1.0 | 5.0 | 15.3 |
| Tourism arrivals (million) | 0.006 | 0.25 | 0.53 | 1.0 |

*Sources: World Bank, Nepal Rastra Bank, NEA, UNDP, CBS Nepal*

---

## Policy Recommendations — Short Summary (2026)

![Policy Recommendations](policy/Nepal_Policy_Recommendation.png)

| Area | Recommendation | Reform |
|---|---|---|
| Governance | Transparency, digital procurement, anti-corruption | Open contracting, public dashboards |
| Public Finance | High-impact spending, tax administration | Performance-based budgeting |
| Jobs & Industry | SMEs, agro-processing, tourism, labor-intensive | Credit access, skills training, clusters |
| Energy | Expand hydropower, pilot wind/solar | Energy-linked industrial policy |
| Agriculture | Agro-processing, poultry, storage, irrigation | Value-chain financing, cold storage |
| Local Development | Strengthen local bodies, service delivery | Social audits, digital reporting |
| Trade & SMEs | Logistics, border trade, industrial zones | Customs reform, simplified registration |

---

## Data Sources

| Source | Description | Used For |
|---|---|---|
| [World Bank Nepal Development Update (Apr 2026)](https://www.worldbank.org/en/country/nepal/publication/nepaldevelopmentupdate) | Macro growth, fiscal, financial sector | National context |
| [Ministry of Finance Economic Status Report (Apr 2026)](https://mof.gov.np) | Remittances, trade, debt | National context |
| [CBS Nepal — National Statistics Office](https://cbs.gov.np) | District population, census 2021 | All district profiles |
| [Invest Nepal](https://investnepal.gov.np) | Sector investment opportunities | District economic anchors |
| [Nepal Rastra Bank](https://nrb.org.np) | Monetary, financial data | Financing analysis |
| [MoALD — Agriculture data](https://moald.gov.np) | Crop production, value chains | District agriculture |
| [SJVN / Investment Board Nepal](https://ibn.gov.np) | Hydropower project data | Energy analysis |

---

## About

**Niraj Neupane** is an Economist and Quantitative Risk Analyst based in New York, with an MS in Financial Economics (University of Wisconsin–Madison) and a Chartered Accountant designation (ICAI). This research is conducted under **Economic Research for Global South** — a long-term project exploring district-wise and constituency-wise economic opportunities in Nepal.

**Connect:**
- GitHub: [nirajneupane17](https://github.com/nirajneupane17)
- Repository: [Nepal-Economic-Development-Research](https://github.com/nirajneupane17/Nepal-Economic-Development-Research)

---

*Last updated: May 2026 | Data cutoff: April 2026*
