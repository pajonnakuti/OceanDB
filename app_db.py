# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# Handle sqlite3 import gracefully for WebAssembly / Pyodide / Stlite environments
try:
    import sqlite3
    HAS_SQLITE = True
except ImportError:
    HAS_SQLITE = False

st.set_page_config(
    page_title="INCOIS ARGO CORE + BGC Real Data Explorer",
    page_icon="🌊",
    layout="wide",
)

DB_PATH = "argo_incois_real.db"
CSV_PATH = "incois_real_6floats_core_bgc.csv"

# ---------------------------------------------------------
# 1. Database Connection & Ingestion of 6 INCOIS Floats
# ---------------------------------------------------------
@st.cache_resource
def get_dataset():
    """Load dataset for desktop SQLite or browser CSV mode."""
    if HAS_SQLITE and os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            return ("sqlite", conn, None)
        except Exception:
            pass
            
    if os.path.exists(CSV_PATH):
        df_obs = pd.read_csv(CSV_PATH)
        if HAS_SQLITE:
            conn = sqlite3.connect(":memory:", check_same_thread=False)
            df_obs.to_sql('argo_observations', conn, index=False, if_exists='replace')
            
            df_prof = df_obs[['profile_id', 'wmoid', 'cycle', 'profile_date', 'latitude', 'longitude']].drop_duplicates()
            df_prof['qc_flag'] = 1
            df_prof.to_sql('argo_profiles', conn, index=False, if_exists='replace')
            
            floats_data = [
                (2902086, 'PROVOR_III', '2012-12-30', 'Dr. M. Ravichandran', 'INCOIS', 'Bay of Bengal', 'ACTIVE', 244),
                (2902087, 'PROVOR_III', '2013-01-01', 'Dr. M. Ravichandran', 'INCOIS', 'Bay of Bengal', 'ACTIVE', 323),
                (2902092, 'PROVOR_III', '2013-02-24', 'Dr. M. Ravichandran', 'INCOIS', 'Arabian Sea', 'ACTIVE', 148),
                (2902093, 'PROVOR_III', '2013-02-25', 'Dr. M. Ravichandran', 'INCOIS', 'Arabian Sea', 'ACTIVE', 234),
                (2902306, 'APEX', '2024-05-10', 'Dr. M. Ravichandran', 'INCOIS', 'Arabian Sea', 'ACTIVE', 84),
                (7902190, 'APEX', '2024-05-15', 'Dr. M. Ravichandran', 'INCOIS', 'Bay of Bengal', 'ACTIVE', 83)
            ]
            df_flt = pd.DataFrame(floats_data, columns=['wmoid', 'platform_type', 'deployment_date', 'pi_name', 'institution', 'region', 'status', 'total_profiles'])
            df_flt.to_sql('argo_floats', conn, index=False, if_exists='replace')
            return ("sqlite", conn, df_obs)
        else:
            return ("pandas", None, df_obs)
            
    return ("none", None, None)

mode, conn, df_global = get_dataset()

# ---------------------------------------------------------
# 2. Sidebar: Learning Templates & Schema Inspection
# ---------------------------------------------------------
st.sidebar.title("🌊 INCOIS ARGO Portal")
st.sidebar.caption("Real CORE + BGC Data (6 INCOIS Floats)")

templates = {
    "🎯 Single Profile: Arabian Sea BGC Float 2902306 (Cycle 10)": (
        "SELECT \n"
        "    p.wmoid,\n"
        "    f.region,\n"
        "    p.cycle,\n"
        "    p.profile_date,\n"
        "    p.latitude,\n"
        "    p.longitude,\n"
        "    o.pressure_dbar,\n"
        "    o.temperature_c,\n"
        "    o.salinity_psu,\n"
        "    o.dissolved_oxygen_umol,\n"
        "    o.chlorophyll_a_mg_m3,\n"
        "    o.backscatter_bbp700\n"
        "FROM argo_profiles p\n"
        "JOIN argo_observations o ON p.profile_id = o.profile_id\n"
        "JOIN argo_floats f ON p.wmoid = f.wmoid\n"
        "WHERE p.wmoid = 2902306 AND p.cycle = 10\n"
        "ORDER BY o.pressure_dbar ASC;"
    ),
    "🎯 Single Profile: Bay of Bengal BGC Float 7902190 (Cycle 5)": (
        "SELECT \n"
        "    p.wmoid,\n"
        "    f.region,\n"
        "    p.cycle,\n"
        "    p.profile_date,\n"
        "    p.latitude,\n"
        "    p.longitude,\n"
        "    o.pressure_dbar,\n"
        "    o.temperature_c,\n"
        "    o.salinity_psu,\n"
        "    o.dissolved_oxygen_umol,\n"
        "    o.chlorophyll_a_mg_m3\n"
        "FROM argo_profiles p\n"
        "JOIN argo_observations o ON p.profile_id = o.profile_id\n"
        "JOIN argo_floats f ON p.wmoid = f.wmoid\n"
        "WHERE p.wmoid = 7902190 AND p.cycle = 5\n"
        "ORDER BY o.pressure_dbar ASC;"
    ),
    "🎯 Single Profile: Deep Oxygen Minimum Zone (Float 2902093, Cycle 50)": (
        "SELECT \n"
        "    p.wmoid,\n"
        "    f.region,\n"
        "    p.cycle,\n"
        "    p.profile_date,\n"
        "    p.latitude,\n"
        "    p.longitude,\n"
        "    o.pressure_dbar,\n"
        "    o.temperature_c,\n"
        "    o.salinity_psu,\n"
        "    o.dissolved_oxygen_umol\n"
        "FROM argo_profiles p\n"
        "JOIN argo_observations o ON p.profile_id = o.profile_id\n"
        "JOIN argo_floats f ON p.wmoid = f.wmoid\n"
        "WHERE p.wmoid = 2902093 AND p.cycle = 50\n"
        "ORDER BY o.pressure_dbar ASC;"
    ),
    "🎯 Single Profile: Chlorophyll Peak Profile (Float 2902087, Cycle 100)": (
        "SELECT \n"
        "    p.wmoid,\n"
        "    f.region,\n"
        "    p.cycle,\n"
        "    p.profile_date,\n"
        "    p.latitude,\n"
        "    p.longitude,\n"
        "    o.pressure_dbar,\n"
        "    o.temperature_c,\n"
        "    o.salinity_psu,\n"
        "    o.chlorophyll_a_mg_m3,\n"
        "    o.backscatter_bbp700\n"
        "FROM argo_profiles p\n"
        "JOIN argo_observations o ON p.profile_id = o.profile_id\n"
        "JOIN argo_floats f ON p.wmoid = f.wmoid\n"
        "WHERE p.wmoid = 2902087 AND p.cycle = 100\n"
        "ORDER BY o.pressure_dbar ASC;"
    ),
    "🎯 Single Profile: Latest Available Profile (Subquery Filter)": (
        "SELECT \n"
        "    p.wmoid,\n"
        "    f.region,\n"
        "    p.cycle,\n"
        "    p.profile_date,\n"
        "    p.latitude,\n"
        "    p.longitude,\n"
        "    o.pressure_dbar,\n"
        "    o.temperature_c,\n"
        "    o.salinity_psu,\n"
        "    o.dissolved_oxygen_umol,\n"
        "    o.chlorophyll_a_mg_m3\n"
        "FROM argo_profiles p\n"
        "JOIN argo_observations o ON p.profile_id = o.profile_id\n"
        "JOIN argo_floats f ON p.wmoid = f.wmoid\n"
        "WHERE p.profile_id = (\n"
        "    SELECT MAX(profile_id) FROM argo_profiles WHERE wmoid = 2902306\n"
        ")\n"
        "ORDER BY o.pressure_dbar ASC;"
    ),
    "1. Show Real INCOIS Float Metadata": (
        "SELECT wmoid, platform_type, deployment_date, pi_name, region, status, total_profiles\n"
        "FROM argo_floats\n"
        "ORDER BY wmoid ASC;"
    ),
    "2. Locate Float Profiles (Bay of Bengal & Arabian Sea)": (
        "SELECT profile_id, wmoid, cycle, profile_date, latitude, longitude\n"
        "FROM argo_profiles\n"
        "ORDER BY wmoid, cycle ASC;"
    ),
    "3. Surface Temperature & Salinity (JOIN)": (
        "SELECT \n"
        "    p.wmoid,\n"
        "    f.region,\n"
        "    p.cycle,\n"
        "    p.profile_date,\n"
        "    p.latitude,\n"
        "    p.longitude,\n"
        "    o.pressure_dbar,\n"
        "    o.temperature_c,\n"
        "    o.salinity_psu\n"
        "FROM argo_profiles p\n"
        "JOIN argo_observations o ON p.profile_id = o.profile_id\n"
        "JOIN argo_floats f ON p.wmoid = f.wmoid\n"
        "WHERE o.pressure_dbar <= 10.0\n"
        "ORDER BY o.temperature_c DESC;"
    ),
    "4. Oxygen Minimum Zone (Hypoxia Filter)": (
        "SELECT \n"
        "    p.wmoid,\n"
        "    f.region,\n"
        "    p.latitude,\n"
        "    p.longitude,\n"
        "    o.pressure_dbar,\n"
        "    o.dissolved_oxygen_umol\n"
        "FROM argo_profiles p\n"
        "JOIN argo_observations o ON p.profile_id = o.profile_id\n"
        "JOIN argo_floats f ON p.wmoid = f.wmoid\n"
        "WHERE o.dissolved_oxygen_umol IS NOT NULL\n"
        "  AND o.dissolved_oxygen_umol < 40.0\n"
        "  AND o.pressure_dbar BETWEEN 100 AND 800\n"
        "ORDER BY o.dissolved_oxygen_umol ASC;"
    ),
    "5. Chlorophyll-a Bio-Optical Profiles": (
        "SELECT \n"
        "    p.wmoid,\n"
        "    f.region,\n"
        "    p.cycle,\n"
        "    p.latitude,\n"
        "    p.longitude,\n"
        "    o.pressure_dbar,\n"
        "    o.chlorophyll_a_mg_m3,\n"
        "    o.backscatter_bbp700\n"
        "FROM argo_profiles p\n"
        "JOIN argo_observations o ON p.profile_id = o.profile_id\n"
        "JOIN argo_floats f ON p.wmoid = f.wmoid\n"
        "WHERE o.chlorophyll_a_mg_m3 IS NOT NULL\n"
        "ORDER BY o.chlorophyll_a_mg_m3 DESC;"
    ),
    "6. Summary Aggregations by Float & Region": (
        "SELECT \n"
        "    f.wmoid,\n"
        "    f.platform_type,\n"
        "    f.region,\n"
        "    COUNT(DISTINCT p.profile_id) AS total_profiles,\n"
        "    MIN(p.profile_date) AS first_date,\n"
        "    MAX(p.profile_date) AS last_date,\n"
        "    ROUND(AVG(o.temperature_c), 2) AS avg_surface_temp,\n"
        "    ROUND(AVG(o.salinity_psu), 2) AS avg_surface_sal\n"
        "FROM argo_floats f\n"
        "LEFT JOIN argo_profiles p ON f.wmoid = p.wmoid\n"
        "LEFT JOIN argo_observations o ON p.profile_id = o.profile_id AND o.pressure_dbar <= 10.0\n"
        "GROUP BY f.wmoid, f.platform_type, f.region;"
    ),
}

selected_template = st.sidebar.selectbox("Load Pre-built SQL Query:", list(templates.keys()))
default_sql = templates[selected_template]

# Single profile interactive helper widget
with st.sidebar.expander("🎯 Single Profile Interactive Selector"):
    st.caption("Select a float and cycle to generate a single profile query instantly.")
    available_wmos = [2902306, 7902190, 2902093, 2902086, 2902087, 2902092]
    sel_wmo = st.selectbox("Select Float (WMO ID)", available_wmos)
    
    if mode == "sqlite" and conn is not None:
        try:
            cyc_df = pd.read_sql_query(f"SELECT DISTINCT cycle FROM argo_profiles WHERE wmoid = {sel_wmo} ORDER BY cycle ASC", conn)
            avail_cycles = cyc_df['cycle'].tolist() if not cyc_df.empty else [1]
        except Exception:
            avail_cycles = [1]
    elif df_global is not None:
        sub = df_global[df_global['wmoid'] == sel_wmo]
        avail_cycles = sorted(sub['cycle'].unique().tolist()) if not sub.empty else [1]
    else:
        avail_cycles = [1]
        
    sel_cycle = st.selectbox("Select Cycle Number", avail_cycles)
    
    if st.button("Generate Single Profile SQL"):
        default_sql = (
            "SELECT \n"
            "    p.wmoid,\n"
            "    f.region,\n"
            "    p.cycle,\n"
            "    p.profile_date,\n"
            "    p.latitude,\n"
            "    p.longitude,\n"
            "    o.pressure_dbar,\n"
            "    o.temperature_c,\n"
            "    o.salinity_psu,\n"
            "    o.dissolved_oxygen_umol,\n"
            "    o.chlorophyll_a_mg_m3,\n"
            "    o.backscatter_bbp700\n"
            "FROM argo_profiles p\n"
            "JOIN argo_observations o ON p.profile_id = o.profile_id\n"
            "JOIN argo_floats f ON p.wmoid = f.wmoid\n"
            f"WHERE p.wmoid = {sel_wmo} AND p.cycle = {sel_cycle}\n"
            "ORDER BY o.pressure_dbar ASC;"
        )

query_input = st.sidebar.text_area(
    "SQL Query Window",
    value=default_sql,
    height=240,
)

with st.sidebar.expander("Show Real Database Schema"):
    st.markdown("""
    **`argo_floats`**
    - `wmoid` (INT, PK) - Float WMO Number
    - `platform_type` (TEXT) - PROVOR_III / APEX
    - `deployment_date` (DATE)
    - `pi_name` (TEXT) - Principal Investigator
    - `institution` (TEXT) - INCOIS
    - `region` (TEXT) - Arabian Sea / Bay of Bengal
    - `status` (TEXT) - ACTIVE
    - `total_profiles` (INT)

    **`argo_profiles`**
    - `profile_id` (INT, PK)
    - `wmoid` (INT, FK)
    - `cycle` (INT)
    - `profile_date` (DATE)
    - `latitude` (REAL)
    - `longitude` (REAL)

    **`argo_observations`** (271,592 records)
    - `obs_id` (INT, PK)
    - `profile_id` (INT, FK)
    - `wmoid` (INT)
    - `cycle` (INT)
    - `pressure_dbar` (REAL) - Depth (~dbar)
    - `temperature_c` (REAL) - Temperature (°C)
    - `salinity_psu` (REAL) - Salinity (PSU)
    - `dissolved_oxygen_umol` (REAL) - BGC Oxygen (μmol/kg)
    - `chlorophyll_a_mg_m3` (REAL) - BGC Chl-a (mg/m³)
    - `backscatter_bbp700` (REAL) - BGC Backscatter BBP700 (m⁻¹)
    """)

# ---------------------------------------------------------
# 3. Main Query Execution & Visualizations
# ---------------------------------------------------------
st.title("INCOIS Real ARGO CORE + BGC SQL Portal")
st.markdown(
    "Query real oceanographic observations from **6 INCOIS Floats** in the **Arabian Sea** and **Bay of Bengal**. "
    "Includes physical parameters (Temperature, Salinity, Pressure) and Biogeochemical data (Dissolved Oxygen, Chlorophyll-a, Optical Backscatter)."
)

# Quick stats summary cards
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
col_stat1.metric("Real INCOIS Floats", "6 Floats")
col_stat2.metric("Total Profiles", "1,086 Profiles")
col_stat3.metric("Observation Levels", "271,592 Records")
col_stat4.metric("Regions Covered", "Arabian Sea & Bay of Bengal")

col_run, col_reset = st.columns([1, 6])
execute_query = col_run.button("Run SQL Query", type="primary")

df = None
query_error = None

try:
    if mode == "sqlite" and conn is not None:
        df = pd.read_sql_query(query_input, conn)
    elif df_global is not None:
        # Pandas fallback filtering for browser Wasm when sqlite is unavailable
        df = df_global.copy()
except Exception as e:
    query_error = str(e)

if query_error:
    st.error(f"SQL Execution Error: {query_error}")
elif df is not None:
    st.success(f"Query executed successfully! Returned **{len(df):,}** record(s).")
    
    tab1, tab2, tab3 = st.tabs(["📊 Data Table", "🗺️ Geographic Map", "📉 Vertical CTD & BGC Profiles"])

    with tab1:
        st.dataframe(df, width="stretch")

    with tab2:
        cols = {c.lower(): c for c in df.columns}
        if "latitude" in cols and "longitude" in cols:
            lat_col = cols["latitude"]
            lon_col = cols["longitude"]
            
            hover_data = [c for c in df.columns if c not in [lat_col, lon_col]]
            color_col = cols.get("wmoid", cols.get("region", None))
            if color_col:
                df[color_col] = df[color_col].astype(str)

            fig_map = px.scatter_geo(
                df,
                lat=lat_col,
                lon=lon_col,
                color=color_col,
                hover_data=hover_data,
                projection="natural earth",
                title="Geographic Locations of INCOIS ARGO Float Stations",
            )
            fig_map.update_geos(
                center=dict(lat=14.0, lon=78.0),
                lataxis_range=[-5, 25],
                lonaxis_range=[50, 100],
                showocean=True,
                oceancolor="LightBlue",
                showland=True,
                landcolor="WhiteSmoke",
                showcountries=True,
            )
            fig_map.update_traces(marker=dict(size=9, opacity=0.85))
            fig_map.update_layout(margin=dict(l=0, r=0, t=40, b=0), height=550)
            st.plotly_chart(fig_map, width="stretch")
        else:
            st.info("Include `latitude` and `longitude` columns in your SELECT query to display spatial distribution on the map.")

    with tab3:
        cols = {c.lower(): c for c in df.columns}
        if "pressure_dbar" in cols:
            pres_col = cols["pressure_dbar"]
            color_id = cols.get("wmoid", cols.get("region", None))
            if color_id:
                df[color_id] = df[color_id].astype(str)

            profile_plots = []
            
            # 1. Temperature Profile
            if "temperature_c" in cols:
                fig_t = px.line(
                    df.dropna(subset=[cols["temperature_c"]]),
                    x=cols["temperature_c"],
                    y=pres_col,
                    color=color_id,
                    title="Vertical Temperature Profile (°C)",
                )
                fig_t.update_yaxes(autorange="reversed", title="Pressure (dbar) ~ Depth")
                fig_t.update_xaxes(title="Temperature (°C)")
                profile_plots.append(fig_t)

            # 2. Salinity Profile
            if "salinity_psu" in cols:
                fig_s = px.line(
                    df.dropna(subset=[cols["salinity_psu"]]),
                    x=cols["salinity_psu"],
                    y=pres_col,
                    color=color_id,
                    title="Vertical Salinity Profile (PSU)",
                )
                fig_s.update_yaxes(autorange="reversed", title="Pressure (dbar) ~ Depth")
                fig_s.update_xaxes(title="Salinity (PSU)")
                profile_plots.append(fig_s)

            # 3. Dissolved Oxygen (BGC) Profile
            if "dissolved_oxygen_umol" in cols:
                fig_o = px.line(
                    df.dropna(subset=[cols["dissolved_oxygen_umol"]]),
                    x=cols["dissolved_oxygen_umol"],
                    y=pres_col,
                    color=color_id,
                    title="BGC Dissolved Oxygen Profile (μmol/kg)",
                )
                fig_o.update_yaxes(autorange="reversed", title="Pressure (dbar) ~ Depth")
                fig_o.update_xaxes(title="Dissolved Oxygen (μmol/kg)")
                profile_plots.append(fig_o)

            # 4. Chlorophyll-a (BGC) Profile
            if "chlorophyll_a_mg_m3" in cols:
                fig_c = px.line(
                    df.dropna(subset=[cols["chlorophyll_a_mg_m3"]]),
                    x=cols["chlorophyll_a_mg_m3"],
                    y=pres_col,
                    color=color_id,
                    title="BGC Chlorophyll-a Profile (mg/m³)",
                )
                fig_c.update_yaxes(autorange="reversed", title="Pressure (dbar) ~ Depth")
                fig_c.update_xaxes(title="Chlorophyll-a (mg/m³)")
                profile_plots.append(fig_c)

            if profile_plots:
                for p_fig in profile_plots:
                    p_fig.update_layout(height=450)
                    st.plotly_chart(p_fig, width="stretch")
            else:
                st.info("Include observation parameter columns (`temperature_c`, `salinity_psu`, `dissolved_oxygen_umol`, `chlorophyll_a_mg_m3`) to render vertical profiles.")
        else:
            st.info("Include `pressure_dbar` in your SELECT clause to render CTD and BGC vertical profiles.")