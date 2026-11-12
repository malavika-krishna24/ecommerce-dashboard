import streamlit as st
import pandas as pd
from pathlib import Path

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE = Path(__file__).resolve().parent
DATA = BASE / "reports" / "query_outputs"

# ==================================================
# CUSTOM CSS - TIMES NEW ROMAN
# ==================================================

st.markdown("""
<style>
/* Force readable dark text throughout */
.stApp,
.stApp p,
.stApp label,
.stApp span,
.stApp li,
.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="stMarkdownContainer"] {
    color: #243B53 !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] small {
    color: #243B53 !important;
}

/* Input labels and select controls */
.stSelectbox label,
.stMultiSelect label {
    color: #17324D !important;
}

/* Keep KPI text readable */
div[data-testid="stMetricLabel"] {
    color: #526579 !important;
}

div[data-testid="stMetricValue"] {
    color: #17324D !important;
}
/* Global font */
html, body, [class*="css"], [data-testid="stApp"] {
    font-family: "Times New Roman", Times, serif !important;
}

/* Main background */
.stApp {
    background-color: #f5f7fb;
}

/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* All headings */
h1 {
    font-family: "Times New Roman", serif !important;
    font-size: 34px !important;
    font-weight: 700 !important;
    color: #17324d !important;
}

h2 {
    font-family: "Times New Roman", serif !important;
    font-size: 25px !important;
    color: #17324d !important;
    font-weight: 700 !important;
}

h3 {
    font-family: "Times New Roman", serif !important;
    font-size: 20px !important;
    color: #24546a !important;
    font-weight: 600 !important;
}

/* Normal text */
p, label, li, span, div {
    font-family: "Times New Roman", Times, serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #eaf0f6;
    border-right: 1px solid #d6e0eb;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #17324d !important;
}

/* KPI cards */
div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #dce5ee;
    border-left: 5px solid #168b91;
    padding: 18px 18px 15px 18px;
    border-radius: 10px;
    box-shadow: 0 3px 10px rgba(20, 45, 70, 0.06);
}

div[data-testid="stMetricLabel"] {
    font-size: 15px !important;
    color: #526579 !important;
}

div[data-testid="stMetricValue"] {
    font-size: 25px !important;
    color: #17324d !important;
    font-weight: bold !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-family: "Times New Roman", serif !important;
    font-size: 17px !important;
    color: #34536b !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #087f83 !important;
    border-bottom-color: #087f83 !important;
}

/* Buttons */
.stButton button {
    background-color: #087f83;
    color: white;
    border-radius: 7px;
    border: none;
    font-family: "Times New Roman", serif;
}

/* Dividers */
hr {
    border-color: #d8e2ec;
}

/* Hide Streamlit branding and header */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {
    background-color: transparent;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():

    files = {
        "products": "06_top_products.csv",
        "states": "07_state_revenue.csv",
        "payments": "08_payment_distribution.csv",
        "aov": "09_average_order_value.csv",
        "monthly": "10_monthly_order_volume.csv",
        "reviews": "11_review_scores.csv",
        "delivery": "12_delivery_time.csv",
        "freight": "13_state_freight.csv",
        "sellers": "14_top_sellers.csv",
        "repeat": "15_repeat_customers.csv"
    }

    return {
        name: pd.read_csv(DATA / filename)
        for name, filename in files.items()
    }


try:
    data = load_data()
except Exception as e:
    st.error(f"Unable to load dashboard data: {e}")
    st.stop()


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.markdown("## Dashboard Controls")
st.sidebar.caption("Filter and explore the dataset")

all_states = sorted(
    data["states"]["c.customer_state"].dropna().unique()
)

selected_states = st.sidebar.multiselect(
    "Customer States",
    all_states,
    default=all_states
)

monthly = data["monthly"].copy()
monthly["order_month"] = pd.to_datetime(monthly["order_month"])

all_months = sorted(
    monthly["order_month"].dt.strftime("%Y-%m").unique()
)

selected_months = st.sidebar.multiselect(
    "Order Months",
    all_months,
    default=all_months
)

st.sidebar.divider()

if st.sidebar.button("Refresh Dashboard", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("### Data Information")
st.sidebar.write("**Dataset:** Olist Brazilian E-Commerce")
st.sidebar.write("**Processing:** Hadoop and HDFS")
st.sidebar.write("**Analytics:** Apache Hive")
st.sidebar.write("**Visualisation:** Python and Streamlit")

st.sidebar.divider()
st.sidebar.caption("M.Sc. Data Science | Big Data Analytics")


# ==================================================
# FILTER DATA
# ==================================================

state_data = data["states"][
    data["states"]["c.customer_state"].isin(selected_states)
].copy()

freight_data = data["freight"][
    data["freight"]["c.customer_state"].isin(selected_states)
].copy()

monthly_data = monthly[
    monthly["order_month"].dt.strftime("%Y-%m").isin(selected_months)
].copy()


# ==================================================
# DASHBOARD HEADER
# ==================================================

st.title("Brazilian E-Commerce Analytics")
st.caption(
    "Business Intelligence Dashboard | Sales, Customers, "
    "Payments and Logistics"
)

st.divider()


# ==================================================
# KPI CARDS
# ==================================================

st.subheader("Business Performance Overview")

total_revenue = state_data["revenue"].sum()
total_orders = state_data["total_orders"].sum()

aov = data["aov"]["average_order_value"].iloc[0]
delivery_days = data["delivery"]["average_delivery_days"].iloc[0]

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Delivered Product Revenue",
    f"R$ {total_revenue:,.2f}"
)

k2.metric(
    "Delivered Orders",
    f"{total_orders:,.0f}"
)

k3.metric(
    "Average Order Value",
    f"R$ {aov:,.2f}"
)

k4.metric(
    "Average Delivery Time",
    f"{delivery_days:.2f} days"
)

st.divider()


# ==================================================
# INTERACTIVE ANALYSIS TABS
# ==================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Sales Analysis",
    "Products & Sellers",
    "Payments",
    "Customer Experience",
    "Detailed Data"
])


# ==================================================
# TAB 1 - SALES ANALYSIS
# ==================================================

with tab1:

    st.subheader("Sales Performance")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Revenue by Customer State")

        if not state_data.empty:
            chart = state_data.sort_values(
                "revenue", ascending=False
            )

            st.bar_chart(
                chart,
                x="c.customer_state",
                y="revenue",
                height=350,
                x_label="Customer State",
                y_label="Revenue (BRL)"
            )
        else:
            st.info("Select at least one customer state.")

    with col2:
        st.markdown("### Monthly Order Volume")

        if not monthly_data.empty:
            st.line_chart(
                monthly_data.sort_values("order_month"),
                x="order_month",
                y="total_orders",
                height=350,
                x_label="Order Month",
                y_label="Number of Orders"
            )
        else:
            st.info("Select at least one month.")

    st.markdown("### State-wise Revenue Details")

    if not state_data.empty:
        st.dataframe(
            state_data.sort_values("revenue", ascending=False),
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# TAB 2 - PRODUCTS AND SELLERS
# ==================================================

with tab2:

    st.subheader("Product and Seller Performance")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Top 10 Products by Units Sold")

        products = data["products"].sort_values(
            "units_sold", ascending=True
        ).copy()

        products["Product ID"] = (
            products["oi.product_id"].str[:12]
        )

        st.bar_chart(
            products,
            x="Product ID",
            y="units_sold",
            height=380,
            x_label="Product ID",
            y_label="Units Sold"
        )

    with col2:
        st.markdown("### Top 10 Sellers by Revenue")

        sellers = data["sellers"].sort_values(
            "revenue", ascending=True
        ).copy()

        sellers["Seller ID"] = (
            sellers["s.seller_id"].str[:12]
        )

        st.bar_chart(
            sellers,
            x="Seller ID",
            y="revenue",
            height=380,
            x_label="Seller ID",
            y_label="Revenue (BRL)"
        )

    st.markdown("### Seller Performance Details")

    st.dataframe(
        data["sellers"].sort_values(
            "revenue", ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# TAB 3 - PAYMENT ANALYSIS
# ==================================================

with tab3:

    st.subheader("Payment Method Analysis")

    payment_data = data["payments"].copy()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Payment Records")

        st.bar_chart(
            payment_data,
            x="payment_type",
            y="payment_records",
            height=350,
            x_label="Payment Method",
            y_label="Payment Records"
        )

    with col2:
        st.markdown("### Payment Value")

        st.bar_chart(
            payment_data,
            x="payment_type",
            y="total_payment",
            height=350,
            x_label="Payment Method",
            y_label="Total Payment (BRL)"
        )

    st.dataframe(
        payment_data,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# TAB 4 - CUSTOMER EXPERIENCE
# ==================================================

with tab4:

    st.subheader("Customer and Logistics Analysis")

    col1, col2 = st.columns(2)

    review_data = data["reviews"].copy()
    review_data["Score"] = (
        review_data["r.review_score"].astype(str)
    )

    with col1:
        st.markdown("### Customer Review Scores")

        st.bar_chart(
            review_data,
            x="Score",
            y="total_reviews",
            height=350,
            x_label="Review Score",
            y_label="Number of Reviews"
        )

    with col2:
        st.markdown("### Average Freight by State")

        if not freight_data.empty:
            freight_chart = freight_data.sort_values(
                "average_item_freight",
                ascending=False
            )

            st.bar_chart(
                freight_chart,
                x="c.customer_state",
                y="average_item_freight",
                height=350,
                x_label="Customer State",
                y_label="Average Freight (BRL)"
            )
        else:
            st.info("Select at least one customer state.")

    total_reviews = review_data["total_reviews"].sum()

    positive_reviews = review_data[
        review_data["r.review_score"] >= 4
    ]["total_reviews"].sum()

    positive_percentage = (
        positive_reviews / total_reviews * 100
        if total_reviews else 0
    )

    st.metric(
        "Positive Review Share (Scores 4–5)",
        f"{positive_percentage:.2f}%"
    )


# ==================================================
# TAB 5 - DETAILED DATA
# ==================================================

with tab5:

    st.subheader("Explore Analytical Results")

    tables = {
        "Top Products": data["products"],
        "State Revenue": state_data,
        "Payment Analysis": data["payments"],
        "Monthly Orders": monthly_data,
        "Customer Reviews": data["reviews"],
        "Freight Analysis": freight_data,
        "Seller Performance": data["sellers"],
        "Repeat Customer Summary": data["repeat"]
    }

    selected_table = st.selectbox(
        "Choose an analytical result",
        list(tables.keys())
    )

    st.dataframe(
        tables[selected_table],
        use_container_width=True,
        hide_index=True
    )

    csv_data = tables[selected_table].to_csv(index=False)

    st.download_button(
        "Download Selected Data as CSV",
        data=csv_data,
        file_name=selected_table.lower().replace(" ", "_") + ".csv",
        mime="text/csv"
    )


# ==================================================
# BUSINESS INSIGHTS
# ==================================================

st.divider()

st.subheader("Key Business Insights")

if not state_data.empty:

    top_state = state_data.loc[
        state_data["revenue"].idxmax()
    ]

    st.info(
        f"Leading customer state: {top_state['c.customer_state']} "
        f"with delivered product revenue of "
        f"R$ {top_state['revenue']:,.2f}."
    )

if not data["payments"].empty:

    top_payment = data["payments"].loc[
        data["payments"]["payment_records"].idxmax()
    ]

    st.info(
        f"Most frequently used payment method: "
        f"{top_payment['payment_type']}."
    )

st.caption(
    "Revenue represents delivered product-item prices. "
    "Freight is analysed separately. "
    "Average order value is calculated from the Hive query output."
)

st.divider()

st.markdown(
    "<div style='text-align:center; color:#526579; "
    "font-family:Times New Roman; font-size:15px;'>"
    "Big Data Analytics | Hadoop | HDFS | Apache Hive | Python | Streamlit"
    "</div>",
    unsafe_allow_html=True
)

