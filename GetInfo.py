# In this file we will read in the CSV input file and then generate the necessary data for the output file
# In order for to be parsed in the command line we need to import argparse
import argparse
import csv


# This function will be responsible for parsing command line args when running script
def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('-i', '--input', type=str, metavar="input.csv", required=True)
    parse.add_argument('-o', '--output', type=str, metavar='output.csv', required=True)
    return parse.parse_args()


# This next function will read in the csv file
def csv_reader(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip headers
        for row in reader:
            yield row


# The purpose for this function will be to keep track of the trade data. Such as the number of shares bought and sold
# As well as more stats we will need later on to fill in the CSV file.
# we will use a list to keep track of the data in each row
# we will have another list for the exchanges happening
# A dict will be most optimal when keeping track of the shares and exchanges
# And we will have another dict to track how much we spent and earned

def trade_data(row_data, exchanges_shares, exchanges, funds):
    more_data = [0] * 10
    symbol = row_data[1]
    type_trade = row_data[3]
    exchange = row_data[6]

    fill_size = int(row_data[4])
    fill_price = float(row_data[5])

    sign = 1 if type_trade == 'b' else -1
    buy_factor = int(sign > 0)
    sell_factor = int(sign < 0)

    # Updating symbol tracking
    if symbol not in exchanges_shares:
        exchanges_shares[symbol] = {'current_shares': 0, 'bought_shares': 0, 'sold_shares': 0}

    exchanges_shares[symbol]['current_shares'] += sign * fill_size
    exchanges_shares[symbol]['bought_shares'] += buy_factor * fill_size
    exchanges_shares[symbol]['sold_shares'] += sell_factor * fill_size

    # Updating exchange tracking separately
    if exchange not in exchanges:
        exchanges.append(exchange)

    funds['bought'] += buy_factor * fill_size * fill_price
    funds['sold'] += sell_factor * fill_size * fill_price

    # Prepare row data
    more_data[0] = exchanges_shares[symbol]['bought_shares']
    more_data[1] = exchanges_shares[symbol]['sold_shares']
    more_data[2] = exchanges_shares[symbol]['current_shares']
    more_data[3] = int(fill_size * fill_price)
    more_data[4] = sum(exchanges_shares[s]['bought_shares'] for s in exchanges_shares)
    more_data[5] = sum(exchanges_shares[s]['sold_shares'] for s in exchanges_shares)
    more_data[6] = sum(exchanges_shares[s]['bought_shares'] for s in exchanges_shares)
    more_data[7] = sum(exchanges_shares[s]['sold_shares'] for s in exchanges_shares)
    more_data[8] = funds['bought']
    more_data[9] = funds['sold']

    return more_data


# This next function will help process the data from the trade_data function in the CSV file
def process_data(file):
    exchanges_shares = {}
    exchanges = []
    funds = {'bought': 0.0, 'sold': 0.0}
    processed_rows = []

    for row in csv_reader(file):
        more_data = trade_data(row, exchanges_shares, exchanges, funds)
        processed_rows.append(row + more_data)

    return processed_rows


# Time to make our new CSV file with all the data
def write_file(input_file, output):
    headers = ['LocalTime', 'Symbol', 'EventType', 'Side', 'FillSize', 'FillPrice', 'Exchange',
               'SymbolBought', 'SymbolSold', 'SymbolPosition', 'SymbolNotional', 'TotalBought',
               'TotalSold', 'TotalBoughtNotional', 'TotalSoldNotional']

    processed_data = process_data(input_file)

    with open(output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(processed_data)


if __name__ == '__main__':
    args = parse_args()
    write_file(args.input, args.output)
