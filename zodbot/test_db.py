import unittest
from .db import Database

class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.db.create_table()

    def tearDown(self):
        self.db.drop_table()

    def test_check_if_db_exists(self):
        self.assertTrue(self.db.check_if_db_exists())

    def test_add_transaction(self):
        self.db.add_transaction("user1", "AAPL", "BUY", 10, 150.0)
        self.db.add_transaction("user1", "AAPL", "SELL", 5, 160.0)
        self.db.add_transaction("user2", "GOOG", "BUY", 8, 1200.0)
        self.assertEqual(len(self.db.get_user_transactions("user1")), 2)
        self.assertEqual(len(self.db.get_user_transactions("user2")), 1)

    def test_get_all_portfolio(self):
        self.db.add_transaction("user1", "AAPL", "BUY", 10, 150.0)
        self.db.add_transaction("user1", "AAPL", "SELL", 5, 160.0)
        self.db.add_transaction("user2", "GOOG", "BUY", 8, 1200.0)
        portfolio = self.db.get_all_portfolio()
        self.assertEqual(len(portfolio), 2)
        self.assertEqual(portfolio[0].symbol, "AAPL")
        self.assertEqual(portfolio[0].shares, 5)
        self.assertEqual(portfolio[0].value, 700.0)
        self.assertEqual(portfolio[0].weighted_average, 140.0)
        self.assertEqual(portfolio[1].symbol, "GOOG")
        self.assertEqual(portfolio[1].shares, 8)
        self.assertEqual(portfolio[1].value, 9600.0)
        self.assertEqual(portfolio[1].weighted_average, 1200.0)

    def test_get_user_transactions(self):
        self.db.add_transaction("user1", "AAPL", "BUY", 10, 150.0)
        self.db.add_transaction("user1", "AAPL", "SELL", 5, 160.0)
        self.db.add_transaction("user2", "GOOG", "BUY", 8, 1200.0)
        transactions_user1 = self.db.get_user_transactions("user1")
        transactions_user2 = self.db.get_user_transactions("user2")
        self.assertEqual(len(transactions_user1), 2)
        self.assertEqual(len(transactions_user2), 1)
        self.assertEqual(transactions_user1[0].uid, "user1")
        self.assertEqual(transactions_user1[0].symbol, "AAPL")
        self.assertEqual(transactions_user1[0].action, "BUY")
        self.assertEqual(transactions_user1[0].shares, 10)
        self.assertEqual(transactions_user1[0].price, 150.0)
        self.assertEqual(transactions_user1[1].uid, "user1")
        self.assertEqual(transactions_user1[1].symbol, "AAPL")
        self.assertEqual(transactions_user1[1].action, "SELL")
        self.assertEqual(transactions_user1[1].shares, 5)
        self.assertEqual(transactions_user1[1].price, 160.0)
        self.assertEqual(transactions_user2[0].uid, "user2")
        self.assertEqual(transactions_user2[0].symbol, "GOOG")
        self.assertEqual(transactions_user2[0].action, "BUY")
        self.assertEqual(transactions_user2[0].shares, 8)
        self.assertEqual(transactions_user2[0].price, 1200.0)

    def test_get_user_portfolio(self):
        self.db.add_transaction("user1", "AAPL", "BUY", 10, 150.0)
        self.db.add_transaction("user1", "AAPL", "SELL", 5, 160.0)
        self.db.add_transaction("user2", "GOOG", "BUY", 8, 1200.0)
        portfolio_user1 = self.db.get_user_portfolio("user1")
        portfolio_user2 = self.db.get_user_portfolio("user2")
        self.assertEqual(len(portfolio_user1), 1)
        self.assertEqual(len(portfolio_user2), 1)
        self.assertEqual(portfolio_user1[0].symbol, "AAPL")
        self.assertEqual(portfolio_user1[0].shares, 5)
        self.assertEqual(portfolio_user1[0].value, 700.0)
        self.assertEqual(portfolio_user1[0].weighted_average, 140.0)
        self.assertEqual(portfolio_user2[0].symbol, "GOOG")
        self.assertEqual(portfolio_user2[0].shares, 8)
        self.assertEqual(portfolio_user2[0].value, 9600.0)
        self.assertEqual(portfolio_user2[0].weighted_average, 1200.0)


    def test_get_user_stock(self):
        self.db.add_transaction("user1", "AAPL", "BUY", 10, 150.0)
        self.db.add_transaction("user1", "AAPL", "SELL", 5, 160.0)
        self.db.add_transaction("user2", "GOOG", "BUY", 8, 1200.0)
        stock_user1 = self.db.get_user_stock("user1", "AAPL")
        stock_user2 = self.db.get_user_stock("user2", "GOOG")
        self.assertIsNotNone(stock_user1)
        self.assertIsNotNone(stock_user2)
        if stock_user1 is None or stock_user2 is None:
            return
        self.assertEqual(stock_user1.symbol, "AAPL")
        self.assertEqual(stock_user1.shares, 5)
        self.assertEqual(stock_user1.value, 700.0)
        self.assertEqual(stock_user1.weighted_average, 140.0)
        self.assertEqual(stock_user2.symbol, "GOOG")
        self.assertEqual(stock_user2.shares, 8)
        self.assertEqual(stock_user2.value, 9600.0)
        self.assertEqual(stock_user2.weighted_average, 1200.0)

if __name__ == '__main__':
    unittest.main()