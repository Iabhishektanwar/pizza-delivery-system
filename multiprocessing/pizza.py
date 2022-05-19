from time import sleep
from ingredients import *
from orders import *


class Pizzas:
    def __init__(self):
        self.pizza = ['Large_Pizza', 'Medium_Pizza', 'Small_Pizza']

    @staticmethod
    def get_total_pizza(order):
        """Returns total number of pizzas in an order"""
        total_pizza = order['Small_Pizza'] + order['Medium_Pizza'] + order['Large_Pizza']
        return total_pizza

    def create_pizza(self, storage, pizza):
        """create a pizza and returns all ingredients if available on this basis of pizza size"""
        if pizza not in self.pizza:
            return None
        else:
            ingredients_for_pizza = Ingredients().ingredients_available(storage, pizza)
            if ingredients_for_pizza is not None:
                sleep(0.02)
                return ingredients_for_pizza
            return None

    def cook_pizza(self, storage, order, time_of_order, delivery_queue):
        """selects a single pizza from order dictionary and starts cooking"""
        ingredients_used_for_order = []
        order_id = order['Order_ID']
        order.pop('Order_ID')
        for pizza in order:
            for i in range(0, order[pizza]):
                ingredients_required_for_pizza_making = self.create_pizza(storage, pizza)
                if ingredients_required_for_pizza_making is None:
                    return False
                else:
                    ingredients_used_for_order.append(ingredients_required_for_pizza_making)

        time_to_cook = 0.01 * self.get_total_pizza(order)
        sleep(time_to_cook)

        processed_order = [order_id, time_of_order, order, ingredients_used_for_order]
        Orders().collection_queue(delivery_queue, processed_order)
        return True
