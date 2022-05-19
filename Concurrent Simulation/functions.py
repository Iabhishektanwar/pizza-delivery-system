import random


def random_number(length):
    """create a random number which is assigned to ingredient"""
    range_start = 10 ** (length - 1)
    range_end = (10 ** length) - 1
    return random.randint(range_start, range_end)


def create_ingredient_id(ingredient):
    """concatenate random number with ingredient code"""
    ingredient_id = ""
    ing_id = str(random_number(11))

    if ingredient == "dough":
        ingredient_id = "DOU-" + ing_id
    elif ingredient == "sauce":
        ingredient_id = "SAU-" + ing_id
    elif ingredient == "first topping":
        ingredient_id = "TOP1-" + ing_id
    elif ingredient == "second topping":
        ingredient_id = "TOP2-" + ing_id
    elif ingredient == "third topping":
        ingredient_id = "TOP3-" + ing_id
    elif ingredient == "forth topping":
        ingredient_id = "TOP4-" + ing_id
    return ingredient_id


def random_toppings(pizza):
    """selects random toppings for small and medium pizza"""
    toppings = ['first topping', 'second topping', 'third topping', 'forth topping']
    if pizza == "Medium_Pizza":
        return random.sample(toppings, 3)
    elif pizza == "Small_Pizza":
        return random.sample(toppings, 2)
