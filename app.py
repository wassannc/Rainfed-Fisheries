import streamlit as st
from config import FORMS
from utils import load_odk_data, load_entities
st.set_page_config(page_title="Rainfed Fisheries", layout="wide")

st.sidebar.title("Menu")

main_section = st.sidebar.radio(
    "Select Section",
    ["MIS-Status", "MIS-Reports", "Dashboard"]
)

# 👇 Form selection only when Reports selected
if main_section == "MIS-Reports":
    page = st.sidebar.radio("Select Form", list(FORMS.keys()))
else:
    page = main_section
    
# ---------------- MIS STATUS ----------------
if page == "MIS-Status":
    import pandas as pd
    import calendar

    st.title("📊 Rainfed Fisheries")

    # ---------------- FILTERS ----------------
    col1, col2 = st.columns(2)

    with col1:
        all_districts = set()

        for form_name, config in FORMS.items():
            df_temp = load_odk_data(config["form_id"])
            col = config.get("district_col")   # 🔥 changed

            if col and col in df_temp.columns:
                all_districts.update(df_temp[col].dropna().unique())

        all_districts = sorted(all_districts)

        selected_district = st.selectbox(
            "Select District",
            ["All"] + list(all_districts)
        )

    with col2:
        months = ["All"] + [calendar.month_name[i] for i in range(1, 13)]
        selected_month = st.selectbox("Select Month", months)

    # ---------------- DATA DISPLAY ----------------
    forms_list = list(FORMS.items())
    cols_per_row = 2

    for i in range(0, len(forms_list), cols_per_row):
        cols = st.columns(cols_per_row)

        for j in range(cols_per_row):
            if i + j >= len(forms_list):
                break

            form_name, config = forms_list[i + j]
            df = load_odk_data(config["form_id"])

            district_col = config.get("district_col")  # 🔥 changed

            # -------- APPLY FILTERS --------

            # District filter
            if selected_district != "All" and district_col in df.columns:
                df = df[df[district_col] == selected_district]

            # Month filter
            date_cols = ["__system.submissionDate", "meta.submissionDate"]
            date_col = None

            for col in date_cols:
                if col in df.columns:
                    date_col = col
                    break

            if selected_month != "All" and date_col:
                df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
                month_num = list(calendar.month_name).index(selected_month)
                df = df[df[date_col].dt.month == month_num]

            # -------- UI --------
            with cols[j]:
                st.markdown(f"#### 📦 {form_name}")

                if df.empty:
                    st.write("No data")
                    continue

                st.caption(f"Total: {len(df)}")

                if district_col and district_col in df.columns:
                    grouped = (
                        df.groupby(district_col)
                        .size()
                        .reset_index(name="Count")
                        .sort_values("Count", ascending=False)
                    )

                    grouped.columns = ["District", "Count"]

                    st.dataframe(grouped, use_container_width=True, height=200)

                else:
                    st.warning(f"{district_col} not found")


# ---------------- REPORTS ----------------
elif page in FORMS:
    st.title(f"📥 {page} Report")

    config = FORMS[page]
    df = load_odk_data(config["form_id"])

    if df.empty:
        st.warning("No data found")
    else:
        columns = config.get("columns", [])
        available_cols = [col for col in columns if col in df.columns]

        if not available_cols:
            st.error("No matching columns found")
            st.write("Available columns:", df.columns)
        else:
            df_filtered = df[available_cols]

            st.dataframe(df_filtered, use_container_width=True)

            st.download_button(
                "⬇ Download CSV",
                df_filtered.to_csv(index=False),
                f"{page}_report.csv",
                "text/csv"
            )
 
elif main_section == "Dashboard":
    import pandas as pd

    st.title("🐟 Dashboard")
    
    #Refresh data
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
        
    df_release = load_odk_data(FORMS["1. Fingerlings Release"]["form_id"])
    df_mort = load_odk_data(FORMS["2. Mortality Check"]["form_id"])
    df_feed = load_odk_data(FORMS["3. Feeding"]["form_id"])
    df_trail = load_odk_data(FORMS["4. Trailnet"]["form_id"])
    df_harvest = load_odk_data(FORMS["5. Harvesting"]["form_id"])

    # ---------------- COVERAGE ----------------
    st.subheader("📍 Coverage")

    col1, col2 = st.columns([3, 1])

    with col1:
        # Coverage table
        if not df_release.empty:
             # 🔥 FIX: convert to numeric
            df_release["fingerlings.ext_pond"] = pd.to_numeric(
                df_release["fingerlings.ext_pond"],
                errors="coerce"
            )
            grouped = df_release.groupby(["pd.district", "pd.block"]).agg(
                ponds=("fingerlings.fish_farmer", "count"),
                extent=("fingerlings.ext_pond", "sum")
            ).reset_index()

            grouped.columns = ["District", "Block", "No. of ponds", "Extent (Acres)"]
            st.dataframe(grouped, use_container_width=True)

    with col2:
        st.metric("🐟 Mortality Checked", len(df_mort))
        st.metric("🎓 Trailnet Done", len(df_trail))

    # 👉 VERY IMPORTANT: BREAK COLUMN FLOW
    st.divider()

    st.subheader("🌾 Feed Tracking")

    if not df_feed.empty:

        district_col = "pd.district"
        block_col = "pd.block"
        farmer_col = "pd.fish_farmer"

        # 🔥 Step 1: count feed records per farmer
        farmer_counts = (
            df_feed.groupby([district_col, block_col, farmer_col])
            .size()
            .reset_index(name="feed_times")
        )

        # 🔥 Step 2: count frequency (1 time, 2 times, etc.)
        freq_table = (
            farmer_counts.groupby([district_col, block_col, "feed_times"])
            .size()
            .reset_index(name="farmer_count")
        )

        # 🔥 Step 3: pivot table
        pivot = freq_table.pivot_table(
            index=[district_col, block_col],
            columns="feed_times",
            values="farmer_count",
            fill_value=0
        ).reset_index()

        # Rename columns
        pivot.columns.name = None
        pivot = pivot.rename(columns={
            district_col: "District",
            block_col: "Block"
        })

        # 🔥 Step 4: rename feed columns nicely
        pivot.columns = [
            "District", "Block"
        ] + [f"{int(col)} time" if col == 1 else f"{int(col)} times" for col in pivot.columns[2:]]

        # 🔥 Step 5: Add Total ponds (from release)
        df_release_group = df_release.groupby([district_col, block_col]).agg(
            ponds=("fingerlings.fish_farmer", "count")
        ).reset_index()

        df_release_group = df_release_group.rename(columns={
            district_col: "District",
            block_col: "Block"
        })

        final_df = pivot.merge(df_release_group, on=["District", "Block"], how="left")

        # Move ponds column to front
        cols = ["District", "Block", "ponds"] + [c for c in final_df.columns if c not in ["District", "Block", "ponds"]]
        final_df = final_df[cols]

        final_df = final_df.rename(columns={"ponds": "Total ponds released"})

        st.dataframe(final_df, use_container_width=True)

    # ---------------- HARVESTING ----------------
    st.subheader("🐟 Harvesting")

    if not df_harvest.empty:

        district_col = "pd.district"
        block_col = "pd.block"
        farmer_col = "pd.fish_farmer"

        # 🔥 STEP 1: KG column (UPDATE THIS NAME)
        kg_col = "harvest.fish_sold_kgs"

        if kg_col in df_harvest.columns:
            df_harvest[kg_col] = pd.to_numeric(df_harvest[kg_col], errors="coerce")

        # 🔥 STEP 2: Harvest aggregation
        harvest_group = df_harvest.groupby([district_col, block_col]).agg(
            ponds_harvested=(farmer_col, "nunique"),
            total_kg=(kg_col, "sum") if kg_col in df_harvest.columns else (farmer_col, "count")
        ).reset_index()

        # 🔥 STEP 3: Release aggregation (ponds released)
        release_group = df_release.groupby([district_col, block_col]).agg(
            ponds_released=("fingerlings.fish_farmer", "count")
        ).reset_index()

        # 🔥 STEP 4: Merge both
        final = release_group.merge(
            harvest_group,
            on=[district_col, block_col],
            how="left"
        ).fillna(0)

        # 🔥 STEP 5: Rename columns
        final.columns = [
            "District",
            "Block",
            "Total ponds released",
            "Total ponds harvested",
            "Total KGs harvested"
        ]

        # Optional formatting
        final["Total KGs harvested"] = final["Total KGs harvested"].round(2)

        st.dataframe(final, use_container_width=True)
