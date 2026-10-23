import yfinance as yf


class Portfolio:
    def __init__(self, initial_capital):
        self.capital = initial_capital
        self.stocks = {}

    def get_add_stock(self, symbol):
        if symbol not in self.stocks:
            print(f"Adding {symbol} to portfolio.")
            self.stocks[symbol] = Stock(symbol)
        return self.stocks[symbol]

    def buy(self, symbol):
        try:
            stock = self.get_add_stock(symbol)
            stock_price = stock.get_price()

            # Calculate risk and amount
            risk_per_share = 0.05 * stock_price
            capital_risked = 0.01 * self.capital
            stock_amount = int(capital_risked / risk_per_share)

            if stock_amount < 0:
                print(f"Suggested to buy 0 stocks of {symbol}")
                return

            cost = stock_amount * stock_price

            if cost > self.capital:
                print(f"Not enough money to buy {symbol}")
                return

            # Execute trades
            self.capital -= cost
            stock.add_positions(stock_amount,stock_price)
            print(f"Bought {stock_amount} shares of {symbol} at ${stock_price:.2f}")
            print(f"Used ${cost:.2f} | Remaining Capital: ${self.capital:.2f}")
            print("-----------------------------------------------------")


        except Exception as e:
            print(f"Failed to buy {symbol}: {e}")

    def sell(self, symbol):

        if symbol not in self.stocks:
            print(f"You don't own any shares of  {symbol}")
            return

        try:
            stock = self.stocks[symbol]
            shares_to_sell = stock.active_positions
            stock_price = stock.get_price()

            revenue = shares_to_sell * stock_price
            profit = revenue - (shares_to_sell * stock.average_price)

            self.capital += revenue
            stock.active_positions = 0
            stock.average_price = 0.0   #Reset Average Price

            print(f"Successfully sold {shares_to_sell} shares of {symbol} at ${stock_price:.2f}")
            print(f"Revenue gained: {revenue:.2f}  | Capital: {self.capital:.2f}")
            print(f"Realized P/L: ${profit}")


        except Exception as e:
            print(f"Failed to buy {symbol}: {e}")

    def check_price(self, symbol):
        try:
            stock_price = yf.Ticker(symbol).fast_info['lastPrice']
            print(f"{symbol}: ${stock_price:.2f}")


        except Exception as e:
            print(f"Failed to get stock price for {symbol}")

    def print_portfolio_summary(self):
        print(f"\n--- Portfolio Summary ---")
        print(f"Available Capital: ${self.capital:.2f}")

        has_positions = False

        for symbol, stock in self.stocks.items():
            if stock.active_positions > 0:
                print(f"{stock.name} ({symbol}): {stock.active_positions} shares")
                has_positions = True

        if not has_positions:
            print("No stocks owned yet")
            print("------------------------------")


class Stock:
    def __init__(self, symbol):
        self.symbol = symbol.upper()
        self.ticker = yf.Ticker(self.symbol)
        self.average_price = 0

        self.name = self.ticker.info.get("longName", self.symbol)
        self.active_positions = 0

    def add_positions(self, amount,price):
        if(self.active_positions == 0):
            self.average_price = price
        else:
            total_cost = (self.average_price * self.active_positions) + (price * amount)
            self.average_price = total_cost / (self.active_positions + amount)

        self.active_positions += amount


    def get_price(self):
        return self.ticker.fast_info['lastPrice']


if __name__ == "__main__":
    my_portfolio = Portfolio(10000)
    print(f"Starting Capital: {my_portfolio.capital:.2f}")

    while True:
        user_input = input("Enter a command: ")

        if user_input.lower() == "exit":
            print(f"Exiting. Final Capital: ${my_portfolio.capital:.2f}")
            break

        parts = user_input.split()

        if not parts:
            continue

        command = parts[0].lower()

        if command == "buy" and len(parts) >= 2:
            for ticker_str in parts[1:]:
                my_portfolio.buy(ticker_str.upper())


        elif command == "sell" and len(parts) >= 2:
            for ticker_str in parts[1:]:
                my_portfolio.sell(ticker_str.upper())


        elif command == "summary":
            my_portfolio.print_portfolio_summary()


        else:
            for ticker_str in parts:
                my_portfolio.check_price(ticker_str.upper())
