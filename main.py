import yfinance as yf

def get_ticker(stock_name):
    print(f"Getting Data for {stock_name}")
    stock_data = yf.download (stock_name, period="6mo", interval = "1d", auto_adjust=True);
    print (stock_data.tail(5))
    ticker = yf.Ticker(stock_name)
    return ticker


def risk_management(capital, stock_price,stop_loss):

    risk = 0.01 * capital
    stock_amount = stock_price / risk

    risk_stop_loss = abs(stock_amount - stop_loss)
    stock_amount_2 = stock_amount / risk_stop_loss

    print(stock_amount)
    print(stock_amount_2)
    return min(stock_amount, stock_amount_2)


def calc_stop_loss(stock_price):
    ##insert algorithm
    stop_loss_factor = 0.05;
    stop_loss_factor = 0.95
    stop_loss_price = stock_price * (1.00 - stop_loss_factor)
    print("Stop loss price: ", stop_loss_price)
    return stop_loss_price;


if __name__ == "__main__":
   #user_input = input("Enter a stock ticker to analyze: ")
   user_input = "AAPL"
   ticker = get_ticker(user_input)
   live_price = ticker
   print(live_price)    
   stop_loss_price = calc_stop_loss(live_price)
   stock_amount = risk_management(10000, live_price, stop_loss_price)
   print(stock_amount)

