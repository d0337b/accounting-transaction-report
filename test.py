import pandas as pd
import matplotlib.pyplot as plt

# 데이터 불러오기
def load_data():
    df = pd.read_csv("data/transactions.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month
    df["balance"] = df["debit"] - df["credit"]
    return df
df = load_data()

# 월별 debit 합계
monthly = df.groupby("month")["debit"].sum()

# 계정별 debit 합계
account = df.groupby("account")["debit"].sum().sort_values(ascending=False)

# 월별 x 계정별 debit 표
pivot = pd.pivot_table(
    df,
    index = "month",
    columns = "account",
    values = "debit",
    aggfunc = "sum"
)

# account별 debit Top 3자동화
month_input = int(input("몇 월을 보시겠습니까? : "))

def get_monthly_account(df, month):
    result = (
        df[df["month"] == month]
        .groupby("account")["debit"]
        .sum()
    )
    return result

monthly_account = get_monthly_account(df, month_input)

top3 = (monthly_account
            .sort_values(ascending=False)
            .head(3)
)

def plot_monthly_account(monthly_account, month):
    plt.figure(figsize=(8, 5))
    monthly_account.plot(kind="bar")
    plt.title(f"Month {month} Account Debit")
    plt.xlabel("Account")
    plt.ylabel("Debit")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"result/{month}_debit.png")
    plt.show()


# 출력
print("=== 월별 debit 합계 ===")
print(monthly)
print()

print("=== 계정별 debit 합계 ===")
print(account)
print()

print("=== 월별 x 계정별 debit 표 ===")
print(pivot)
print()

if len(monthly_account) == 0:
    print("데이터 없음")
else:
    # 출력
    print("===", month_input,"월 account별 TOP 3 ===")
    print(top3)

    #그래프
    plot_monthly_account(monthly_account, month_input)
