import streamlit as st
from Bank import Bank, SavingsAccount, CurrentAccount

banks = {
    "Bank of Python": Bank("Bank of Python"),
    "OOP National Bank": Bank("OOP National Bank")
}

if 'current_bank' not in st.session_state:
    st.session_state.current_bank = None

if 'logged_in_account' not in st.session_state:
    st.session_state.logged_in_account = None

st.title("🏦 ATM Machine Simulator (OOP in Python)")

bank_choice = st.selectbox("Select a Bank", list(banks.keys()))
st.session_state.current_bank = banks[bank_choice]

tabs = st.tabs(["Create Account", "Login", "ATM Operations"])

with tabs[0]:
    st.subheader("📝 Create New Account")
    acc_type = st.radio("Select Account Type", ["Savings", "Current"])
    acc_no = st.text_input("Account Number")
    holder_name = st.text_input("Account Holder Name")
    password = st.text_input("Set Account Password", type="password")

    if st.button("Create Account"):
        if acc_no.strip() == "" or holder_name.strip() == "" or password.strip() == "":
            st.warning("Please fill all fields.")
        else:
            created = st.session_state.current_bank.create_account(acc_type, acc_no, holder_name, password)
            if created:
                st.success(f"{acc_type} Account created successfully!")
            else:
                st.error("Account number already exists!")

with tabs[1]:
    st.subheader("🔐 Login to Your Account")
    login_acc_no = st.text_input("Enter your Account Number", key="login_acc")
    login_password = st.text_input("Enter Password", type="password", key="login_pass")

    if st.button("Login"):
        acc = st.session_state.current_bank.get_account(login_acc_no)
        if acc:
            if acc.verify_password(login_password):
                st.session_state.logged_in_account = acc
                st.success(f"Welcome {acc.holder_name}!")
            else:
                st.error("Incorrect password!")
        else:
            st.error("Account not found!")

with tabs[2]:
    st.subheader("💳 ATM Operations")
    acc = st.session_state.logged_in_account
    if acc:
        st.info(f"Logged in as: {acc.display_info()}")
        op = st.selectbox("Choose Operation", ["Check Balance", "Deposit", "Withdraw", "Apply Interest (Savings Only)"])
        if op == "Check Balance":
            st.success(f"Your balance is ₹{acc.get_balance():.2f}")
        elif op == "Deposit":
            amount = st.number_input("Enter amount to deposit", min_value=1)
            if st.button("Deposit"):
                acc.deposit(amount)
                st.session_state.current_bank.save_accounts()
                st.success(f"Deposited ₹{amount}. New balance: ₹{acc.get_balance():.2f}")
        elif op == "Withdraw":
            amount = st.number_input("Enter amount to withdraw", min_value=1)
            if st.button("Withdraw"):
                if acc.withdraw(amount):
                    st.session_state.current_bank.save_accounts()
                    st.success(f"Withdrew ₹{amount}. New balance: ₹{acc.get_balance():.2f}")
                else:
                    st.error("Insufficient balance or overdraft limit exceeded.")
        elif op == "Apply Interest (Savings Only)":
            if isinstance(acc, SavingsAccount):
                acc.apply_interest()
                st.session_state.current_bank.save_accounts()
                st.success(f"Interest applied. New balance: ₹{acc.get_balance():.2f}")
            else:
                st.warning("This feature is only for Savings Accounts.")
    else:
        st.warning("Please login first to access ATM features.")
