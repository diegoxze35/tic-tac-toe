from datetime import date

if __name__ == '__main__':

    date_1 = date(day=12, month=9, year=2002)
    date_2 = date(day=29, month=8, year=2004)
    march_10_2025 = date(day=10, month=3, year=2025)
    lived_days_1 = (march_10_2025 - date_1).days
    lived_days_2 = (march_10_2025 - date_2).days
    print(lived_days_1 % 3, lived_days_2 % 3)

    print('Welcome to Tic Tac Toe!')