Coral Reef Tipping Point Evidence Assessment
Data Inspection and Feasibility Analysis


# PROJECT OVERVIEW


This repository contains a structured data inspection and feasibility analysis of
multiple long-term coral reef monitoring datasets. The purpose of this work is
not to predict tipping points, but to rigorously assess how strong the available
empirical evidence is for claims that coral reef systems have already crossed a
dynamical tipping point.

The analysis focuses on:
- Identifying genuine time-series datasets (not spatial snapshots)
- Evaluating whether the data support early-warning signals such as increased
  variance or autocorrelation
- Distinguishing externally forced collapses from intrinsic dynamical tipping

All analyses are intentionally conservative and diagnostic, designed to clarify
what the data can and cannot support.


# REPOSITORY STRUCTURE


CoralReefs/
│
├── Data/
│   ├── Coral_Cover/
│   │   └── coral_cover.csv
│   │
│   ├── Moorea_Coral_Reef_LongTerm_Ecological/
│   │   └── Moorea_Coral_Reef.csv
│   │
│   ├── AIMS_LTMP_manta-tow-by-reef/
│   │   └── manta-tow-by-reef.csv
│   │
│   └── USGS_Coral_cover_data/
│       └── Coral_cover_data.csv
│
├── data_loader.py
└── README.md



# DATASETS

Dataset 1: Coral Cover at St. John (USVI) and Moʻorea LTER Sites (1992–2019)
Source:
https://www.bco-dmo.org/dataset/832378

Long-term, annually resolved measurements of live stony coral cover collected at
fixed reef transects. The dataset captures multiple documented disturbance events
and periods of recovery. It provides a clean benchmark for testing whether abrupt
declines correspond to irreversible regime shifts or transient disturbances.


------------------------------------------------------------

Dataset 2: Moorea Coral Reef Long-Term Ecological Research (LTER) (2005–2025)
Sources:
https://mcr.lternet.edu/data
https://portal.edirepository.org/nis/mapbrowse?scope=knb-lter-mcr&identifier=4
https://dex.edirepository.org/dex/profile/96757

High-quality, site-specific annual time series of coral cover, benthic composition,
and taxonomic structure. The dataset captures a well-documented collapse followed
by substantial recovery, making it particularly valuable for distinguishing
collapse from true tipping.


------------------------------------------------------------

Dataset 3: AIMS Long-Term Monitoring Program (LTMP) Manta Tow Data
Sources:
https://apps.aims.gov.au/metadata/view/5bb9a340-4ade-11dc-8f56-00008a07204e
https://apps.aims.gov.au/metadata/view/a17249ab-5316-4396-bb27-29f2d568f727

Multi-decadal reef-level observations of coral cover across the Great Barrier Reef.
Includes explicit measurements of external stressors, especially crown-of-thorns
starfish density. Temporal sampling is sparse and irregular, limiting tipping-point
inference despite long time spans.


# Dataset 4: USGS Coral Cover Time-Series Dataset (1992–2015)
Sources:
https://coastal.er.usgs.gov/data-release/doi-F78W3C7W/
https://www.usgs.gov/data/time-series-coral-cover-data-hawaii-florida-moorea-and-virgin-islands

Site-level coral cover time series from 123 fixed reef sites across multiple regions.
Data include taxonomic resolution and span up to ~24 years at best-sampled sites.
The dataset highlights limitations of detectability when monitoring begins after
substantial ecological degradation.


# CODE OVERVIEW: data_loader.py

The data_loader.py script performs dataset-specific loading, validation, and
diagnostic analysis. Its purpose is feasibility assessment, not modeling or
prediction.

Each dataset has a dedicated loader function that:
1. Confirms genuine temporal structure (Sanity check for having time-series)
2. Constructs site-level time series
3. Selects well-sampled example sites
4. Applies standardized diagnostics

Key diagnostics include:
- Rolling variance
- Rolling lag-1 autocorrelation
- Signal-to-noise and detectability analysis

A dedicated detectability diagnostic explicitly evaluates whether early-warning
signals would be statistically observable given noise, sampling resolution, and
record length.


# SUMMARY OF FINDINGS

Across all datasets:
- Abrupt coral declines are common, but recovery is frequently observed
- Canonical early-warning signals of critical slowing down are not robustly present
- External stressors dominate observed dynamics
- Noise and sampling limitations strongly constrain inference

Conclusion:
Currently available observational datasets do not provide strong scientific
evidence that coral reef systems have already crossed an intrinsic dynamical
tipping point. Instead, they reveal fundamental limits on detectability and the
risk of conflating collapse with irreversible regime shifts.


# SCOPE AND NEXT STEPS

This repository establishes:
- Data feasibility
- Empirical constraints
- A disciplined separation between claims and evidence

Any future modeling (e.g., reservoir computing or meta-learning) should proceed
only after explicitly accounting for these limitations and addressing issues of
learnability and detectability.
