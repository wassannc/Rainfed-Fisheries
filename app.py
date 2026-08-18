import streamlit as st
from config import FORMS
from utils import load_odk_data, load_entities
import pandas as pd
import calendar
from pathlib import Path
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

# ---------------- COMMON FILTERS ----------------
all_districts=set()
for _,config in FORMS.items():
    try:
        _df=load_odk_data(config["form_id"])
        dc=config.get("district_col")
        if dc and dc in _df.columns:
            all_districts.update(_df[dc].dropna().unique())
    except:
        pass
all_districts=sorted(all_districts)
st.sidebar.markdown("### Filters")
selected_districts = st.sidebar.multiselect("District",options=all_districts,default=all_districts,key="district_filter")
months = [calendar.month_name[i] for i in range(1,13)]
selected_months = st.sidebar.multiselect(
    "Month",
    options=months,
    default=months,
    key="month_filter"
)

def apply_filters(df,district_col=None):
    if df is None or df.empty:
        return df
    
    if district_col and district_col in df.columns:
        df = df[df[district_col].isin(selected_districts)]
    date_col = "SubmissionDate" if "SubmissionDate" in df.columns else None
        
    if selected_months and date_col:
        df=df.copy()
        df[date_col]=pd.to_datetime(df[date_col],errors="coerce")
        month_numbers = [
            list(calendar.month_name).index(month)
            for month in selected_months
        ]
        df = df[df[date_col].dt.month.isin(month_numbers)]
    return df

    
# ---------------- MIS STATUS ----------------
if page == "MIS-Status":

    st.title("🐟 Rainfed Fisheries")

    # ---------------- DATA DISPLAY ----------------
    forms_list = list(FORMS.items())
    cols_per_row = 2

    BASE_DIR = Path(__file__).parent

    FORM_ICONS = {
        "1. Fingerlings Release": BASE_DIR / "icons" / "fingerling.png",
        "2. Mortality Check": BASE_DIR / "icons" / "mortality.png",
        "3. Feeding": BASE_DIR / "icons" / "feed.png",
        "4. Trailnet": BASE_DIR / "icons" / "trail.png",
        "5. Harvesting": BASE_DIR / "icons" / "harvest.png",
    }

    for i in range(0, len(forms_list), cols_per_row):

        cols = st.columns(cols_per_row)

        for j in range(cols_per_row):

            if i + j >= len(forms_list):
                break

            form_name, config = forms_list[i + j]

            df = load_odk_data(config["form_id"])

            district_col = config.get("district_col")

            df = apply_filters(df, district_col)

            # -------- UI --------
            with cols[j]:

                # -------- FORM TITLE + ICON --------
                icon = FORM_ICONS.get(form_name)

                title_col1, title_col2 = st.columns([0.12, 0.88])

                with title_col1:
                    if icon and icon.exists():
                        st.image(str(icon), width=32)

                with title_col2:
                    st.markdown(f"#### {form_name}")

                # -------- DATA --------
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

                    st.dataframe(
                        grouped,
                        use_container_width=True,
                        height=200
                    )

                else:
                    st.warning(f"{district_col} not found")
                    
# ---------------- REPORTS ----------------
elif page in FORMS:
    st.title(f"📥 {page} Data")

    config = FORMS[page]
    df = load_odk_data(config["form_id"])
    district_col = config.get("district_col")
    df = apply_filters(df, district_col)

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
    import plotly.express as px

    st.title("🐟 Rainfed Fisheries")

    if st.button("🔄 Refresh Data", key="dashboard_refresh"):
        st.cache_data.clear()
        st.rerun()

    # ---------------- LOAD DATA ----------------
    df_release = load_odk_data(FORMS["1. Fingerlings Release"]["form_id"])
    df_mort = load_odk_data(FORMS["2. Mortality Check"]["form_id"])
    df_feed = load_odk_data(FORMS["3. Feeding"]["form_id"])
    df_trail = load_odk_data(FORMS["4. Trailnet"]["form_id"])
    df_harvest = load_odk_data(FORMS["5. Harvesting"]["form_id"])

    # ---------------- APPLY FILTERS ----------------
    df_release = apply_filters(df_release, "pd-district")
    df_mort = apply_filters(df_mort, "pd-district")
    df_feed = apply_filters(df_feed, "pd-district")
    df_trail = apply_filters(df_trail, "pd-district")
    df_harvest = apply_filters(df_harvest, "pd-district")

    # ---------------- KPI VALUES ----------------
    total_ponds = (
        df_release["fingerlings-fish_farmer"].nunique()
        if not df_release.empty and "fingerlings-fish_farmer" in df_release.columns
        else 0
    )

    if not df_release.empty and "fingerlings-ext_pond" in df_release.columns:
        df_release["fingerlings-ext_pond"] = pd.to_numeric(
            df_release["fingerlings-ext_pond"], errors="coerce"
        )
        total_extent = df_release["fingerlings-ext_pond"].sum()
    else:
        total_extent = 0

    total_mortality = len(df_mort)
    total_trailnet = len(df_trail)

    kg_col = "harvest-fish_sold_kgs"

    if not df_harvest.empty and kg_col in df_harvest.columns:
        df_harvest[kg_col] = pd.to_numeric(df_harvest[kg_col], errors="coerce")
        total_harvest_kg = df_harvest[kg_col].sum()
    else:
        total_harvest_kg = 0

    # ---------------- KPI CARDS ----------------
    st.subheader("📊 Key Indicators")

    k1, k2, k3, k4, k5 = st.columns(5)

    k1.metric("🐟 Ponds", f"{total_ponds:,}")
    k2.metric("📐 Pond Extent", f"{total_extent:,.2f} ac")
    k3.metric("🎣 Harvest", f"{total_harvest_kg:,.0f} kg")
    k4.metric("💀 Mortality Checked", f"{total_mortality:,}")
    k5.metric("🎓 Trailnet Done", f"{total_trailnet:,}")

    st.divider()

    # ---------------- COVERAGE ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Ponds by District")

        if not df_release.empty and "pd-district" in df_release.columns and "fingerlings-fish_farmer" in df_release.columns:
            district_ponds = (
                df_release.groupby("pd-district")["fingerlings-fish_farmer"]
                .nunique()
                .reset_index(name="Ponds")
                .sort_values("Ponds", ascending=False)
            )

            fig = px.bar(
                district_ponds,
                x="pd-district",
                y="Ponds",
                text="Ponds",
                labels={"pd-district": "District", "Ponds": "Number of Ponds"}
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)

            st.plotly_chart(fig, use_container_width=True, key="ponds_by_district")
        else:
            st.info("No pond data available.")

    with col2:
        st.subheader("🎣 Harvest by District")

        if not df_harvest.empty and "pd-district" in df_harvest.columns and kg_col in df_harvest.columns:
            harvest_district = (
                df_harvest.groupby("pd-district")[kg_col]
                .sum()
                .reset_index(name="Harvest KG")
                .sort_values("Harvest KG", ascending=False)
            )

            fig = px.bar(
                harvest_district,
                x="pd-district",
                y="Harvest KG",
                text="Harvest KG",
                labels={"pd-district": "District", "Harvest KG": "Harvest (kg)"}
            )
            fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
            fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)

            st.plotly_chart(fig, use_container_width=True, key="harvest_by_district")
        else:
            st.info("No harvest data available.")

    # ---------------- EXTENT + ACTIVITY ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📐 Pond Extent by District")

        if not df_release.empty and "pd-district" in df_release.columns and "fingerlings-ext_pond" in df_release.columns:
            extent_district = (
                df_release.groupby("pd-district")["fingerlings-ext_pond"]
                .sum()
                .reset_index(name="Extent")
                .sort_values("Extent", ascending=False)
            )

            fig = px.bar(
                extent_district,
                x="pd-district",
                y="Extent",
                text="Extent",
                labels={"pd-district": "District", "Extent": "Extent (Acres)"}
            )
            fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
            fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)

            st.plotly_chart(fig, use_container_width=True, key="pond_extent_by_district")
        else:
            st.info("No pond extent data available.")

    with col2:
        st.subheader("📊 Activity by District")

        activity_data = []

        for data, label in [
            (df_release, "Fingerlings Release"),
            (df_mort, "Mortality Check"),
            (df_trail, "Trailnet"),
        ]:
            if not data.empty and "pd-district" in data.columns:
                temp = data.groupby("pd-district").size().reset_index(name="Count")
                temp["Activity"] = label
                activity_data.append(temp)

        if activity_data:
            activity_df = pd.concat(activity_data, ignore_index=True)

            fig = px.bar(
                activity_df,
                x="pd-district",
                y="Count",
                color="Activity",
                barmode="group",
                labels={"pd-district": "District", "Count": "Records"}
            )
            fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), legend_title_text="")

            st.plotly_chart(fig, use_container_width=True, key="activity_by_district")
        else:
            st.info("No activity data available.")

    # ---------------- FEEDING ----------------
    st.divider()
    st.subheader("🌾 Feeding Performance")

    if not df_feed.empty:
        district_col = "pd-district"
        block_col = "pd-block"
        farmer_col = "pd-fish_farmer"

        farmer_counts = (
            df_feed.groupby([district_col, block_col, farmer_col])
            .size()
            .reset_index(name="feed_times")
        )

        def classify_feed(months):
            if months >= 6:
                return "Regular"
            elif months >= 3:
                return "Moderate"
            elif months >= 1:
                return "Poor"
            return "No Feed"

        farmer_counts["feed_category"] = farmer_counts["feed_times"].apply(classify_feed)

        feed_summary = (
            farmer_counts["feed_category"]
            .value_counts()
            .reindex(["Regular", "Moderate", "Poor", "No Feed"], fill_value=0)
            .reset_index()
        )
        feed_summary.columns = ["Feed Category", "Count"]

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                feed_summary,
                x="Feed Category",
                y="Count",
                text="Count",
                labels={"Feed Category": "", "Count": "Number of Ponds"}
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)

            st.plotly_chart(fig, use_container_width=True, key="feeding_frequency")

        with col2:
            pie_data = feed_summary[feed_summary["Count"] > 0]

            if not pie_data.empty:
                fig = px.pie(pie_data, names="Feed Category", values="Count", hole=0.55)
                fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20))

                st.plotly_chart(fig, use_container_width=True, key="feeding_distribution")
            else:
                st.info("No feeding categories available.")

        st.write("#### 📍 Feeding Performance by Block")

        block_perf = (
            farmer_counts.groupby(["pd-block", "feed_category"])
            .size()
            .reset_index(name="Count")
        )

        fig = px.bar(
            block_perf,
            x="pd-block",
            y="Count",
            color="feed_category",
            barmode="stack",
            labels={"pd-block": "Block", "Count": "Ponds", "feed_category": "Feed Category"}
        )
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=20))

        st.plotly_chart(fig, use_container_width=True, key="feeding_block_performance")
    else:
        st.info("No feeding data available.")

    # ---------------- FEED VS YIELD ----------------
    st.divider()
    st.subheader("🧠 Feed vs Yield Intelligence")

    if (
        not df_feed.empty
        and not df_harvest.empty
        and "pd-fish_farmer" in df_feed.columns
        and "pd-fish_farmer" in df_harvest.columns
        and kg_col in df_harvest.columns
    ):
        feed_summary_pond = (
            df_feed.groupby("pd-fish_farmer")
            .size()
            .reset_index(name="feed_times")
        )

        harvest_summary = (
            df_harvest.groupby("pd-fish_farmer")
            .agg(total_kg=(kg_col, "sum"))
            .reset_index()
        )

        pond_df = feed_summary_pond.merge(
            harvest_summary,
            on="pd-fish_farmer",
            how="left"
        )

        pond_df["yield_status"] = pond_df["total_kg"].apply(
            lambda x: "No Data" if pd.isna(x) or x == 0 else "Available"
        )
        pond_df["total_kg"] = pond_df["total_kg"].fillna(0)
        pond_df["feed_category"] = pond_df["feed_times"].apply(classify_feed)

        yield_df = pond_df[pond_df["yield_status"] == "Available"]

        if not yield_df.empty:
            yield_summary = (
                yield_df.groupby("feed_category")["total_kg"]
                .mean()
                .reindex(["Regular", "Moderate", "Poor", "No Feed"])
                .dropna()
                .reset_index()
            )
            yield_summary.columns = ["Feed Category", "Average Yield"]

            fig = px.bar(
                yield_summary,
                x="Feed Category",
                y="Average Yield",
                text="Average Yield",
                labels={"Feed Category": "Feed Category", "Average Yield": "Average Harvest (kg)"}
            )
            fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
            fig.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)

            st.plotly_chart(fig, use_container_width=True, key="feed_vs_yield")
        else:
            st.info("No harvest data available for feed vs yield analysis.")
    else:
        st.info("Insufficient data for feed vs yield analysis.")

    # ---------------- ACTION STATUS ----------------
    if (
        not df_feed.empty
        and not df_harvest.empty
        and "pd-fish_farmer" in df_feed.columns
        and "pd-fish_farmer" in df_harvest.columns
        and kg_col in df_harvest.columns
    ):
        feed_summary_action = (
            df_feed.groupby("pd-fish_farmer")
            .size()
            .reset_index(name="feed_times")
        )

        harvest_summary_action = (
            df_harvest.groupby("pd-fish_farmer")
            .agg(total_kg=(kg_col, "sum"))
            .reset_index()
        )

        action_df = feed_summary_action.merge(
            harvest_summary_action,
            on="pd-fish_farmer",
            how="left"
        )

        action_df["total_kg"] = action_df["total_kg"].fillna(0)
        action_df["yield_status"] = action_df["total_kg"].apply(
            lambda x: "No Data" if x == 0 else "Available"
        )

        def advanced_trigger(row):
            if row["yield_status"] == "No Data":
                return "No Harvest Data"
            if row["feed_times"] <= 2 and row["total_kg"] < 50:
                return "Critical"
            elif row["feed_times"] >= 5 and row["total_kg"] < 50:
                return "Technical Issue"
            elif row["feed_times"] <= 2:
                return "Low Feeding"
            return "Normal"

        action_df["Action"] = action_df.apply(advanced_trigger, axis=1)

        action_summary = (
            action_df["Action"]
            .value_counts()
            .reindex(
                ["Critical", "Technical Issue", "Low Feeding", "Normal", "No Harvest Data"],
                fill_value=0
            )
            .reset_index()
        )
        action_summary.columns = ["Action Status", "Count"]

        st.divider()
        st.subheader("🚨 Action Status")

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                action_summary,
                x="Action Status",
                y="Count",
                text="Count",
                labels={"Action Status": "", "Count": "Number of Ponds"}
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)

            st.plotly_chart(fig, use_container_width=True, key="action_status_bar")

        with col2:
            pie_action = action_summary[action_summary["Count"] > 0]

            if not pie_action.empty:
                fig = px.pie(
                    pie_action,
                    names="Action Status",
                    values="Count",
                    hole=0.55
                )
                fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20))

                st.plotly_chart(fig, use_container_width=True, key="action_status_donut")
            else:
                st.info("No action status available.")

    # ---------------- HARVESTING ----------------
    st.divider()
    st.subheader("🐟 Harvesting Performance")

    if (
        not df_harvest.empty
        and "pd-district" in df_harvest.columns
        and "pd-fish_farmer" in df_harvest.columns
        and kg_col in df_harvest.columns
    ):
        harvest_group = (
            df_harvest.groupby("pd-district")
            .agg(
                ponds_harvested=("pd-fish_farmer", "nunique"),
                total_kg=(kg_col, "sum")
            )
            .reset_index()
        )

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                harvest_group.sort_values("ponds_harvested", ascending=False),
                x="pd-district",
                y="ponds_harvested",
                text="ponds_harvested",
                labels={"pd-district": "District", "ponds_harvested": "Ponds Harvested"}
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="harvested_ponds_by_district"
            )

        with col2:
            fig = px.bar(
                harvest_group.sort_values("total_kg", ascending=False),
                x="pd-district",
                y="total_kg",
                text="total_kg",
                labels={"pd-district": "District", "total_kg": "Harvest (kg)"}
            )
            fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
            fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="harvest_kg_by_district"
            )
    else:
        st.info("No harvesting data available.")

