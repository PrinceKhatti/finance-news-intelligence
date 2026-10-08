import feedparser
import re
import hashlib

from bs4 import BeautifulSoup

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


RSS_FEEDS = {

    "Reuters Business":
        "https://feeds.reuters.com/reuters/businessNews",

    "Reuters World":
        "https://feeds.reuters.com/Reuters/worldNews",

    "CNBC Finance":
        "https://www.cnbc.com/id/10000664/device/rss/rss.html",

    "CNBC Business":
        "https://www.cnbc.com/id/10001147/device/rss/rss.html",

    "CNBC Economy":
        "https://www.cnbc.com/id/20910258/device/rss/rss.html",

    "MarketWatch":
        "https://feeds.marketwatch.com/marketwatch/topstories/",

    "Google Finance":
        "https://news.google.com/rss/search?q=finance",

    "Google Economy":
        "https://news.google.com/rss/search?q=economy",

    "Google Business":
        "https://news.google.com/rss/search?q=business",

    "Google M&A":
        "https://news.google.com/rss/search?q=mergers+acquisitions",

    "Google Management":
        "https://news.google.com/rss/search?q=management",

    "Google Banking":
        "https://news.google.com/rss/search?q=banking",

    "Google Markets":
        "https://news.google.com/rss/search?q=stock+market"

}


CATEGORIES = {

    "Economy": [

        "inflation",
        "gdp",
        "interest rate",
        "central bank",
        "monetary policy",
        "fiscal policy",
        "recession",
        "economic growth",
        "unemployment",
        "jobs",
        "rbi",
        "federal reserve",
        "fed",
        "ecb",
        "economy"

    ],

    "Finance": [

        "bank",
        "banking",
        "credit",
        "loan",
        "debt",
        "bond",
        "equity",
        "investment",
        "investor",
        "mutual fund",
        "private equity",
        "venture capital",
        "finance",
        "financial"

    ],

    "Markets": [

        "stock market",
        "stocks",
        "shares",
        "nifty",
        "sensex",
        "nasdaq",
        "s&p 500",
        "dow jones",
        "market",
        "volatility",
        "vix",
        "derivatives",
        "options",
        "futures",
        "forex",
        "currency",
        "rupee",
        "dollar"

    ],

    "Corporate": [

        "company",
        "earnings",
        "revenue",
        "profit",
        "loss",
        "ceo",
        "cfo",
        "ipo",
        "corporate",
        "layoffs",
        "restructuring",
        "business"

    ],

    "M&A": [

        "merger",
        "mergers",
        "acquisition",
        "acquisitions",
        "takeover",
        "buyout",
        "deal",
        "stake",
        "joint venture"

    ],

    "Management": [

        "management",
        "leadership",
        "strategy",
        "strategic",
        "ceo",
        "board",
        "employees",
        "workforce",
        "productivity",
        "corporate culture",
        "human resources"

    ],

    "Technology": [

        "artificial intelligence",
        "ai",
        "technology",
        "software",
        "semiconductor",
        "chip",
        "data center",
        "cloud",
        "automation",
        "machine learning"

    ],

    "Commodities": [

        "oil",
        "crude",
        "brent",
        "wti",
        "gold",
        "silver",
        "copper",
        "commodity",
        "commodities",
        "natural gas"

    ],

    "Geopolitics": [

        "war",
        "conflict",
        "sanctions",
        "tariff",
        "trade war",
        "geopolitical",
        "china",
        "russia",
        "ukraine",
        "iran",
        "middle east"

    ]

}


HIGH_IMPACT_WORDS = [

    "interest rate",
    "rate hike",
    "rate cut",
    "inflation",
    "recession",
    "default",
    "bankruptcy",
    "war",
    "sanctions",
    "tariff",
    "merger",
    "acquisition",
    "ipo",
    "earnings",
    "crisis",
    "central bank",
    "rbi",
    "federal reserve",
    "fed",
    "oil",
    "crude",
    "gdp",
    "unemployment"

]


def clean_text(text):

    if not text:
        return ""

    soup = BeautifulSoup(
        text,
        "html.parser"
    )

    text = soup.get_text(" ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def classify_article(
    title,
    description
):

    text = (
        title +
        " " +
        description
    ).lower()

    scores = {}

    for category, keywords in CATEGORIES.items():

        score = 0

        for keyword in keywords:

            if keyword in text:

                score += 1

        scores[category] = score

    category = max(
        scores,
        key=scores.get
    )

    if scores[category] == 0:

        category = "General"

    return category


def identify_region(
    title,
    description
):

    text = (
        title +
        " " +
        description
    ).lower()

    india_keywords = [

        "india",
        "indian",
        "rbi",
        "rupee",
        "nifty",
        "sensex",
        "mumbai",
        "delhi"

    ]

    us_keywords = [

        "us",
        "u.s.",
        "united states",
        "federal reserve",
        "fed",
        "wall street",
        "nasdaq",
        "s&p"

    ]

    europe_keywords = [

        "europe",
        "european",
        "ecb",
        "euro",
        "germany",
        "france",
        "uk",
        "britain"

    ]

    china_keywords = [

        "china",
        "chinese",
        "beijing",
        "yuan"

    ]

    if any(
        x in text
        for x in india_keywords
    ):

        return "India"

    if any(
        x in text
        for x in us_keywords
    ):

        return "United States"

    if any(
        x in text
        for x in europe_keywords
    ):

        return "Europe"

    if any(
        x in text
        for x in china_keywords
    ):

        return "China"

    return "Global"


def calculate_importance(
    title,
    description,
    source
):

    text = (
        title +
        " " +
        description
    ).lower()

    score = 1

    for keyword in HIGH_IMPACT_WORDS:

        if keyword in text:

            score += 2

    market_keywords = [

        "stock",
        "bond",
        "yield",
        "market",
        "nifty",
        "sensex",
        "nasdaq",
        "rupee",
        "dollar",
        "gold",
        "oil"

    ]

    for keyword in market_keywords:

        if keyword in text:

            score += 1

    if (
        "reuters"
        in source.lower()
    ):

        score += 2

    if (
        "cnbc"
        in source.lower()
    ):

        score += 1

    return min(
        score,
        10
    )


def create_summary(
    title,
    description
):

    description = clean_text(
        description
    )

    if not description:

        return (
            "The article reports "
            "a development related to "
            + title
            + "."
        )

    sentences = re.split(
        r"(?<=[.!?])\s+",
        description
    )

    sentences = [
        x.strip()
        for x in sentences
        if len(x.strip()) > 30
    ]

    if len(sentences) >= 2:

        return (
            sentences[0]
            + " "
            + sentences[1]
        )

    return description[:600]


def generate_analysis(
    title,
    description,
    category,
    region
):

    text = (
        title +
        " " +
        description
    ).lower()

    summary = create_summary(
        title,
        description
    )

    # WHY IT MATTERS

    why_it_matters = ""

    if category == "Economy":

        why_it_matters = (
            "This development can affect "
            "economic growth, inflation, "
            "interest rates, employment or "
            "business conditions."
        )

    elif category == "Finance":

        why_it_matters = (
            "This development can influence "
            "credit conditions, investment "
            "flows, financial institutions "
            "and the cost of capital."
        )

    elif category == "Markets":

        why_it_matters = (
            "This development can influence "
            "investor sentiment, asset prices, "
            "volatility and capital flows."
        )

    elif category == "Corporate":

        why_it_matters = (
            "The development provides information "
            "about corporate earnings, strategy, "
            "competition or business conditions."
        )

    elif category == "M&A":

        why_it_matters = (
            "The deal could change market share, "
            "competitive dynamics, costs or the "
            "strategic position of the companies involved."
        )

    elif category == "Management":

        why_it_matters = (
            "The decision could affect corporate "
            "strategy, employees, productivity, "
            "leadership or organizational performance."
        )

    elif category == "Technology":

        why_it_matters = (
            "The development could affect technology "
            "investment, productivity, competition "
            "and future business models."
        )

    elif category == "Commodities":

        why_it_matters = (
            "Commodity prices affect production costs, "
            "inflation, trade balances and corporate margins."
        )

    elif category == "Geopolitics":

        why_it_matters = (
            "Geopolitical developments can affect "
            "trade, supply chains, commodities, "
            "investment flows and market risk."
        )

    else:

        why_it_matters = (
            "The development could have implications "
            "for businesses, investors or the broader economy."
        )


    # INDIA IMPACT

    if region == "India":

        india_impact = (
            "The development has a direct connection "
            "to India and may influence Indian companies, "
            "markets or economic conditions."
        )

    elif any(
        x in text
        for x in [
            "oil",
            "crude",
            "energy"
        ]
    ):

        india_impact = (
            "India can be affected through energy prices, "
            "the import bill, inflation and the rupee."
        )

    elif any(
        x in text
        for x in [
            "federal reserve",
            "fed",
            "us interest rate",
            "treasury"
        ]
    ):

        india_impact = (
            "Changes in US monetary policy can influence "
            "foreign portfolio flows, the rupee, Indian "
            "bond yields and equity valuations."
        )

    else:

        india_impact = (
            "The indirect impact on India will depend "
            "on trade, capital flows, commodities and "
            "global investor sentiment."
        )


    # MARKET IMPACT

    if category in [
        "Markets",
        "Finance",
        "Economy"
    ]:

        market_impact = (
            "Potential market impact is likely to appear "
            "through equity prices, bond yields, currencies "
            "and investor sentiment."
        )

    elif category == "Commodities":

        market_impact = (
            "The strongest market effects are likely to "
            "appear in commodity-linked companies, "
            "inflation expectations and currencies."
        )

    elif category == "M&A":

        market_impact = (
            "The target company, acquirer and competing "
            "companies may react differently depending "
            "on the valuation and strategic rationale."
        )

    elif category == "Corporate":

        market_impact = (
            "The immediate effect is likely to be "
            "company or sector specific, depending "
            "on earnings, guidance and investor expectations."
        )

    else:

        market_impact = (
            "The market effect will depend on whether "
            "the development changes expectations about "
            "economic growth, corporate earnings or risk."
        )


    # WHAT TO WATCH

    watch_items = []

    if "inflation" in text:

        watch_items.append(
            "inflation data"
        )

    if any(
        x in text
        for x in [
            "interest rate",
            "rbi",
            "fed",
            "central bank"
        ]
    ):

        watch_items.append(
            "central bank policy"
        )

    if any(
        x in text
        for x in [
            "oil",
            "crude"
        ]
    ):

        watch_items.append(
            "crude oil prices"
        )

    if any(
        x in text
        for x in [
            "earnings",
            "profit",
            "revenue"
        ]
    ):

        watch_items.append(
            "company earnings and guidance"
        )

    if any(
        x in text
        for x in [
            "merger",
            "acquisition"
        ]
    ):

        watch_items.append(
            "regulatory approval and deal completion"
        )

    if not watch_items:

        watch_items = [
            "market reaction",
            "follow-up announcements",
            "economic and business data"
        ]

    what_to_watch = ", ".join(
        watch_items
    )

    return {

        "summary": summary,

        "why_it_matters":
            why_it_matters,

        "india_impact":
            india_impact,

        "market_impact":
            market_impact,

        "what_to_watch":
            what_to_watch

    }


def remove_duplicates(
    articles
):

    if len(articles) <= 1:

        return articles

    titles = [
        article["title"]
        for article in articles
    ]

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        matrix = vectorizer.fit_transform(
            titles
        )

        similarity = cosine_similarity(
            matrix
        )

    except Exception:

        return articles

    keep = []

    removed = set()

    for i in range(
        len(articles)
    ):

        if i in removed:
            continue

        keep.append(
            articles[i]
        )

        for j in range(
            i + 1,
            len(articles)
        ):

            if similarity[i][j] >= 0.75:

                removed.add(j)

    return keep


def collect_news():

    articles = []

    for source, feed_url in RSS_FEEDS.items():

        try:

            feed = feedparser.parse(
                feed_url
            )

            for entry in feed.entries:

                title = clean_text(
                    entry.get(
                        "title",
                        ""
                    )
                )

                description = clean_text(
                    entry.get(
                        "summary",
                        entry.get(
                            "description",
                            ""
                        )
                    )
                )

                url = entry.get(
                    "link",
                    ""
                )

                published = entry.get(
                    "published",
                    ""
                )

                if not title or not url:

                    continue

                category = classify_article(
                    title,
                    description
                )

                region = identify_region(
                    title,
                    description
                )

                importance = calculate_importance(
                    title,
                    description,
                    source
                )

                analysis = generate_analysis(
                    title,
                    description,
                    category,
                    region
                )

                article = {

                    "title": title,

                    "description":
                        description,

                    "source":
                        source,

                    "url":
                        url,

                    "published":
                        published,

                    "category":
                        category,

                    "importance":
                        importance,

                    "region":
                        region,

                    "summary":
                        analysis["summary"],

                    "why_it_matters":
                        analysis["why_it_matters"],

                    "india_impact":
                        analysis["india_impact"],

                    "market_impact":
                        analysis["market_impact"],

                    "what_to_watch":
                        analysis["what_to_watch"]

                }

                articles.append(
                    article
                )

        except Exception as e:

            print(
                f"{source}: {e}"
            )

    articles = remove_duplicates(
        articles
    )

    return articles