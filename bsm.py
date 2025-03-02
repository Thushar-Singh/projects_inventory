import numpy as np
import scipy.stats as si
import matplotlib.pyplot as plt
import seaborn as sns

def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    Computes the Black-Scholes price for a European call or put option.
    
    Parameters:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to expiration (in years)
        r (float): Risk-free interest rate (as a decimal)
        sigma (float): Volatility of the underlying asset
        option_type (str): 'call' for Call option, 'put' for Put option
    
    Returns:
        float: Option price
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        option_price = S * si.norm.cdf(d1) - K * np.exp(-r * T) * si.norm.cdf(d2)
    else:
        option_price = K * np.exp(-r * T) * si.norm.cdf(-d2) - S * si.norm.cdf(-d1)
    
    return option_price

def plot_heatmap(T, r, sigma, option_type='call'):
    """Generates a heatmap showing option prices for different stock and strike price scenarios."""
    stock_prices = np.linspace(50, 200, 50)  # Stock price range
    strike_prices = np.linspace(50, 200, 50)  # Strike price range
    
    option_prices = np.zeros((len(stock_prices), len(strike_prices)))
    
    for i, S in enumerate(stock_prices):
        for j, K in enumerate(strike_prices):
            option_prices[i, j] = black_scholes(S, K, T, r, sigma, option_type)
    
    plt.figure(figsize=(10, 6))
    cmap = 'RdYlGn'  # Gradient colormap from red to yellow to green
    sns.heatmap(option_prices, xticklabels=np.round(strike_prices, 2), yticklabels=np.round(stock_prices, 2), cmap=cmap, annot=False)
    plt.xlabel('Strike Price')
    plt.ylabel('Stock Price')
    plt.title(f'Black-Scholes {option_type.capitalize()} Option Heatmap')
    plt.show()

# User input
S = float(input("Enter current stock price: "))
K = float(input("Enter strike price: "))
T = float(input("Enter time to expiration (in years): "))
r = float(input("Enter risk-free interest rate (as decimal): "))
sigma = float(input("Enter volatility (as decimal): "))
option_type = input("Enter option type (call/put): ").strip().lower()

# Compute option price
option_price = black_scholes(S, K, T, r, sigma, option_type)
print(f"{option_type.capitalize()} Option Price: {option_price:.2f}")

# Plot heatmap for visualization
plot_heatmap(T, r, sigma, option_type)
