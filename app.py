import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="MoneyMentor Pro",
    page_icon="💰",
    layout="wide"
)
st.set_page_config(
    page_title="MoneyMentor Pro",
    page_icon="💰",
    layout="wide"
)

# Login System
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 MoneyMentor Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Credentials")

    st.stop()

# Main App
st.title("💰 MoneyMentor Pro")
st.subheader("Smart Expense and Savings Tracker")

# Transactions
if "transactions" not in st.session_state:
    st.session_state.transactions = []

st.header("➕ Add Transaction")

trans_type = st.selectbox(
    "Type",
    ["Income", "Expense"]
)

description = st.text_input("Description")

amount = st.number_input(
    "Amount (₹)",
    min_value=0.0
)

if st.button("Add Transaction"):
    st.session_state.transactions.append(
        {
            "Type": trans_type,
            "Description": description,
            "Amount": amount
        }
    )

    st.success("Transaction Added!")

st.header("📋 Transaction History")
if st.session_state.transactions:

    df = pd.DataFrame(st.session_state.transactions)

    st.dataframe(df)

    # Delete Transaction
    st.subheader("🗑️ Delete Transaction")

    delete_index = st.number_input(
        "Transaction Number",
        min_value=1,
        max_value=len(df),
        step=1
    )

    if st.button("Delete Transaction"):
        st.session_state.transactions.pop(delete_index - 1)
        st.success("Deleted Successfully!")
        st.rerun()

    # Dashboard
    total_income = df[df["Type"] == "Income"]["Amount"].sum()
    total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
    balance = total_income - total_expense

    st.header("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("💵 Income", f"₹{total_income:.2f}")
    col2.metric("💸 Expense", f"₹{total_expense:.2f}")
    col3.metric("💰 Balance", f"₹{balance:.2f}")

    # Savings Goal
    st.header("🎯 Savings Goal")

    goal = st.number_input(
        "Enter Savings Goal",
        min_value=0.0
    )

    if goal > 0:
        progress = min(balance / goal, 1.0)
        st.progress(progress)

    # Budget Planner
    st.header("💵 Monthly Budget Planner")

    food_budget = st.number_input(
        "Food Budget",
        min_value=0.0
    )

    travel_budget = st.number_input(
        "Travel Budget",
        min_value=0.0
    )

    shopping_budget = st.number_input(
        "Shopping Budget",
        min_value=0.0
    )

    # Budget Alerts
    food_spent = df[df["Description"] == "Food"]["Amount"].sum()

    if food_budget > 0 and food_spent > food_budget:
        st.warning(
            f"⚠️ Food budget exceeded by ₹{food_spent-food_budget:.2f}"
        )

    # Smart Financial Tips
    st.header("🤖 Smart Financial Tips")

    if total_income > 0:

        savings_rate = balance / total_income

        if savings_rate > 0.2:
            st.success(
                "Excellent! You are saving more than 20%."
            )
        elif savings_rate > 0.1:
            st.info(
                "Good savings habit. Try to increase it."
            )
        else:
            st.error(
                "Your expenses are too high."
            )
                # Achievement Badges
    st.header("🏆 Achievement Badges")

    if balance > 10000:
        st.success("🥉 Beginner Saver")

    if balance > 50000:
        st.success("🥈 Smart Saver")

    if balance > 100000:
        st.success("🥇 Financial Master")

    # CSV Export
    st.header("📥 Export Transactions")

    csv = df.to_csv(index=False)

    st.download_button(
        "Download CSV",
        csv,
        "moneymentor_transactions.csv",
        "text/csv"
    )

    # Expense Pie Chart
    expense_df = df[df["Type"] == "Expense"]

    if not expense_df.empty:

        st.header("📈 Expense Analysis")

        category_expenses = expense_df.groupby(
            "Description"
        )["Amount"].sum()

        fig, ax = plt.subplots()

        ax.pie(
            category_expenses,
            labels=category_expenses.index,
            autopct="%1.1f%%"
        )

        ax.axis("equal")

        st.pyplot(fig)

else:
    st.info("No transactions added yet.")