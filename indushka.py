from tradingview_ta import TA_Handler
from tabulate import tabulate

assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'DOGEUSDT', 'PEPEUSDT']
timeframes = ['1h', '4h', '1d']

def get_recs():
    recommendations = {'1h': [], '4h': [], '1d': []}

    for timeframe in timeframes:
        for symbol in assets:
            result = TA_Handler(symbol=symbol,
                                screener='Crypto',
                                exchange='mexc',
                                interval=timeframe).get_analysis().summary['RECOMMENDATION']

            recommendations[timeframe].append(result)

    return recommendations


def get_TA(asset, tf='1h', exchange='mexc'):
    recommendation = TA_Handler(symbol=asset + 'usdt',
                                screener='Crypto',
                                exchange=exchange,
                                interval=tf  # Interval.INTERVAL_15_MINUTES
                                )
    try:
        recommendation = recommendation.get_analysis().summary
    except:
        return None

    recommendation = [[key, value] for key, value in recommendation.items()]
    return tabulate(recommendation, tablefmt="github")


def make_table(data):
    return tabulate(
        data,
        headers='keys',
        showindex=assets,
        tablefmt="github")
