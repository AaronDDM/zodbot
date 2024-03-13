import sqlite3
from typing import Optional
from zodbot.config import config

class Transaction:
    def __init__(self, uid:str, symbol:str, action: str, shares: int, price: float):
        self.uid = uid
        self.symbol = symbol
        self.action = action
        self.shares = shares
        self.price = price
        self.added_on = None

class Portfolio:
    def __init__(self, uid:str, symbol:str, last_transaction_date: int, shares=0, value=0.0, weighted_average=0.0):
        self.uid = uid
        self.symbol = symbol
        self.shares = shares
        self.value = value
        self.last_transaction_date = last_transaction_date
        self.weighted_average = weighted_average

class Database:
    TABLES_NAMES = {
        "TRANSACTIONS": "transactions"
    }

    def __init__(self, db_name):
        self.con = sqlite3.connect(db_name)

    def check_if_db_exists(self):
        with self.con:
            cur = self.con.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.TABLES_NAMES['TRANSACTIONS']}'")
            return cur.fetchone() is not None

    def create_table(self):
        with self.con:
            self.con.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.TABLES_NAMES['TRANSACTIONS']} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uid TEXT,
                    symbol TEXT,
                    action TEXT CHECK(action IN ('BUY', 'SELL')),
                    shares INTEGER,
                    price REAL
                    added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

    def drop_table(self):
        with self.con:
            self.con.execute(f"DROP TABLE IF EXISTS {self.TABLES_NAMES['TRANSACTIONS']}")

    def add_transaction(self, uid, symbol, action, shares, price):
        with self.con:
            self.con.execute(f"INSERT INTO {self.TABLES_NAMES['TRANSACTIONS']} (uid, symbol, action, shares, price) VALUES (?, ?, ?, ?, ?)", (uid, symbol, action, shares, price))

    def get_all_portfolio(self) -> list[Portfolio]:
        with self.con:
            cur = self.con.execute(f"""
            SELECT 
                uid,
                symbol, 
                SUM(CASE WHEN action = 'BUY' THEN shares ELSE -shares END) AS shares, 
                SUM(CASE WHEN action = 'BUY' THEN shares * price ELSE -shares * price END) AS value,
                SUM(CASE WHEN action = 'BUY' THEN shares * price ELSE -shares * price END) / SUM(CASE WHEN action = 'BUY' THEN shares ELSE -shares END) AS weighted_average,
                MAX(added_on) AS last_transaction_date
            FROM 
                {self.TABLES_NAMES['TRANSACTIONS']} 
            GROUP BY 
                uid, symbol
            """)
            
            results = cur.fetchall()

            portfolios = []
            for result in results:
                portfolio = Portfolio(result[0], result[1], result[2], result[3], result[4])
                portfolios.append(portfolio)
            
            return portfolios

    def get_user_transactions(self, uid) -> list[Transaction]:
        with self.con:
            cur = self.con.execute(f"""
                SELECT 
                    uid, 
                    symbol, 
                    action, 
                    shares, 
                    price 
                FROM 
                    {self.TABLES_NAMES['TRANSACTIONS']}  
                WHERE 
                    uid = ?
            """, (uid,))
            
            results = cur.fetchall()

            transactions = []
            for result in results:
                transaction = Transaction(result[0], result[1], result[2], result[3], result[4])
                transactions.append(transaction)

            return transactions
        
    def get_user_stock(self, uid, symbol) -> Optional[Portfolio]:
        with self.con:
            cur = self.con.execute(f"""
                SELECT 
                    uid, 
                    symbol, 
                    SUM(CASE WHEN action = 'BUY' THEN shares ELSE -shares END) AS shares, 
                    SUM(CASE WHEN action = 'BUY' THEN shares * price ELSE -shares * price END) AS value,
                    SUM(CASE WHEN action = 'BUY' THEN shares * price ELSE -shares * price END) / SUM(CASE WHEN action = 'BUY' THEN shares ELSE -shares END) AS weighted_average,
                    MAX(added_on) AS last_transaction_date
                FROM 
                    {self.TABLES_NAMES['TRANSACTIONS']}  
                WHERE 
                    uid = ? AND symbol = ?
                GROUP BY 
                    symbol
            """, (uid, symbol))
            result = cur.fetchone()
            if result is None:
                return None
            return Portfolio(result[0], result[1], result[2], result[3], result[4])

    # User's portfolio is the sum of all the transactions
    # where the action is "BUY" minus the sum of all the
    # transactions where the action is "SELL" with a final
    def get_user_portfolio(self, uid) -> list[Portfolio]:
        with self.con:
            cur = self.con.execute(f"""
                SELECT 
                    symbol, 
                    SUM(CASE WHEN action = 'BUY' THEN shares ELSE -shares END) AS shares, 
                    SUM(CASE WHEN action = 'BUY' THEN shares * price ELSE -shares * price END) AS value,
                    SUM(CASE WHEN action = 'BUY' THEN shares * price ELSE -shares * price END) / SUM(CASE WHEN action = 'BUY' THEN shares ELSE -shares END) AS weighted_average,
                    MAX(added_on) AS last_transaction_date
                FROM 
                    {self.TABLES_NAMES['TRANSACTIONS']}  
                WHERE 
                    uid = ?
                GROUP 
                    BY symbol
            """, (uid,))
            result = cur.fetchall()

            portfolios = []
            for res in result:
                portfolio = Portfolio(uid, res[0], res[1], res[2], res[3])
                portfolios.append(portfolio)
            
            return portfolios

db = Database(config.db_file)