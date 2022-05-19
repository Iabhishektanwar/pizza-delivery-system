from pizza import *
from datetime import datetime
from threading import Thread


def start_processing_orders(all_orders):
    while len(all_orders) != 0:
        order = all_orders[0]
        order_accepted_time = datetime.now().strftime("%H:%M:%S")
        cook_pizza = Pizzas().cook_pizza(order, order_accepted_time)
        if cook_pizza:
            all_orders.pop(0)
        else:
            print("All ingredients for next order are not available.")
            break


def start_delivering_orders():
    delivery_queue = Orders.delivery_queue
    total_orders = len(orders)
    while total_orders != 0:
        if len(delivery_queue) > 0:
            processed_order = delivery_queue[0]
            order_collected_time = datetime.now().strftime("%H:%M:%S")
            Orders().write_csv(processed_order, order_collected_time)
            delivery_queue.pop(0)
            total_orders -= 1
            sleep(0.05)
        if len(orders) > 0 and not threads[0].is_alive():
            break


def periodic_refill_storage():
    """ Refills storage if storage is not full"""
    if threads[0].is_alive() and threads[1].is_alive():
        sleep(2)
        if not storage.Storage().is_storage_full():
            storage.Storage().fill_partially_empty_storage()
        else:
            pass


if __name__ == "__main__":
    # fills storage for the first time
    storage.Storage().fill_storage()

    # read orders from the JSON file
    orders = Orders().read_orders('orders.json')

    # Three threads are formed, one for processing, one for processing orders, one for delivering orders, and one for
    # occasionally filling storage.
    threads = [Thread(target=start_processing_orders, args=(orders,)), Thread(target=start_delivering_orders),
               Thread(target=periodic_refill_storage)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
