
import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# --------------------------------------------------
# APP CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Market Basket Analyzer",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Market Basket Analyzer")
st.write(
    "Discover shopping patterns using the Apriori algorithm "
    "and association rule mining."
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "transactions" not in st.session_state:
    st.session_state.transactions = []

# --------------------------------------------------
# INPUT VALIDATION
# --------------------------------------------------

def is_invalid_item(item):
    """Reject numeric-only items and single-letter items."""
    item = item.strip()

    if not item:
        return True

    if item.isdigit():
        return True

    if len(item) == 1 and item.isalpha():
        return True

    return False


# --------------------------------------------------
# TRANSACTION INPUT
# --------------------------------------------------

st.subheader("➕ Add a Transaction")

with st.form("transaction_form", clear_on_submit=True):
    items_input = st.text_input(
        "Enter items separated by commas",
        placeholder="Example: bread, milk, butter"
    )

    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        if not items_input.strip():
            st.warning("Please enter at least one item.")

        else:
            raw_items = [
                item.strip().lower()
                for item in items_input.split(",")
                if item.strip()
            ]

            invalid_items = [
                item for item in raw_items
                if is_invalid_item(item)
            ]

            if invalid_items:
                st.error(
                    "Invalid item(s): "
                    + ", ".join(invalid_items)
                    + ". Use meaningful product names."
                )

            elif not raw_items:
                st.warning("Please enter valid product names.")

            else:
                # Remove duplicates while preserving input order.
                transaction = list(dict.fromkeys(raw_items))

                st.session_state.transactions.append(transaction)
                st.success("Transaction added successfully!")

# --------------------------------------------------
# TRANSACTION CONTROLS
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    if st.button(
        "↩️ Remove Last Transaction",
        use_container_width=True
    ):
        if st.session_state.transactions:
            st.session_state.transactions.pop()
            st.rerun()
        else:
            st.info("There are no transactions to remove.")

with col2:
    if st.button(
        "🔄 Restart / Clear All",
        use_container_width=True
    ):
        st.session_state.transactions = []
        st.rerun()

# --------------------------------------------------
# DISPLAY TRANSACTIONS
# --------------------------------------------------

st.divider()
st.subheader("📋 Current Transactions")

if st.session_state.transactions:
    for index, transaction in enumerate(
        st.session_state.transactions, start=1
    ):
        st.write(
            f"**Transaction {index}:** "
            + ", ".join(transaction)
        )
else:
    st.info("Add some transactions to begin the analysis.")

# --------------------------------------------------
# ANALYSIS SETTINGS
# --------------------------------------------------

st.divider()
st.subheader("⚙️ Analysis Settings")

col1, col2 = st.columns(2)

with col1:
    min_support = st.slider(
        "Minimum Support",
        min_value=0.10,
        max_value=1.00,
        value=0.40,
        step=0.05,
        format="%.2f"
    )

    st.caption(
        f"Current Minimum Support: {min_support * 100:.0f}%"
    )

with col2:
    min_confidence = st.slider(
        "Minimum Confidence",
        min_value=0.10,
        max_value=1.00,
        value=0.60,
        step=0.05,
        format="%.2f"
    )

    st.caption(
        f"Current Minimum Confidence: "
        f"{min_confidence * 100:.0f}%"
    )

analyze = st.button(
    "📊 Generate Association Rules",
    use_container_width=True,
    type="primary"
)

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

if analyze:

    if len(st.session_state.transactions) < 2:
        st.warning(
            "Please add at least two transactions before analysis."
        )

    else:
        # Convert transactions into a one-hot encoded DataFrame.
        all_items = sorted({
            item
            for transaction in st.session_state.transactions
            for item in transaction
        })

        encoded_data = []

        for transaction in st.session_state.transactions:
            encoded_data.append({
                item: item in transaction
                for item in all_items
            })

        df = pd.DataFrame(encoded_data, columns=all_items)
        df = df.astype(bool)

        # --------------------------------------------------
        # APRIORI: FREQUENT ITEMSETS
        # --------------------------------------------------

        frequent_itemsets = apriori(
            df,
            min_support=min_support,
            use_colnames=True
        )

        st.divider()

        if frequent_itemsets.empty:
            st.warning(
                "No frequent itemsets found for the selected "
                "minimum support. Try lowering the support value."
            )

        else:
            # --------------------------------------------------
            # FREQUENT ITEMSETS TABLE
            # --------------------------------------------------

            itemset_display = frequent_itemsets.copy()

            itemset_display["Items"] = (
                itemset_display["itemsets"].apply(
                    lambda items: ", ".join(sorted(items))
                )
            )

            itemset_display["Support (%)"] = (
                itemset_display["support"] * 100
            ).round(2)

            itemset_display = itemset_display[
                ["Items", "Support (%)"]
            ]

            st.subheader("📦 Frequent Itemsets")

            st.dataframe(
                itemset_display,
                use_container_width=True,
                hide_index=True
            )

            # --------------------------------------------------
            # ASSOCIATION RULES
            # --------------------------------------------------

            st.subheader("🔗 Association Rules")

            if len(frequent_itemsets) < 2:
                rules = pd.DataFrame()

            else:
                # Tiny tolerance for floating-point precision.
                rules = association_rules(
                    frequent_itemsets,
                    metric="confidence",
                    min_threshold=max(
                        0,
                        min_confidence - 1e-9
                    )
                )

                # Keep rules meeting the selected threshold.
                if not rules.empty:
                    rules = rules[
                        rules["confidence"]
                        >= min_confidence - 1e-9
                    ].copy()

            if rules.empty:
                st.warning(
                    "No association rules found for the selected "
                    "support and confidence values."
                )

                st.info(
                    "Try lowering the Minimum Support or "
                    "Minimum Confidence."
                )

            else:
                rules["From"] = rules["antecedents"].apply(
                    lambda items: ", ".join(sorted(items))
                )

                rules["To"] = rules["consequents"].apply(
                    lambda items: ", ".join(sorted(items))
                )

                rules["Support (%)"] = (
                    rules["support"] * 100
                ).round(2)

                rules["Confidence (%)"] = (
                    rules["confidence"] * 100
                ).round(2)

                rules = rules.sort_values(
                    by=["confidence", "support"],
                    ascending=[False, False]
                ).reset_index(drop=True)

                # Lift has been removed from the display.
                rule_display = rules[
                    [
                        "From",
                        "To",
                        "Support (%)",
                        "Confidence (%)"
                    ]
                ].copy()

                rule_display.rename(
                    columns={
                        "From": "If Customer Buys",
                        "To": "Then Customer May Buy"
                    },
                    inplace=True
                )

                st.dataframe(
                    rule_display,
                    use_container_width=True,
                    hide_index=True
                )

                # --------------------------------------------------
                # SHOPPING PATTERN INSIGHTS
                # --------------------------------------------------

                st.subheader("🧠 Shopping Pattern Insights")

                for _, rule in rules.head(5).iterrows():
                    lhs = ", ".join(
                        sorted(rule["antecedents"])
                    )

                    rhs = ", ".join(
                        sorted(rule["consequents"])
                    )

                    confidence = round(
                        rule["confidence"] * 100, 2
                    )

                    st.write(
                        f"Customers who buy **{lhs}** "
                        f"are likely to also buy **{rhs}**, "
                        f"with **{confidence}% confidence**."
                    )

                # --------------------------------------------------
                # BUSINESS RECOMMENDATION
                # --------------------------------------------------

                st.subheader("💡 Business Recommendation")

                best_rule = rules.iloc[0]

                best_from = ", ".join(
                    sorted(best_rule["antecedents"])
                )

                best_to = ", ".join(
                    sorted(best_rule["consequents"])
                )

                best_confidence = round(
                    best_rule["confidence"] * 100, 2
                )

                st.success(
                    f"Customers who purchase **{best_from}** "
                    f"are associated with **{best_to}**. "
                    f"The confidence is **{best_confidence}%**. "
                    "Consider placing these products together "
                    "or offering them as a combo."
                )

st.divider()

st.caption(
    "Market Basket Analyzer | Data Science Mini-Project | "
    "Powered by Apriori and Association Rule Mining"
)
