import streamlit as st

# Alphabetically sorted currencies
currencies = sorted(["USD", "CAD", "GBP", "EUR", "CHF", "NOK", "SEK", "JPY", "AUD", "NZD"])

# Updated Economic Indicators and Weights (Total: 100%)
indicators = {
    "Interest Rate Decisions": 30,
    "Consumer Price Index (CPI)": 25,
    "Unemployment Rate": 15,
    "GDP Growth": 10,
    "Producer Price Index (PPI)": 7,
    "Services PMI": 7,
    "Manufacturing PMI": 6,
}

# Streamlit UI
st.title("📊 Currency Strength Tracker")
st.write("Enter weighted scores for each currency and compare their strength.")

# Dictionary to store currency scores
currency_scores = {currency: 0 for currency in currencies}

# Data Input Section
st.subheader("🔢 Enter Weighted Scores")

for currency in currencies:
    st.write(f"### {currency}")
    total_score = 0

    cols = st.columns(len(indicators))  # Creates a column for each indicator

    for i, (indicator, weight) in enumerate(indicators.items()):
        with cols[i]:
            score = st.number_input(
                f"{indicator}",
                value=0.0,  # Default value
                step=0.1,  # Allows decimals
                key=f"{currency}_{indicator}"
            )
            weighted_score = (score * weight) / 100
            total_score += weighted_score

    currency_scores[currency] = total_score

# Sort currencies by strength (highest score first)
sorted_currencies = sorted(currency_scores.items(), key=lambda x: x[1], reverse=True)

# Display Ranked Results
st.subheader("🏆 Currency Strength Rankings")

st.write("### **Ranked from Strongest (1st) to Weakest (10th):**")
for rank, (currency, score) in enumerate(sorted_currencies, start=1):
    st.write(f"**{rank}. {currency}** - {score:.2f}")

# Show full table
st.subheader("📊 Full Currency Strength Table")
st.write("### **Weighted Scores for Each Currency:**")
st.table({currency: [f"{score:.2f}"] for currency, score in sorted_currencies})


# Predicted Trend Table Based on Specific Pairs
st.subheader("📈 Predicted Trend Table (Based on Currency Strength)")

# Define the specific currency pairs
selected_pairs = [
    "AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD", "AUDUSD", 
    "CADCHF", "CADJPY", "CHFJPY", "EURAUD", "EURCAD", 
    "EURCHF", "EURGBP", "EURJPY", "EURNZD", "EURNOK", 
    "EURSEK", "EURUSD", "GBPAUD", "GBPCAD", "GBPCHF", 
    "GBPJPY", "GBPNZD", "GBPNOK", "GBPSEK", "GBPUSD", 
    "NZDCAD", "NZDCHF", "NZDJPY", "NZDUSD", "NOKJPY", 
    "NOKSEK", "SEKJPY", "USDCAD", "USDCHF", "USDJPY", 
    "USDNOK", "USDSEK"
]

# Threshold for Neutral trend (score difference)
neutral_threshold = 0.3

# Build trend prediction table manually for the selected pairs
trend_rows = []
for pair in selected_pairs:
    base, quote = pair[:3], pair[3:]
    base_score = currency_scores[base]
    quote_score = currency_scores[quote]
    diff = base_score - quote_score

    if abs(diff) <= neutral_threshold:
        trend = "🟠 Neutral"
    elif diff > 0:
        trend = "🟢 Bullish"
    else:
        trend = "🔴 Bearish"

    trend_rows.append((pair, trend))

# Display the trend table
st.write("### **Currency Pair Trend Predictions**")
st.markdown("Each pair shows trend for the **base currency vs. quote currency**.")

# Display in a formatted table using Markdown
table_md = "| Pair | Trend |\n|------|--------|\n"
for pair, trend in trend_rows:
    table_md += f"| {pair} | {trend} |\n"

st.markdown(table_md)
