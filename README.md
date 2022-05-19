#Pizza delivery system

Ingredient storage is a shared resource that is created using the multiprocessing manager function and is a ListProxy object. This object contains six additional ListProxy objects, each of which has all of the ingredients needed to make a pizza. I have considered four different sorts of toppings in my implementation.

To manage the mutually exclusive access and race condition locks have been implemented on the shared storage to avoid deadlocks.Ingredient store, Pizza oven, and Collection queue are all shared resources which are modified as pizzas are being processed. To avoid the possibility of data corruption, the critical region has been locked.

A lock has been implemented inside the try catch block to ensure that no deadlock or livelock occurs. A try block is used to acquire lock before critical section, and a finally block is used to release it once the critical section code has been successfully executed.

start_processing_orders is a cyclic process which will process all the orders until orders queue is empty. If the queue is empty this cyclic process will terminate. Likewise start_delivering_orders is also a cyclic process which will deliver all processed orders until delivery queue is empty. By limiting the number of iteration in this process starvation is handled.
