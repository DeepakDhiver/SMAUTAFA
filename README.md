# Stock Market Prediction Using Technical and Sentiment Analysis
## Description

This project provides insights into the stock market by utilizing deep learning combined with technical and sentiment analysis. Key features include:

- **News Sentiment Analysis**: Input a company name to receive its sentiment score.
- **Dashboard for Stock Recommendations**: Select a stock and time interval from a list, and receive recommendations based on 12 technical indicators, informing whether to buy or not in that particular time frame.
- **Stock Charts Display**: A dedicated page showcasing stock charts.
- **Stock Fundamentals**: View fundamental details for stocks.

Built using Django, the project integrates with `yfinance` for stock data fetching and incorporates Trading View scripts for certain fundamental stock data.

## Features

1. **News Sentiment Analysis**: Understand the sentiment of news articles related to a given company.
2. **Stock Recommendation Dashboard**: Gain insights based on 12 technical indicators.
3. **Visual Stock Charts**: Analyze stock performance over time.
4. **Stock Fundamentals**: Deep dive into the fundamental aspects of stocks.

## Prerequisites

- Python 3.x
- Django (latest version)
- yfinance library
- [Trading View scripts](LINK_TO_TRADEVIEW_SCRIPTS_IF_AVAILABLE)

## Installation & Setup

1. Clone the repository:
2. Navigate to the project directory:
3. Install the required Python packages:
4. Run the Django server:

This should start the server, and the application should be accessible at `http://127.0.0.1:8000/`.

## Usage

1. **News Sentiment Analysis**: Navigate to the 'News Sentiment' page, input the company name and fetch its sentiment score.
2. **Dashboard**: Select your desired stock and time interval. The dashboard will provide insights based on 12 technical indicators.
3. **Stock Charts**: Accessible via the 'Stock Charts' page.
4. **Stock Fundamentals**: Retrieve fundamental details for any stock via the dedicated page.

## License

[MIT License](LICENSE)

## Acknowledgments

- Special thanks to the `yfinance` library for enabling stock data fetching.
- Gratitude to Trading View for providing scripts that facilitated fundamental stock data fetching.

## Contact & Support

For any issues, questions, or feedback, please contact [deepakdhiver28@gmail.com].
