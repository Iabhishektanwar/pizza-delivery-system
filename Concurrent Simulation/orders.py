import json
from operator import itemgetter
import csv


class Orders:

    def __init__(self):
        self.order = None
        self.header = ['Order ID', 'Time Accepted', 'Time Collected', 'Number of Small Pizzas',
                       'Number of Medium Pizzas', 'Number of Large Pizzas',
                       'IDs for each ingredient used for the order', 'Total Pizzas']

    @staticmethod
    def sort_orders(json_data):
        """Sorts all orders according to order id"""
        def get_orderid(order):
            return order.get('Order_ID')

        json_data.sort(key=get_orderid)
        return json_data

    def read_orders(self, file):
        """read json"""
        with open(file) as f:
            orders = json.load(f)
        self.sort_orders(orders)
        return orders

    @staticmethod
    def collection_queue(delivery_queue, processed_order):
        """Adds processed orders into delivery queue"""
        all_ingredients_used = []
        for i in processed_order[3]:
            all_ingredients_used += i
        ingredient_id_used_for_order = set(all_ingredients_used)
        order_json = {'Order ID': processed_order[0], 'Time Accepted': processed_order[1],
                      'Number of Small Pizzas': processed_order[2]['Small_Pizza'],
                      'Number of Medium Pizzas': processed_order[2]['Medium_Pizza'],
                      'Number of Large Pizzas': processed_order[2]['Large_Pizza'],
                      'IDs for each ingredient used for the order': ingredient_id_used_for_order,
                      'Total Pizzas': processed_order[2]['Small_Pizza'] + processed_order[2]['Medium_Pizza'] + \
                                      processed_order[2]['Large_Pizza']}

        delivery_queue.append(order_json)
        delivery_queue.sort(key=itemgetter('Total Pizzas'), reverse=True)

    def write_csv(self, order, time_of_collection):
        """Writes into CSV"""
        self.order = [order]
        self.order[0]['Time Collected'] = time_of_collection

        with open('processed_orders.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.header)
            writer.writerows(self.order)
        csvfile.close()

    def create_header_in_csv(self):
        """Creates header in new CSV file"""
        with open('processed_orders.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.header)
            writer.writeheader()
        csvfile.close()
