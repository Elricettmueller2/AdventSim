import pygame
import random
from enum import Enum

# Define some constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)


# Message Log Box Constants
MESSAGE_LOG_WIDTH = 400
MESSAGE_LOG_HEIGHT = 150
MESSAGE_LOG_X = SCREEN_WIDTH - MESSAGE_LOG_WIDTH - 10  # 10 pixels from the right edge
MESSAGE_LOG_Y = SCREEN_HEIGHT - MESSAGE_LOG_HEIGHT - 10  # 10 pixels from the bottom edge
MESSAGE_LOG_BACKGROUND_COLOR = (50, 50, 50)
MESSAGE_LOG_TEXT_COLOR = WHITE
MESSAGE_LOG_LINE_HEIGHT = 20  # Line height for messages



# Player class definition initiate player and give stats 
class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack = 10
        self.defense = 1
        self.gold = 0
        self.level = 0

    def level_up(self):
                self.level += 1
                self.health += 20
                self.attack += 5
                self.defense += 2
                # Any other stat increases and logic for leveling up

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0: 
            self.health = 0
            self.dead = True  # You could add this flag)
                

            # You could also handle the player's death here

class Ally:
    def __init__(self, name, health, attack, special_abilities):
        self.name = name
        self.health = health
        self.attack = attack
        self.special_abilities = special_abilities

    def perform_ability(self, ability_name):
        # Perform the special ability (details depend on your game's mechanics)
        pass

# Enemy class definition would go here
class Enemy:
    def __init__(self, name, health, attack, defense, special_abilities, loot):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.special_abilities = special_abilities
        self.loot = loot


    def take_damage(self, damage):
        # Subtract damage from health, considering defense
        self.health -= damage / self.defense

    def is_defeated(self):
        return self.health <= 0

goblin = Enemy("Goblin", 50, 5, 2, ["Bash"], {"Gold": 5})
dragon = Enemy("Dragon", 300, 20, 10, ["Fire Breath", "Swipe"], {"Gold": 200, "Dragon Scale": 1})


class States(Enum):
    EXPLORATION = 1
    COMBAT = 2
    INVENTORY = 3
    MENU = 4
    TRAVEL = 5


# MessageLog class definition would go here
class MessageLog:
    def __init__(self):
        self.messages = []
        self.max_messages = 5  # Number of messages to display

    def add_message(self, new_message):
        """Adds a new message to the log."""
        self.messages.append(new_message)
        # Make sure we do not exceed the maximum number of messages
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
    
    def render_messages(self, screen, font, x, y, line_height):
        # Draw the message log background box
        pygame.draw.rect(
            screen,
            MESSAGE_LOG_BACKGROUND_COLOR,
            (MESSAGE_LOG_X, MESSAGE_LOG_Y, MESSAGE_LOG_WIDTH, MESSAGE_LOG_HEIGHT)
        )

        # Initialize the starting y-coordinate for the bottom of the message log
        current_y = MESSAGE_LOG_Y + MESSAGE_LOG_HEIGHT - line_height
        
        # We reverse the messages list so the newer messages are rendered last and at the bottom
        for message in reversed(self.messages):
            message_str = str(message)   # Convert to string
            words = message_str.split(' ')
            lines = []
            current_line = ""
            
            for word in words:
                # Check if this word would exceed the width of the log box
                if font.size(current_line + word)[0] > MESSAGE_LOG_WIDTH:
                    lines.append(current_line)  # Finish the current line before the word is added
                    current_line = word + " "  # Start a new line with the current word
                else:
                    current_line += word + " "
            lines.append(current_line)  # Add the last line
            
            # Render the message lines from bottom to top
            for line in reversed(lines):
                if current_y < MESSAGE_LOG_Y:  # Don't draw above the message log's top
                    break
                text_surface = font.render(line, True, MESSAGE_LOG_TEXT_COLOR)
                screen.blit(text_surface, (x, current_y))
                current_y -= line_height  # Move the text up for the next line

# Replace this class definition in your existing code.

# Event class definition would go here
class Event:
    def __init__(self, description, function):
        self.description = description
        self.function = function

    def __call__(self, *args):
        return self.function(*args)
        
        



def find_treasure_event(player):
    gold_found = random.randint(10, 50)  # Randomize treasure value
    player.gold += gold_found  # Increment player's gold by found amount
    return f"You found {gold_found} gold!"
    
# Assume that ambush_event and other events now have basic implementations
def ambush_event(player):
        # Implement the actual ambush
        enemy = Enemy("Bandit", 30, 8, 2, [], {"Gold": 10})
        return f"You have been ambushed by a {enemy.name}!"

def find_ancient_artifact_event(game_manager):
    game_manager.message_log.add_message("You found an ancient artifact!")

def ghost_encounter_event(game_manager):
    # Placeholder for a ghost encounter
    ghost = Enemy("Ghost", 30, 12, 5, ["Haunt"], {"Ectoplasm": 1})
    game_manager.message_log.add_message("You encountered a ghost!")
    game_manager.start_combat(ghost)

find_treasure = Event("Find Treasure", find_treasure_event)
ambush = Event("Ambush", ambush_event)
find_artifact = Event("Find Artifact", find_ancient_artifact_event)
ghost_encounter = Event("Ghost Encounter", ghost_encounter_event)

event_functions = {
    "Find Treasure": find_treasure_event,
    "Ambush": ambush_event,
    "Find Artifact": find_ancient_artifact_event,
    "Ghost Encounter": ghost_encounter_event
}



class Location:
    def __init__(self, name, message_log, game_manager, description, events):
        self.name = name
        self.message_log = message_log
        self.description = description
        self.game_manager = game_manager
        self.events = events

    def display_event(self):
        # Randomly select an event to display
        current_event = random.choice(self.events)
        # Ensure that current_event is being called with the appropriate arguments
        current_event()

message_log = MessageLog()



# Button class definition would go here
class Button:
    def __init__(self, x, y, width, height, text, font, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.callback = callback
        self.hovered = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print("[DEBUG] Button pressed: {}", format(self.text))  # Debug statement
                self.callback()  # Call the button's callback function
        elif event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        
    def draw(self, screen):
        print(f'[DEBUG] Drawing button: {self.text}')  # Debug statement
        # Draw button background
        background_color = (100, 100, 100) if self.hovered else (200, 200, 200)
        pygame.draw.rect(screen, background_color, self.rect)
        # Draw button text
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class GUIManager:
    def __init__(self, screen, font, player, state):
        self.screen = screen
        self.font = font
        self.player = player
        self.buttons = []
        self.state = state

    
    def add_button(self, button):
        self.buttons.append(button)
        print("[DEBUG] Button added: {}", format(button.text))  # Debug statement
    
    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("[DEBUG] Clicked at: {}", format(event.pos))  # Debug statement
    
    def draw(self):
        print(f"[DEBUG] Drawing GUI. Number of buttons: {len(self.buttons)}")  # Debug statement
        # Go through all buttons and call their draw method
        for button in self.buttons:
            button.draw(self.screen)
        if self.state.state == States.COMBAT:
            self.draw_combat_actions()


        # Draw based on the state
        if self.state.state == States.EXPLORATION:
            pass # Add expolration buttons and call them 
        elif self.state.state == States.COMBAT:
            pass  # Add combat buttons and draw them
        elif self.state.state == States.INVENTORY:
            pass  # Draw the inventory screen
        elif self.state.state == States.MENU:
            pass  # Draw the main menu

        # Draw common UI elements, such as player stats
        self.draw_player_stats()

    def draw_player_stats(self):
        # Draw player stats now using self.player
        self.render_text(f"Health: {self.player.health}", (10, 10))
        self.render_text(f"Gold: {self.player.gold}", (10, 30))
        # Add more stats as needed

    def render_text(self, text, position, color=(0, 0, 0)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def draw_combat_actions(self, combat_manager):

        # Define and create buttons for combat actions here
        attack_button = Button(
            x=50, y=SCREEN_HEIGHT - 100,
            width=200, height=40,
            text='Attack',
            font=self.font,
            callback=lambda: combat_manager.perform_player_turn('attack')  # Call attack action
        )
        self.add_button(attack_button)

        # More buttons can be added here for different combat actions
     

class GameState:
    def __init__(self, player):
        self.player = player
        self.current_location = None
        self.state = States.EXPLORATION

    def change_state(self, new_state):
        print(f'[DEBUG] Changing state from {self.state} to {new_state}')  # Debug statement
        self.state = new_state

    


class GameManager:
    def __init__(self, screen, font):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()  # Initialize the clock
        self.player = Player("Hero")
        self.message_log = MessageLog()
        self.state = GameState(self.player)  # Create GameState instance here
        self.gui_manager = GUIManager(screen, font, self.player, self.state)  # Pass that 'state' instance to GUIManager
        self.combat_manager = None
        self.font = font
        self.initialize_game_world()
        self.enter_exploration()

    def enter_combat(self, enemy):
        # Logic to configure the game state for combat
        self.change_state(States.COMBAT)
        # Create a CombatManager instance with the required arguments
        self.combat_manager = CombatManager(self.player, enemy, self.font)
        # Pass the combat_manager instance to the GUIManager's draw_combat_actions method
        self.gui_manager.draw_combat_actions(self.combat_manager)

    def initialize_game_world(self):
    # Initialize this list here, now with correct Location initialization
        enchanted_forest_events = [find_treasure, lambda gm=self: gm.enter_combat(goblin)]  # Fixed lambda function
        abandoned_castle_events = [find_artifact, ghost_encounter]  # Ghost encounter already defined as needed
    
        self.locations = [
            Location(
                "Enchanted Forest",
                self.message_log,
                self,  # Pass correct reference to the GameManager
                "A mysterious forest filled with ancient trees and unknown creatures.",
                enchanted_forest_events
            ),
            Location(
                "Abandoned Castle",
                self.message_log,
                self,  # Pass correct reference to the GameManager
                "The ruins of a once-mighty castle, said to be haunted by spirits.",
                abandoned_castle_events
            ),
        ]
        self.state.current_location = self.locations[0]  # The first location in the list
    

    def enter_inventory(self):
        # Logic to enter the inventory state
        self.state.change_state(States.INVENTORY)


    def main_loop(self):
        while self.running:
            self.clock.tick(60)  # Limit the frame rate to 60 FPS

            # Get all events from pygame
            print('[DEBUG] Handling events')  # Debug statement
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            # Handle events based on game state
            if self.state.state == States.EXPLORATION:
                self.handle_exploration(events)  # Pass the events to the method
            elif self.state.state == States.COMBAT:
                self.handle_combat(events)  # Pass the events to the method
            elif self.state.state == States.INVENTORY:
                self.handle_inventory(events)  # Pass the events to the method
            elif self.state.state == States.MENU:
                self.handle_menu(events)  # Pass the events to the method

            self.update()

            if self.combat_manager and self.combat_manager.enemy.is_defeated():
                self.enter_exploration()

            self.render()


    def update(self):
    # Correct usage of f-string for debug print statement
        print(f"[DEBUG] Current game state: {self.state.state}")
        if self.state.state == States.COMBAT:
            self.combat_manager.update()

            # Check if the enemy is defeated and enter exploration if so
            if self.combat_manager.enemy.is_defeated():
                self.enter_exploration()

            # Check if the player has been marked as dead and reset game if so
            if hasattr(self.player, 'dead') and self.player.dead:
                self.reset_game()
            # Depending on your game you might want to handle other states here
    
    
    def render(self):
        """Called to draw the game screen."""
        print("[DEBUG] GameManager's render")  # Debug statement
        self.screen.fill(WHITE)

        # Ensuring combat interface only renders if in combat state
        if self.state.state == States.COMBAT and self.combat_manager is not None:
            self.combat_manager.draw(self.screen)

        # Draw GUI elements like buttons and player stats
        self.gui_manager.draw()

        # Render messages from the game's message log, in the bottom right corner
        self.message_log.render_messages(
            self.screen, 
            self.font, 
            MESSAGE_LOG_X + 5,  # Add some padding inside the box
            MESSAGE_LOG_Y + 5, 
            MESSAGE_LOG_LINE_HEIGHT
        )
        
        # Ensure that pygame.display.flip() is called at the end
        pygame.display.flip()




    def enter_exploration(self):
        print("[DEBUG] Entering exploration state.")  # Debug statement
        # Clear any existing buttons from the previous state
        self.state.change_state(States.EXPLORATION)
        self.gui_manager.buttons.clear()
        # Clear any previous location event messages
        self.message_log.messages.clear()

        # Display the current location name and description
        self.message_log.add_message(f"Current Location: {self.state.current_location.name}")
        self.message_log.add_message(self.state.current_location.description)

        self.render()
        print("Adding exploration buttons.")
        
        # Define properties for the inventory button
        button_x = 50  # X position of the button
        button_y = SCREEN_HEIGHT - 70  # Y position of the button, 70 pixels from the bottom
        button_width = 100  # Width of the button
        button_height = 50  # Height of the button
        button_text_inventory = 'Inventory'  # Text displayed on the button
        button_text_menu = 'Menu'
        button_text_travel = 'Travel'
        button_text_explore = 'Explore'

        # Create the inventory button
        inventory_button = Button(
            x=button_x,
            y=button_y,
            width=button_width,
            height=button_height,
            text=button_text_inventory,
            font=self.font,
            callback=lambda: self.enter_inventory() # Callback that calls the enter_inventory method
        )

        menu_button = Button(
            x=button_x,
            y=button_y - 60,
            width=button_width,
            height=button_height,
            text=button_text_menu,
            font=self.font,
            callback=lambda: self.enter_menu() # Callback that calls the enter_inventory method
        )

        explore_button = Button(
            x=button_x,
            y=button_y - 120,
            width=button_width,
            height=button_height,
            text=button_text_explore, # Make sure this is a string
            font=self.font,
             callback=lambda: self.handle_exploration(pygame.event.get())  # Trigger the handle_exploration function
        )

        travel = Button(
            x=button_x,
            y=button_y - 180,
            width=button_width,
            height=button_height,
            text=button_text_travel,
            font=self.font,
            callback=lambda: self.enter_travel_mode()
        )


        
        # Add the newly created button to the GUI manager
        self.gui_manager.add_button(travel)
        self.gui_manager.add_button(inventory_button)
        self.gui_manager.add_button(menu_button)
        self.gui_manager.add_button(explore_button)

        print(f"[DEBUG] Number of buttons after adding in enter_exploration: {len(self.gui_manager.buttons)}")
    
    def handle_exploration(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Assuming you want to trigger an event with a mouse click
                # You might want to check if the mouse click is in a certain region, add corresponding conditions if needed
                self.state.current_location.display_event()

    def display_event(self):
        # Randomly select an event to display
        current_event = random.choice(self.events)  # Call the event object
        current_event(self.game_manager)  # Pass game_manager to the event

    def enter_travel_mode(self):
        print("[DEBUG] Entering Travel state.")
        # Clear exploration buttons and add location buttons to the GUI manager
        self.state.change_state(States.TRAVEL)
        self.gui_manager.buttons.clear()
        self.add_location_buttons()

    def add_location_buttons(self):
        button_y_start = 50
        button_x = SCREEN_WIDTH // 2 - 100
        button_width = 200
        button_height = 50
        gap_between_buttons = 10

        # Make buttons for all locations to allow the player to select a new location
        for i, location in enumerate(self.locations):
            print(f"Location name: {location.name} (type: {type(location.name)})")
            button_y = button_y_start + i * (button_height + gap_between_buttons)
            location_button = Button(
                x=button_x,
                y=button_y,
                width=button_width,
                height=button_height,
                text=location.name,
                font=self.font,
                callback=lambda loc=location: self.travel_to_location(loc)
            )
            self.gui_manager.add_button(location_button)

    def enter_inventory(self):
        print("[DEBUG] Entering inventory state.")  # Debug statement
        self.state.change_state(States.INVENTORY)
        self.gui_manager.buttons.clear()
        print("Entered inventory state")  # For debugging purposes, replace with your actual implementation

        # Define properties for the inventory button
        button_x = 100  # X position of the button
        button_y = SCREEN_HEIGHT - 70  # Y position of the button, 70 pixels from the bottom
        button_width = 100  # Width of the button
        button_height = 30  # Height of the button
        button_text = 'Leave Inventory'  # Text displayed on the button
        
        # Create the inventory button
        inventory = Button(
            x=button_x,
            y=button_y,
            width=button_width,
            height=button_height,
            text=button_text,
            font=self.font,
            callback=lambda: self.enter_exploration()
        )

        self.gui_manager.add_button(inventory)
        print(f"[DEBUG] Number of buttons after adding in enter_exploration: {len(self.gui_manager.buttons)}")
    
    def enter_menu(self):
        # Prepare main menu UI elements
        print("[DEBUG] Entering Menu state.")  # Debug statement
        self.state.change_state(States.MENU)
        self.gui_manager.buttons.clear()
        print("Entered Menu state")  # For debugging purposes, replace with your actual implementation

        # Define properties for the inventory button
        button_x = 100  # X position of the button
        button_y = SCREEN_HEIGHT - 70  # Y position of the button, 70 pixels from the bottom
        button_width = 100  # Width of the button
        button_height = 30  # Height of the button
        button_text_return = 'Return'  # Text displayed on the button
        button_text_quit_game = 'Quit Game'


         # Create the quit_game button

        quit_game = Button(
            x=button_x,
            y=button_y - 60,
            width=button_width,
            height=button_height,
            text=button_text_quit_game,
            font=self.font,
            callback=lambda: pygame.quit()
        )


        # Create the inventory button

        back = Button(
            x=button_x,
            y=button_y,
            width=button_width,
            height=button_height,
            text=button_text_return,
            font=self.font,
            callback=lambda: self.enter_exploration()
        )

        self.gui_manager.add_button(quit_game)
        self.gui_manager.add_button(back)
        print(f"[DEBUG] Number of buttons after adding in enter_exploration: {len(self.gui_manager.buttons)}")

    def travel_to_location(self, location):
        # Travel to a new location and enter exploration mode there
        self.state.current_location = location
        self.enter_exploration()
        
        # Add the name and description of the new location
        self.message_log.add_message(f"You have arrived at the {location.name}.")
        self.message_log.add_message(location.description)

        # Call render to update the display
        self.render()

    
    def enter_combat(self, enemy):
        # Prepare the combat state
        self.state.change_state(States.COMBAT)
        self.combat_manager = CombatManager(self.player, enemy, self.font)
        self.gui_manager.buttons.clear()  # Clear non-combat buttons
        self.gui_manager.draw_combat_actions()  # Draw combat action buttons

    def handle_combat(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.gui_manager.buttons:
                    button.handle_event(event)
        # Add checks here for combat resolution - win/lose, transitions back to exploration 

    def draw_combat_actions(self):
        attack_button = Button(
            x=50, y=SCREEN_HEIGHT - 150,  # Position the button appropriately
            width=100, height=50,
            text='Attack',
            font=self.font,
            callback=lambda: self.combat_manager.perform_player_turn('attack')
        )

        self.buttons.append(attack_button)  # Add the attack button to the list
        # Repeat this for other combat buttons you create
    
    ghost_encounter = Event("Ghost Encounter", ghost_encounter_event)

    
    def handle_inventory(self, events):
        # Inventory management logic goes here
        pass

    def handle_menu(self, events):
        # Menu interaction logic goes here
        pass
    
    
    def open_inventory(self):
        self.state.change_state(States.INVENTORY)
    
    def enter_location(self, location):
        self.state.change_state(States.EXPLORATION)
        self.state.current_location = location

    def reset_game(self):
        # Reset the player state and any other necessary game states
        print("Game Over! Resetting game state.")
        self.player = Player("Hero")
        self.message_log = MessageLog()
        self.state = GameState(self.player)  # Reset game state to exploration
        self.gui_manager = GUIManager(self.screen, self.font, self.player, self.state)
        self.initialize_game_world()  # Reinitialize locations and possibly reset the player to a safe spot
        self.enter_exploration()  # Make sure the player goes back to exploration state
    
def initialize_game_world(self):
    # Corrected usage; pass string literals as location names
    self.locations = [
        Location(
            "Enchanted Forest", # Pass the location name as a string
            "A mysterious forest filled with ancient trees and unknown creatures.",
            [goblin],
            [find_treasure, lambda gm=self: self.enter_combat(goblin)]
        ),
        Location(
            "Abandoned Castle", # Pass the location name as a string
            "The ruins of a once-mighty castle, said to be haunted by spirits.",
            [dragon],
            [find_artifact, ghost_encounter]
        ),
    ]

class Inventory:
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        self.items.append(item)
    
    # Methods for removing items, using items, and so on

class Item:
    def __init__(self, name, description, effect):
        self.name = name
        self.description = description
        self.effect = effect

    def use_item(item_key, player, target=None):
        item = items[item_key]
        if 'effect' in item:
            item['effect'](target if target else player)  # Use the effect on the target or the player
        elif 'ally' in item:
            player.summon_ally(item['ally'])

        # Define the item dictionary with complex items
            items = {
                'mystic_sword': {
                    'name': 'Mystic Sword',
                    'description': 'A sword imbued with ancient magic.',
                    'effect': lambda target: target.take_damage(50),  # Example effect function
                },
                'healing_potion': {
                    'name': 'Healing Potion',
                    'description': 'Restores 30 points of health.',
                    'effect': lambda target: target.heal(30),  # Example effect function
                },
                'summoning_scroll': {
                    'name': 'Summoning Scroll',
                    'description': 'Summons a powerful ally to fight alongside you.',
                    'ally': Ally('Guardian Spirit', 100, 15, ['Guardian Shield']),  # Summon an ally
                    'effect': lambda player: player.summon_ally('Guardian Spirit'),
                }
            }

class Ability:
    def __init__(self, name, power, cost):
        self.name = name
        self.power = power
        self.cost = cost

    def cast(self, caster, target):
        # Apply the ability's effect, possibly checking for enough resource
        pass

class CombatManager:
    def __init__(self, player, enemy, font):
        self.player = player
        self.enemy = enemy
        self.font = font
        self.combat_log = MessageLog()
        self.player_turn = True 

    def perform_player_turn(self, action):
        if action == "attack":
            damage = max(self.player.attack - self.enemy.defense, 0)
            self.enemy.take_damage(damage)
            self.combat_log.add_message(f"You attack the {self.enemy.name} for {damage} damage.")
            self.player_turn = False
        # Add other actions like defend or use item here

    def perform_enemy_turn(self):
        if not self.enemy.is_defeated():
            damage = max(self.enemy.attack - self.player.defense, 0)
            self.player.take_damage(damage)
            self.combat_log.add_message(f"The {self.enemy.name} attacks you for {damage} damage.")
            self.player_turn = True

    def update(self):
        if not self.player_turn:
            self.perform_enemy_turn()

    def draw(self, screen):
        # Later this will draw each action the player or enemy takes
        pass

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cultivation Game")
    font = pygame.font.SysFont(None, 24)  # None sets the default font, 24 is the size

    game_manager = GameManager(screen, font)
    game_manager.main_loop()

    pygame.quit()

if __name__ == '__main__':
    main()
