import streamlit as st
import pandas as pd
from datetime import datetime

from database import (
    create_database,
    save_article,
    get_articles,
    clear_database
)

from news_engine import (
    collect_news
)

from market_data import (
    get_market_data
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title=
        "Daily Finance Intelligence",

    page_icon=
        "📈",

    layout=
        "wide"

)


# ============================================================
# DATABASE
# ============================================================

create_database()


# ============================================================
# HEADER
# ============================================================

st.title(
    "📈 Daily Finance Intelligence"
)

st.caption(
    "Global finance, economy, markets, business and management briefing"
)

today = datetime.now().strftime(
    "%d %B %Y"
)

st.write(
    today
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "Controls"
)


if st.sidebar.button(
    "🔄 Fetch Latest News",
    use_container_width=True
):

    with st.spinner(
        "Collecting and analysing news..."
    ):

        articles = collect_news()

        inserted = 0

        for article in articles:

            if save_article(
                article
            ):

                inserted += 1

    st.sidebar.success(
        f"{inserted} new stories added."
    )


if st.sidebar.button(
    "🗑️ Clear Database",
    use_container_width=True
):

    clear_database()

    st.sidebar.success(
        "Database cleared."
    )

    st.rerun()


# ============================================================
# LOAD ARTICLES
# ============================================================

df = get_articles()


if df.empty:

    st.info(
        "Click 'Fetch Latest News' to collect today's news."
    )

    st.stop()


# ============================================================
# MARKET SNAPSHOT
# ============================================================

st.header(
    "Market Snapshot"
)


with st.spinner(
    "Loading market data..."
):

    market_df = get_market_data()


if not market_df.empty:

    columns = st.columns(
        min(
            len(market_df),
            6
        )
    )

    for i, row in market_df.head(6).iterrows():

        with columns[
            i % len(columns)
        ]:

            change = row["change"]

            st.metric(

                row["name"],

                row["price"],

                f"{change}%"

            )


# ============================================================
# FILTERS
# ============================================================

st.header(
    "News Filters"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    categories = [
        "All"
    ] + sorted(
        df["category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_category = st.selectbox(
        "Category",
        categories
    )


with col2:

    regions = [
        "All"
    ] + sorted(
        df["region"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_region = st.selectbox(
        "Region",
        regions
    )


with col3:

    importance = st.slider(
        "Minimum importance",
        1,
        10,
        1
    )


with col4:

    number_of_stories = st.slider(
        "Stories",
        5,
        30,
        10
    )


filtered = df.copy()


if selected_category != "All":

    filtered = filtered[
        filtered["category"]
        ==
        selected_category
    ]


if selected_region != "All":

    filtered = filtered[
        filtered["region"]
        ==
        selected_region
    ]


filtered = filtered[
    filtered["importance"]
    >=
    importance
]


filtered = filtered.sort_values(
    "importance",
    ascending=False
)


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

st.header(
    "Today's Executive Summary"
)


top = filtered.head(
    number_of_stories
)


if not top.empty:

    highest = top.iloc[0]

    st.info(
        f"""
        The most important story today is:

        {highest["title"]}

        {highest["summary"]}
        """
    )


# ============================================================
# TOP STORIES
# ============================================================

st.header(
    "Top Stories"
)


for position, (_, article) in enumerate(
    top.iterrows(),
    start=1
):

    st.subheader(
        f"{position}. {article['title']}"
    )

    col1, col2 = st.columns(
        [4, 1]
    )

    with col1:

        st.write(
            f"Source: {article['source']}"
        )

        st.write(
            f"Category: {article['category']} | "
            f"Region: {article['region']}"
        )

    with col2:

        st.metric(
            "Importance",
            f"{article['importance']}/10"
        )

    st.write(
        "WHAT HAPPENED"
    )

    st.write(
        article["summary"]
    )

    st.write(
        "WHY IT MATTERS"
    )

    st.write(
        article["why_it_matters"]
    )

    st.write(
        "IMPACT ON INDIA"
    )

    st.write(
        article["india_impact"]
    )

    st.write(
        "MARKET IMPACT"
    )

    st.write(
        article["market_impact"]
    )

    st.write(
        "WHAT TO WATCH"
    )

    st.write(
        article["what_to_watch"]
    )

    st.link_button(
        "Read Original Article",
        article["url"]
    )

    st.divider()


# ============================================================
# CATEGORY BREAKDOWN
# ============================================================

st.header(
    "News by Category"
)


category_data = (
    filtered["category"]
    .value_counts()
)


st.bar_chart(
    category_data
)


# ============================================================
# REGIONAL BREAKDOWN
# ============================================================

st.header(
    "News by Region"
)


region_data = (
    filtered["region"]
    .value_counts()
)


st.bar_chart(
    region_data
)


# ============================================================
# DAILY TAKEAWAYS
# ============================================================

st.header(
    "Top 5 Takeaways"
)


for i, (_, article) in enumerate(
    top.head(5).iterrows(),
    start=1
):

    st.write(
        f"{i}. {article['title']}"
    )

    st.caption(
        article["why_it_matters"]
    )


# ============================================================
# DOWNLOAD
# ============================================================

st.header(
    "Export"
)


csv_data = filtered.to_csv(
    index=False
)


st.download_button(

    label=
        "Download Today's News",

    data=
        csv_data,

    file_name=
        f"finance_news_{datetime.now().strftime('%Y%m%d')}.csv",

    mime=
        "text/csv"

)