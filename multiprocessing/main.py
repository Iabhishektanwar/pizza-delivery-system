from datetime import datetime
from pizza import *
from functions import *
from storage import *

"""
Ingredient storage is a shared resource that is created using the multiprocessing manager function and is a 
ListProxy object. This object contains six additional ListProxy objects, each of which has all of the ingredients 
needed to make a pizza. I have considered four different sorts of toppings in my implementation.
 
To manage the mutually exclusive access and race condition locks have been implemented on the shared storage to avoid 
deadlocks.Ingredient store, Pizza oven, and Collection queue are all shared resources which are modified as pizzas are 
being processed. To avoid the possibility of data corruption, the critical region has been locked. 
 
A lock has been implemented inside the try catch block to ensure that no deadlock or livelock occurs. A try block is 
used to acquire lock before critical section, and a finally block is used to release it once the critical section code 
has been successfully executed.

start_processing_orders is a cyclic process which will process all the orders until orders queue is empty. If the queue
is empty this cyclic process will terminate. Likewise start_delivering_orders is also a cyclic process which will 
deliver all processed orders until delivery queue is empty. By limiting the number of iteration in this process 
starvation is handled.
 
"""


def start_processing_orders(storage, all_orders, lock, delivery_queue):
    while True:
        if len(all_orders) > 0:
            try:
                lock.acquire()
                order = all_orders[0]
                order_accepted_time = datetime.now().strftime("%H:%M:%S")
                cook_pizza = Pizzas().cook_pizza(storage, order, order_accepted_time, delivery_queue)
                if cook_pizza:
                    all_orders.pop(0)
                else:
                    print("All ingredients for next order are not available.")
                    break
            except IndexError:
                pass
            finally:
                lock.release()
        else:
            break


def start_delivering_orders(orders_json, delivery_queue, lock):
    total_orders = len(orders_json)
    count = 0
    while total_orders != 0:
        try:
            lock.acquire()
            if total_orders > 0 and len(delivery_queue) > 0:
                processed_order = delivery_queue[0]
                order_collected_time = datetime.now().strftime("%H:%M:%S")
                Orders().write_csv(processed_order, order_collected_time)
                delivery_queue.pop(0)
                total_orders -= 1
                sleep(0.05)
            if True:
                if count == 100:
                    break
                else:
                    count += 1
        finally:
            lock.release()


if __name__ == "__main__":

    pool = multiprocessing.Pool()
    manager = multiprocessing.Manager()
    multiprocessing_lock = manager.Lock()

    ingredient_storage = manager.list()

    # Fill Ingredient storage for the first time (The storage is a shared resource)
    for i in range(len(ingredients.Ingredients().ingredients)):
        container = [create_ingredient_id(ingredients.Ingredients().ingredients[i])] * Storage().container_size[i]
        ingredient_container = manager.list(container)
        ingredient_storage.append(ingredient_container)

    orders_from_json = Orders().read_orders('orders.json')

    # Order Queue (The order queue is a shared resource)
    orders = manager.list(orders_from_json)

    # Storage queue (The storage queue is a shared resource)
    delivery = manager.list()

    # Takes input from user
    number_of_chef = int(input("Number of Chefs: "))
    number_of_drivers = int(input("Number of Drivers: "))

    cooking_processes = []
    delivery_processes = []

    for i in range(number_of_chef):
        process = multiprocessing.Process(target=start_processing_orders,
                                          args=(ingredient_storage, orders, multiprocessing_lock, delivery,))
        cooking_processes.append(process)

    for i in range(number_of_drivers):
        process = multiprocessing.Process(target=start_delivering_orders, args=(orders_from_json, delivery,
                                                                                multiprocessing_lock,))
        delivery_processes.append(process)

    processes = cooking_processes + delivery_processes

    for process in processes:
        process.start()

    for process in processes:
        process.join()
