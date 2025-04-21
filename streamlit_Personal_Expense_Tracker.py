import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title("Personal Expense Tracker")
st.write("Track your expenses, visualize spending habits, and achieve your savings goals!")


if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])


with st.form("expense_form"):
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Transport", "Bills", "Entertainment", "Other"])
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    description = st.text_input("Description")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_expense = pd.DataFrame([[date, category, amount, description]], 
                                   columns=['Date', 'Category', 'Amount', 'Description'])
        st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
        st.success("Expense added successfully!")


st.subheader("Expense History")
st.dataframe(st.session_state.expenses)


st.subheader("Spending by Category")
if not st.session_state.expenses.empty:
    category_sum = st.session_state.expenses.groupby('Category')['Amount'].sum()
    plt.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%')
    st.pyplot(plt)


st.subheader("Savings Goal Tracker")
goal = st.number_input("Set Monthly Savings Goal:", min_value=0.0, step=100.0)
if goal > 0:
    total_spent = st.session_state.expenses['Amount'].sum()
    remaining = max(0, goal - total_spent)
    st.write(f"Goal: ₹{goal:.2f}, Spent: ₹{total_spent:.2f}, Remaining: ₹{remaining:.2f}")
    st.progress(total_spent / goal if goal else 0)
