from pykrx import stock
from datetime import datetime, timedelta
import pandas as pd


def get_price_info(tickers, begin, end, kind):
	data = list()
	for id, t in enumerate(tickers):
		if id % 10 == 0:
			print(id)
		df = stock.get_market_ohlcv_by_date(begin, end, t, 'm')
		# print(df.head())
		# print(df.index.to_list())
		# print(df['종가'].to_list())
		data.append({k.strftime('%Y%m%d'):v for k, v in zip(df.index.to_list(), df['종가'].to_list())})
		data[-1]['티커'] = t
		data[-1]['종목명'] = stock.get_market_ticker_name(t)
		data[-1]['시장'] = kind
		data[-1]['고가일'] = df['종가'].idxmax()
		data[-1]['고가'] = df['종가'].max()
	df = pd.DataFrame(data)
	df = df.set_index('티커')
	return df

def make_base_table(begin, end, output_path):

	kospi_tickers = stock.get_market_ticker_list(now, 'KOSPI')
	kosdaq_tickers = stock.get_market_ticker_list(now, 'KOSDAQ')

	print('kospi:', len(kospi_tickers), 'kosdaq:', len(kosdaq_tickers))
	print('begin', three_years_ago, 'end', now)

	kospi_df = get_price_info(kospi_tickers, begin, end, 'KOSPI')
	kosdaq_df = get_price_info(kosdaq_tickers, begin, end, 'KOSDAQ')
	df = pd.concat([kospi_df, kosdaq_df])


	cap_df = stock.get_market_cap_by_ticker(end)
	df = pd.merge(df, cap_df, how='left', on='티커')
	df['편차'] = round((df['종가'] / df['고가']-1) * 100, 2)

	fundamental_df = stock.get_market_fundamental_by_ticker(end, 'ALL')
	fundamental_df['ROE'] = fundamental_df['PBR'] / fundamental_df['PER'] * 100
	df = pd.merge(df, fundamental_df, how='left', on='티커')

	moving_columns = ['종목명', '시장', '고가일', '고가',  '편차'] + cap_df.columns.to_list() + fundamental_df.columns.to_list()
	columns = df.columns.to_list()[-len(moving_columns):] + df.columns.to_list()[:-len(moving_columns)]
	df = df[columns]

	df.to_csv(output_path, encoding='utf-8')

if __name__ == '__main__':
	now = datetime.today().strftime('%Y%m%d')
	three_years_ago = (datetime.now() - timedelta(days=3 * 365)).strftime('%Y%m%d')
	make_base_table(three_years_ago, now, 'stock_info.csv')




