import ingredients


class Storage:
    storage = []

    def __init__(self, dough_stack_size=120, sauce_stack_size=80, topping1_stack_size=45, topping2_stack_size=45,
                 topping3_stack_size=45, topping4_stack_size=45):
        self.dough_stack_size = dough_stack_size
        self.sauce_stack_size = sauce_stack_size
        self.topping1_stack_size = topping1_stack_size
        self.topping2_stack_size = topping2_stack_size
        self.topping3_stack_size = topping3_stack_size
        self.topping4_stack_size = topping4_stack_size

        self.storage_capacity = self.dough_stack_size + self.sauce_stack_size + self.topping1_stack_size + \
                                self.topping2_stack_size + self.topping3_stack_size + self.topping4_stack_size

    def is_storage_full(self):
        """checks if storage is full or not"""
        number_of_available_ingredients = 0
        for _ in self.storage:
            number_of_available_ingredients += len(_)
        return True if number_of_available_ingredients == self.storage_capacity else False

    def available_ingredients_in_storge(self):
        """Returns the number of ingredients available in storage"""
        available_ingredients = {}
        for i in range(0, len(self.storage)):
            available_ingredients[ingredients.Ingredients().ingredients[i]] = len(self.storage[i])
        return available_ingredients

    def fill_storage(self):
        """Fills new storage"""
        ing = ingredients.Ingredients()
        self.storage.append(ing.new_ingredient_batch("Dough", self.dough_stack_size))
        self.storage.append(ing.new_ingredient_batch("sauce", self.sauce_stack_size))
        self.storage.append(ing.new_ingredient_batch("first topping", self.topping1_stack_size))
        self.storage.append(ing.new_ingredient_batch("second topping", self.topping2_stack_size))
        self.storage.append(ing.new_ingredient_batch("third topping", self.topping3_stack_size))
        self.storage.append(ing.new_ingredient_batch("forth topping", self.topping4_stack_size))

    def fill_partially_empty_storage(self):
        """Fills partially empty storage"""
        if self.is_storage_full():
            return "Ingredient storage is full. No more items can be added until some have been taken out."
        else:
            ing = ingredients.Ingredients()
            current_quantity = self.available_ingredients_in_storge()
            self.storage[0] += ing.new_ingredient_batch("dough", self.dough_stack_size - int(current_quantity['dough']))
            self.storage[1] += ing.new_ingredient_batch("sauce", self.sauce_stack_size - int(current_quantity['sauce']))
            self.storage[2] += ing.new_ingredient_batch("first topping",
                                                        self.topping1_stack_size - int(
                                                            current_quantity['first topping']))
            self.storage[3] += ing.new_ingredient_batch("second topping",
                                                        self.topping2_stack_size - int(
                                                            current_quantity['second topping']))
            self.storage[4] += ing.new_ingredient_batch("third topping",
                                                        self.topping3_stack_size - int(
                                                            current_quantity['third topping']))
            self.storage[5] += ing.new_ingredient_batch("forth topping",
                                                        self.topping4_stack_size - int(
                                                            current_quantity['forth topping']))

    def update_storage(self, dough_and_sauce, toppings):
        """Updates storage and returns ingredients used for pizza"""
        ingredients_required_for_pizza = []
        available_ingredients = self.available_ingredients_in_storge()
        for i in dough_and_sauce:
            available_ingredients[i] -= dough_and_sauce[i]
        for i in toppings:
            available_ingredients[i] -= 1
        for i in range(0, dough_and_sauce['dough']):
            ingredients_required_for_pizza.append(self.storage[0].pop(0))

        for i in range(0, dough_and_sauce['sauce']):
            ingredients_required_for_pizza.append(self.storage[1].pop(0))

        for i in range(0, len(toppings)):
            if toppings[i] == 'first topping':
                ingredients_required_for_pizza.append(self.storage[2].pop(0))

            elif toppings[i] == 'second topping':
                ingredients_required_for_pizza.append(self.storage[3].pop(0))

            elif toppings[i] == 'third topping':
                ingredients_required_for_pizza.append(self.storage[4].pop(0))

            elif toppings[i] == 'forth topping':
                ingredients_required_for_pizza.append(self.storage[5].pop(0))

        return ingredients_required_for_pizza
