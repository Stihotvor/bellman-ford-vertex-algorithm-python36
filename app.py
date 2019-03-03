from math import log
from typing import Tuple, List
import logging

logs = logging.getLogger('Logger')
logs.setLevel(logging.DEBUG)

rates = (
    # PLN, EUR, USD, RUB
    (1, 0.23, 0.26, 17.41),  # PLN
    (4.31, 1, 1.14, 75.01),  # EUR
    (3.79, 0.88, 1, 65.93),  # USD
    (0.057, 0.013, 0.015, 1),  # RUB
)

currencies = ('PLN', 'EUR', 'USD', 'RUB')


def negate_logarithm_converter(graph: Tuple[Tuple[float]]) -> List[List[float]]:
    """
    Takes logarithm of each item in graph and negate it
    :param graph: Tuple of tuples of currency rates. Each rate is the float
    :return:
    """
    logs.info('Converting with logarithms and negating')
    result = [[-log(edge) for edge in row] for row in graph]
    logs.debug(f'New graph: {result}')
    return result


def arbitrage(currency_tuple: tuple, rates_matrix: Tuple[Tuple[float, ...]]):
    """
    Calculates arbitrage situations and prints out the details of this calculations
    :param currency_tuple: Tuple of currencies, used in source matrix with the appropriate order
    :param rates_matrix: Tuple of tuples of currency rates. Each rate is the float
    :return:
    """
    logs.info('Starting arbitrage calculator')
    logs.debug('Setup source currency to the first one')
    source = 0

    logs.debug('Converting the graph to the appropriate one')
    trans_graph = negate_logarithm_converter(rates_matrix)

    logs.debug('Calculating length of the graph')
    n = len(trans_graph)
    logs.debug(f'The lenght is {n}')

    logs.debug('Set the minimum distance to infinity for all the currencies')
    min_dist = [float('inf')] * n

    logs.debug('Set the price/rate source currency for each destination currency')
    min_dist_cur = [[]] * n

    logs.debug('Minimum distance for the source currency set to 0')
    min_dist[source] = 0

    logs.info('Setup complete. Starting calculations.')
    logs.debug('Relax edges |V - 1| times')
    for loop in range(n - 1):
        logs.debug(f'Loop no.{loop}')
        for source_currency in range(n):
            logs.debug(f'Loop for source currency {currency_tuple[source_currency]}')

            for dest_currency in range(n):
                logs.debug(f'Loop for pair {currency_tuple[source_currency]} -> {currency_tuple[dest_currency]}')

                if min_dist[dest_currency] > min_dist[source_currency] + trans_graph[source_currency][dest_currency]:
                    logs.info("Cheaper route found")
                    min_dist[dest_currency] = min_dist[source_currency] + trans_graph[source_currency][dest_currency]

                    # TODO Figure out how to register correct chains
                    min_dist_cur[dest_currency] = currency_tuple[source_currency]

    print(min_dist_cur)


    # If we can still relax edges, then we have a negative cycle
    for source_currency in range(n):
        for dest_currency in range(n):
            if min_dist[dest_currency] > min_dist[source_currency] + trans_graph[source_currency][dest_currency]:
                print(f'Found arbitrage: {currency_tuple[source_currency]} -> {currency_tuple[dest_currency]}')


if __name__ == "__main__":
    arbitrage(currencies, rates)
