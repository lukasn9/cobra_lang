class Player(name, health becomes 100):
    own.name becomes name
    own.health becomes health
    own.inventory becomes []

    define take_damage(self, amount):
        self.health subtract amount
        output own.name + " takes " + str(amount) + " damage. Health is now " + str(own.health)
        if self.health is at most 0:
            output own.name + " has been defeated!"

    define add_item(self, item):
        own.inventory append item
        output own.name + " picked up " + item

    define show_status(self):
        output "Player: " + own.name + " | Health: " + str(own.health) + " | Inventory: " + str(own.inventory)