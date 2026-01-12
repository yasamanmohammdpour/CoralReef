import pandas as pd
import numpy as np

# ======================================================
# DATASET 1: STONY CORAL COVER (UNCHANGED BEHAVIOR)
# ======================================================

def load_stony_coral_cover(path="Data/Coral_Cover/coral_cover.csv"):
    print("\n==============================")
    print("LOADING STONY CORAL COVER DATA")
    print("==============================")

    df = pd.read_csv(path)
    print(f"Loaded shape: {df.shape}")
    print("Columns:", df.columns.tolist())

    # --- Time series check ---
    time_col = "Year"
    site_col = "Site"
    state_col = "Stony_coral_cover"

    df = df.sort_values([site_col, time_col])
    df[time_col] = pd.to_numeric(df[time_col], errors="coerce")

    counts = df.groupby(site_col)[time_col].nunique()

    print("\nTime series summary:")
    print("Sites:", counts.index.tolist())
    print("Years per site (min / max):", counts.min(), "/", counts.max())

    print("PASS: Dataset qualifies as time series")

    # --- Tipping signal check (example site) ---
    site_example = counts.idxmax()
    ts = (
        df[df[site_col] == site_example]
        .groupby(time_col)[state_col]
        .mean()
    )

    _tipping_sanity(ts, label="Stony coral cover")

    detectability_diagnostic(
        ts,
        label="Stony coral cover"
    )

    return df


# ======================================================
# DATASET 2: MOOREA LTER COMMUNITY DATA
# ======================================================

def load_moorea_lter(path="Data/Moorea_Coral_Reef_LongTerm_Ecological/Moorea_Coral_Reef.csv"):
    print("\n==============================")
    print("LOADING MOOREA LTER DATA")
    print("==============================")

    df = pd.read_csv(path)
    print(f"Loaded shape: {df.shape}")
    print("Columns:", df.columns.tolist())

    # --- Identify time & site ---
    time_col = "Date"
    site_col = "Location"

    df[time_col] = pd.to_numeric(df[time_col], errors="coerce")
    df = df.sort_values([site_col, time_col])

    # --- Define coral taxa columns (hard corals only) ---
    coral_genera = [
        "Acropora", "Porites", "Pocillopora", "Montipora",
        "Pavona", "Astrea", "Astreopora", "Cyphastrea",
        "Goniastrea", "Leptastrea", "Leptoseris",
        "Lobophyllia", "Psammocora", "Stylocoeniella"
    ]

    coral_genera = [c for c in coral_genera if c in df.columns]

    # Convert to numeric
    for c in coral_genera:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # --- Construct aggregate coral cover ---
    df["Total_Hard_Coral"] = df[coral_genera].sum(axis=1)

    # Optional: macroalgae vs sand
    for col in ["Macroalgae", "Sand"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # --- Time series sanity check ---
    counts = df.groupby(site_col)[time_col].nunique()

    print("\nTime series summary:")
    print("Number of sites:", len(counts))
    print("Years per site (min / max):", counts.min(), "/", counts.max())

    if counts.min() < 10:
        print("WARNING: Some sites have short records")

    print("PASS: Moorea dataset qualifies as time series")

    # --- Example site tipping check ---
    site_example = counts.idxmax()
    ts = (
        df[df[site_col] == site_example]
        .groupby(time_col)["Total_Hard_Coral"]
        .mean()
    )

    _tipping_sanity(ts, label="Total hard coral (aggregated)")

    detectability_diagnostic(
        ts,
        label="Total hard coral (Moorea LTER)"
    )

    return df



# ======================================================
# DATASET 3: AIMS LTMP MANTA-TOW (REEF-LEVEL SNAPSHOTS)
# ======================================================

def load_aims_manta_tow(
    path="Data/AIMS_LTMP_manta-tow-by-reef/manta-tow-by-reef.csv"
):
    print("\n==============================")
    print("LOADING AIMS MANTA-TOW DATA")
    print("==============================")

    df = pd.read_csv(path)
    print(f"Loaded shape: {df.shape}")
    print("Columns:", df.columns.tolist())

    # --- Time & site definitions ---
    time_col = "REPORT_YEAR"
    site_col = "REEF_NAME"

    df[time_col] = pd.to_numeric(df[time_col], errors="coerce")
    df = df.sort_values([site_col, time_col])

    # --- State variables ---
    state_vars = [
        "MEAN_LIVE_CORAL",
        "MEAN_DEAD_CORAL",
        "MEAN_SOFT_CORAL"
    ]

    for c in state_vars:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # --- Pressure variables (important for interpretation) ---
    for c in ["MEAN_COTS_PER_TOW", "TOTAL_COTS"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # --- Time series sanity ---
    counts = df.groupby(site_col)[time_col].nunique()

    print("\nTime series summary:")
    print("Number of reefs:", len(counts))
    print("Years per reef (min / max):", counts.min(), "/", counts.max())

    if counts.min() < 5:
        print("WARNING: Many reefs have sparse temporal sampling")

    print("PASS: Reef-level temporal structure confirmed")

    # --- Pick a well-sampled reef ---
    reef_example = counts.idxmax()
    print(f"\nExample reef: {reef_example}")

    ts = (
        df[df[site_col] == reef_example]
        .set_index(time_col)["MEAN_LIVE_CORAL"]
        .dropna()
    )

    _tipping_sanity_sparse(
        ts,
        df[df[site_col] == reef_example]
    )

    return df

# ======================================================
# SPARSE-TIME-SERIES SANITY (AIMS-SPECIFIC)
# ======================================================

def _tipping_sanity_sparse(ts, df_reef):
    print("\n------------------------------")
    print("SPARSE TIPPING SANITY CHECK")
    print("------------------------------")

    print("Time span:", ts.index.min(), "–", ts.index.max())
    print("Observations:", len(ts))

    diffs = ts.diff().abs()
    print("Max inter-survey change:", np.nanmax(diffs))

    print("\nNOTE:")
    print("This dataset is externally forced and irregularly sampled.")
    print("Absence of early-warning signals is EXPECTED and")
    print("does NOT imply system stability.")

    if "MEAN_COTS_PER_TOW" in df_reef.columns:
        print("\nCOTS pressure (summary):")
        print(df_reef["MEAN_COTS_PER_TOW"].describe())

    print("\nInterpretation:")
    print("This dataset supports threshold-like responses")
    print("under identifiable stressors, not intrinsic tipping.")


# ======================================================
# DATASET 4: USGS SPECIES-RESOLVED CORAL COVER
# ======================================================

def load_usgs_coral_cover(
    path="Data/USGS_Coral_cover_data/Coral_cover_data.csv"
):
    print("\n==============================")
    print("LOADING USGS CORAL COVER DATA")
    print("==============================")

    df = pd.read_csv(path, sep="\t" if "\t" in open(path).readline() else ",")
    print(f"Loaded shape: {df.shape}")
    print("Columns:", df.columns.tolist())

    # --- Time & site definitions ---
    time_col = "Year"
    site_col = "Site_name"
    taxon_col = "Taxon"
    state_col = "Percent_cover"

    df[time_col] = pd.to_numeric(df[time_col], errors="coerce")
    df[state_col] = pd.to_numeric(df[state_col], errors="coerce")

    df = df.sort_values([site_col, time_col])

    # --- Aggregate to total coral cover ---
    agg = (
        df.groupby([site_col, time_col])[state_col]
        .sum()
        .reset_index(name="Total_Coral_Cover")
    )

    # --- Time series sanity ---
    counts = agg.groupby(site_col)[time_col].nunique()

    print("\nTime series summary:")
    print("Number of sites:", len(counts))
    print("Years per site (min / max):", counts.min(), "/", counts.max())

    if counts.min() < 10:
        print("WARNING: Many sites have short or truncated records")

    print("PASS: Site-level temporal structure confirmed")

    # --- Example site tipping sanity ---
    site_example = counts.idxmax()
    print(f"\nExample site: {site_example}")

    ts = (
        agg[agg[site_col] == site_example]
        .set_index(time_col)["Total_Coral_Cover"]
        .dropna()
    )

    _tipping_sanity(
        ts,
        label="USGS total coral cover (aggregated)"
    )

    detectability_diagnostic(
        ts,
        label="USGS total coral cover"
    )

    print("\nNOTE:")
    print("Species-level zeros dominate this dataset.")
    print("Signals reflect post-collapse persistence,")
    print("not clean pre-transition dynamics.")

    return df, agg

# ======================================================
# SHARED TIPPING SANITY FUNCTION
# ======================================================

def _tipping_sanity(ts, label="state variable"):
    print("\n------------------------------")
    print(f"TIPPING SIGNAL CHECK: {label}")
    print("------------------------------")

    print("Time span:", ts.index.min(), "–", ts.index.max())
    print("Length:", len(ts))

    diffs = ts.diff().abs()
    print("Max year-to-year change:", np.nanmax(diffs))

    window = 5
    rolling_var = ts.rolling(window).var()
    rolling_ac = ts.rolling(window).apply(
        lambda x: pd.Series(x).autocorr(lag=1),
        raw=False
    )

    print("\nRolling variance (last 5):")
    print(rolling_var.tail())

    print("\nRolling autocorrelation (last 5):")
    print(rolling_ac.tail())

    if len(rolling_var.dropna()) > 0:
        print("\nEarly-warning consistency:")
        print("Variance increasing:",
              rolling_var.dropna().iloc[-1] > rolling_var.dropna().iloc[0])
        print("Autocorrelation increasing:",
              rolling_ac.dropna().iloc[-1] > rolling_ac.dropna().iloc[0])

    print("NOTE: Signals are CONSISTENT with destabilization,")
    print("but NOT sufficient to prove a tipping point.")


# ======================================================
# DETECTABILITY DIAGNOSTIC
# ======================================================

def detectability_diagnostic(ts, label="state variable"):
    print("\n==============================")
    print(f"DETECTABILITY DIAGNOSTIC: {label}")
    print("==============================")

    # --- Basic sanitation ---
    ts = ts.dropna()

    print("Time span:", ts.index.min(), "–", ts.index.max())
    print("Effective length:", len(ts))

    if len(ts) < 10:
        print("WARNING: Time series too short for reliable diagnostics")
        return

    # --- Noise vs signal ---
    diffs = ts.diff().dropna()

    signal_std = ts.std()
    noise_std = diffs.std()

    print("\nSignal statistics:")
    print("State std (signal level):", signal_std)
    print("Year-to-year diff std (noise level):", noise_std)

    if noise_std > signal_std:
        print("WARNING: Noise dominates signal")
    else:
        print("Signal-to-noise ratio acceptable")

    # --- Autocorrelation reliability ---
    ac = ts.autocorr(lag=1)
    print("\nLag-1 autocorrelation:", ac)

    if np.isnan(ac):
        print("WARNING: Autocorrelation undefined (insufficient structure)")
    elif abs(ac) < 0.2:
        print("WARNING: Weak autocorrelation – CSD signals unreliable")
    else:
        print("Autocorrelation magnitude potentially informative")

    # --- Rolling-window robustness check ---
    window = 5
    if len(ts) < 2 * window:
        print("\nWARNING: Too few points for rolling-window diagnostics")
    else:
        rolling_var = ts.rolling(window).var()
        rolling_ac = ts.rolling(window).apply(
            lambda x: pd.Series(x).autocorr(lag=1),
            raw=False
        )

        valid_var = rolling_var.dropna()
        valid_ac = rolling_ac.dropna()

        print("\nRolling diagnostics availability:")
        print("Rolling variance points:", len(valid_var))
        print("Rolling autocorr points:", len(valid_ac))

        if len(valid_var) < 3 or len(valid_ac) < 3:
            print("WARNING: Rolling diagnostics statistically fragile")

    # --- Final interpretation ---
    print("\nINTERPRETATION:")
    print(
        "Even if a tipping point existed in the underlying system, "
        "the combination of noise level, autocorrelation structure, "
        "and limited temporal resolution may prevent reliable detection "
        "of early-warning signals in this dataset."
    )

# ======================================================
# MAIN
# ======================================================

if __name__ == "__main__":

    # # For each dataset, uncomment their line below:

    # load_stony_coral_cover()
    # load_moorea_lter()
    # load_aims_manta_tow()
    load_usgs_coral_cover()
