import streamlit as st
from config import FORMS
from utils import load_odk_data

st.set_page_config(page_title="Rainfed Fisheries", layout="wide")

st.sidebar.title("Menu")

menu_items = ["MIS-Status"] + list(FORMS.keys())
page = st.sidebar.radio("Go to", menu_items)

# ---------------- MIS STATUS ----------------
if page == "MIS-Status":
    import pandas as pd
    import calendar

    st.title("📊 MIS Tracking - Rainfed Fisheries")

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
