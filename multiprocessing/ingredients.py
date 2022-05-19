from functions import *
from storage import *
import multiprocessing


class Ingredients:
    def __init__(self):
        self.ingredients = ['dough', 'sauce', 'first topping', 'second topping', 'third topping', 'forth topping']
        self.pizza_size = ['Large_Pizza', 'Medium_Pizza', 'Small_Pizza']

    def new_ingredient_batch(self, ingredient, size):
        """creates a new batch of ingredients"""
        ingredient = ingredient.lower()
        if ingredient not in self.ingredients:
            return "Incorrect Ingredient"
        else:
            ingredient_id = create_ingredient_id(ingredient)
            ingredient_container = [ingredient_id] * size
            return ingredient_container

    def get_required_ingredients(self, storage, pizza, toppings):
        """Return ingredient list for pizzas from storage"""
        ingredients_required = {}
        if pizza not in self.pizza_size:
            return False
        else:
            if pizza == self.pizza_size[0]:
                ingredients_required = {'dough': 3, 'sauce': 2}
            elif pizza == self.pizza_size[1]:
                ingredients_required = {'dough': 2, 'sauce': 1}
            elif pizza == self.pizza_size[2]:
                ingredients_required = {'dough': 1, 'sauce': 1}

            ingredient_list = Storage().update_storage(storage, ingredients_required, toppings)
            return ingredient_list

    def ingredients_available(self, storage, pizza):
        """checks if ingredients are available for pizza"""
        if pizza not in self.pizza_size:
            return None
        else:
            available_ingredients = Storage().available_ingredients_in_storge(storage)

            if pizza == self.pizza_size[0]:
                toppings = ['first topping', 'second topping', 'third topping', 'forth topping']
                if available_ingredients['dough'] >= 3 and available_ingredients['sauce'] >= 2 and \
                        available_ingredients['first topping'] >= 1 and available_ingredients['second topping'] >= 1 \
                        and available_ingredients['third topping'] >= 1 and available_ingredients['forth topping'] >= 1:

                    ingredients_required_for_pizza = self.get_required_ingredients(storage, pizza, toppings)
                    return ingredients_required_for_pizza
                else:
                    return None
            elif pizza == self.pizza_size[1]:
                toppings = random_toppings(pizza)
                if available_ingredients['dough'] >= 2 and available_ingredients['sauce'] >= 1 and \
                        available_ingredients[toppings[0]] >= 1 and available_ingredients[toppings[1]] >= 1 and \
                        available_ingredients[toppings[2]] >= 1:

                    ingredients_required_for_pizza = self.get_required_ingredients(storage, pizza, toppings)
                    return ingredients_required_for_pizza
                else:
                    return None
            elif pizza == self.pizza_size[2]:
                toppings = random_toppings(pizza)
                if available_ingredients['dough'] >= 1 and available_ingredients['sauce'] >= 1 and \
                        available_ingredients[toppings[0]] >= 1 and available_ingredients[toppings[1]] >= 1:

                    ingredients_required_for_pizza = self.get_required_ingredients(storage, pizza, toppings)
                    return ingredients_required_for_pizza
                else:
                    return None
