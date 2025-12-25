import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# -----------------------------
# App Title
# -----------------------------
st.title("🛒 Market Basket Analyzer (Mini Project)")

# -----------------------------
# Session State Initialization
# -----------------------------
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# -----------------------------
# Helper: Input Validation
# -----------------------------
def is_invalid_item(item):
    if item.isdigit():              # numbers not allowed
        return True
    if len(item) == 1 and item.isalpha():  # single alphabet not allowed
        return True
    return False

# -----------------------------
# Add Transaction (FORM)
# -----------------------------
st.subheader("Enter Transaction Items")

with st.form("transaction_form", clear_on_submit=True):
    items_input = st.text_input("Enter items (comma separated):")
    add_clicked = st.form_submit_button("➕ Add Transaction")

    if add_clicked:
        if not items_input.strip():
            st.error("Please enter items.")
        else:
            raw_items = [
                i.strip().lower()
                for i in items_input.split(",")
                if i.strip()
            ]

            for item in raw_items:
                if is_invalid_item(item):
                    st.error("Numbers or single-letter items are not allowed.")
                    break
            else:
                transaction = list(set(raw_items))
                st.session_state.transactions.append(transaction)
                st.success("Transaction added successfully.")

# -----------------------------
# Action Buttons
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➖ Remove Last Transaction"):
        if st.session_state.transactions:
            st.session_state.transactions.pop()
            st.success("Last transaction removed.")
        else:
            st.warning("No transactions to remove.")

with col2:
    analyze_clicked = st.button("📊 Analyze Transactions")

with col3:
    if st.button("🔄 Restart"):
        st.session_state.transactions.clear()
        st.success("All transactions cleared.")

# -----------------------------
# Display Transactions
# -----------------------------
st.subheader("📋 Transactions")

if st.session_state.transactions:
    for idx, t in enumerate(st.session_state.transactions, start=1):
        st.write(f"{idx}. {', '.join(t)}")
else:
    st.info("No transactions added yet.")

# -----------------------------
# Analysis Section
# -----------------------------
if analyze_clicked:

    if len(st.session_state.transactions) < 2:
        st.error("Add at least two transactions for analysis.")
    else:
        # One-hot encoding
        items = sorted({item for t in st.session_state.transactions for item in t})
        encoded_data = []

        for t in st.session_state.transactions:
            encoded_data.append({item: item in t for item in items})

        df = pd.DataFrame(encoded_data)

        # Apriori
        frequent_itemsets = apriori(df, min_support=0.3, use_colnames=True)

        if frequent_itemsets.empty:
            st.warning("No frequent itemsets found. All items are unique.")
        else:
            rules = association_rules(
                frequent_itemsets,
                metric="lift",
                min_threshold=0.8
            )

            # Remove rules that occur only once
            rules = rules[rules["support"] > (1 / len(st.session_state.transactions))]

            if rules.empty:
                st.warning("No strong association rules found.")
            else:
                st.subheader("🧠 Shopping Pattern Insights")

                for _, rule in rules.iterrows():
                    lhs = ", ".join(rule["antecedents"])
                    rhs = ", ".join(rule["consequents"])
                    confidence = round(rule["confidence"] * 100, 2)
                    st.write(
        f"• Customers who buy **{lhs}** "
        f"are likely to also buy **{rhs}** "
        f"with **{confidence}% probability**."
    )