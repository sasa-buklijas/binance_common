from urllib.request import urlopen
import json


class BinanceExchangeInfo:
    
    def __init__(self):
        # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#exchange-information
        url = "https://data.binance.com/api/v3/exchangeInfo"
        response = urlopen(url)
        data_json = json.loads(response.read())
        #print(data_json)

        self._data_from = data_json['timezone']
        
        maybe_trading_assets = set()
        maybe_break_assets = set()

        trading_pairs = set()
        non_trading_pairs = set()
        len_trading_pairs = 0
        len_non_trading_pairs = 0
        len_pairs = 0
        for symbol in data_json['symbols']:
            len_pairs += 1
            #print(set(symbol['status']))
            
            match symbol['status']:
                case 'TRADING':
                    len_trading_pairs += 1
                    trading_pairs.add(symbol['symbol'])
                    maybe_trading_assets.add(symbol['baseAsset'])
                    maybe_trading_assets.add(symbol['quoteAsset'])
                case 'BREAK':
                    len_non_trading_pairs += 1
                    non_trading_pairs.add(symbol['symbol'])
                    maybe_break_assets.add(symbol['baseAsset'])
                    maybe_break_assets.add(symbol['quoteAsset'])

        assert len_pairs == len_trading_pairs+len_non_trading_pairs\
            ,'status other than TRADING or BREAK'
        self._len_trading_pairs = len_trading_pairs
        self._len_non_trading_pairs = len_non_trading_pairs
        self._len_pairs = len_pairs
        self._trading_pairs = trading_pairs
        self._non_trading_pairs = non_trading_pairs

        non_trading_assets = maybe_break_assets - maybe_trading_assets
        len_non_trading_assets = len(non_trading_assets)
        trading_assets = maybe_trading_assets - non_trading_assets
        len_trading_assets = len(trading_assets)
        len_assets = len(maybe_trading_assets.union(maybe_break_assets))
        assert len_non_trading_assets + len_trading_assets == len_assets\
            ,'Number of trading and non_trading assets wrong'
        self._trading_assets = trading_assets
        self._non_trading_assets = non_trading_assets
        self._len_assets = len_assets
        self._len_non_trading_assets = len_non_trading_assets
        self._len_trading_assets = len_trading_assets


def main():
    pass

if __name__ == "__main__":
    main()
