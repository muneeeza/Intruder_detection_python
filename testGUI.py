import tkinter as tk
import pandas as pd
import pygame
from ApartmentSprite import Apartment
import random
from searching import ApartmentIntrusionSolver
from buttons import Button

root = tk.Tk()
label1 = tk.Label(root, text='Intruder Detection and Localization')
label1.pack()


def winCentre(window):
    app_Width = 800
    app_Height = 600
    swidth = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (swidth / 2) - (app_Width / 2)
    y = (screen_height / 2) - (app_Height / 2)
    window.geometry(f'{app_Width}x{app_Height}+{int(x)}+{int(y)}')


def buttons(screen):
    start_img = pygame.image.load('images/start.png').convert_alpha()
    exit_img = pygame.image.load('images/exit.png').convert_alpha()

    button_margin = 20  # Set the margin between buttons

    # Calculate the positions of the buttons on the right side of the screen
    start_x = screen.get_width() - start_img.get_width() - button_margin
    start_y = button_margin

    exit_x = screen.get_width() - exit_img.get_width() - button_margin
    exit_y = start_y + start_img.get_height() + button_margin

    start_button = Button(start_x, start_y, start_img, 0.3)
    exit_button = Button(exit_x, exit_y, exit_img, 0.3)

    start_button.draw(screen)
    exit_button.draw(screen)


def simul():
    root.withdraw()
    # Initialize pygame
    pygame.init()

    screen_width, screen_height = 1200, 800  # Set your desired screen dimensions

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Intrusion Simulation')

    rect_x = 20
    rect_y = 20
    # Assuming you have a class called ApartmentList
    solver = ApartmentIntrusionSolver()  # Create an instance of the ApartmentIntrusionSolver class
    solver.generate_intrusion()  # Generate intrusion in the apartments
    apartment_list = solver.locations
    target_apartment = solver.get_broken_apartments()
    # After generating the intrusion and creating the apartment_list
    df = pd.DataFrame(apartment_list, columns=['Floor', 'Apartment'])
    all_sprites = pygame.sprite.Group()

    # calculating unique num of floors and apartments
    num_floors = df['Floor'].nunique()
    num_apartments = df['Apartment'].nunique()

    window_width, window_height = 100, 100  # Set the dimensions of your window sprite
    total_width = num_apartments * window_width
    total_height = num_floors * window_height

    start_x = (screen_width - total_width) // 2
    start_y = (screen_height - total_height) // 2

    for index, row in df.iterrows():
        floor = row['Floor']
        apartment = row['Apartment']
        window_x = start_x + (apartment - 1) * window_width
        window_y = start_y + (floor - 1) * window_height
        apartment_data = solver.apartments.loc[
            (solver.apartments['Floor'] == floor) & (solver.apartments['Apartment'] == apartment)]
        if not apartment_data.empty:
            broken_window = apartment_data['Broken Window'].values[0]
            broken_lock = apartment_data['Broken Lock'].values[0]
            print(f"Target Apartment: {target_apartment}")
            print(f"Floor: {floor}, Apartment: {apartment}")
            print(f"Broken Window: {broken_window}, Broken Lock: {broken_lock}")

            if target_apartment == (floor, apartment) and broken_lock and broken_window:
                window = Apartment(window_x, window_y, window_width, window_height, True, True)
                all_sprites.add(window)
                print(f"Target Apartment: {target_apartment}")
                print(f"Floor: {floor}, Apartment: {apartment}")
                print(f"Broken Window: {broken_window}, Broken Lock: {broken_lock}")

            elif broken_window:
                window = Apartment(window_x, window_y, window_width, window_height, True, False)
                all_sprites.add(window)
                print(f"Target Apartment: {target_apartment}")
                print(f"Floor: {floor}, Apartment: {apartment}")
                print(f"Broken Window: {broken_window}, Broken Lock: {broken_lock}")

            elif broken_lock:
                window = Apartment(window_x, window_y, window_width, window_height, False, True)
                all_sprites.add(window)
                print(f"Target Apartment: {target_apartment}")
                print(f"Floor: {floor}, Apartment: {apartment}")
                print(f"Broken Window: {broken_window}, Broken Lock: {broken_lock}")

            else:
                window = Apartment(window_x, window_y, window_width, window_height, False, False)
                all_sprites.add(window)
                print(f"Target Apartment: {target_apartment}")
                print(f"Floor: {floor}, Apartment: {apartment}")
                print(f"Broken Window: {broken_window}, Broken Lock: {broken_lock}")

    # Continue with your code...
    # Call the buttons function to draw buttons on the screen
    # buttons(screen)

    while running[0]:
        screen.fill((202, 228, 241))
        # Poll for events
        # pygame.QUIT event means the user clicked X to close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running[0] = False
        # Call the buttons function to draw buttons on the screen
        buttons(screen)
        # Clear the screen
        # Draw all sprites onto the screen
        all_sprites.draw(screen)
        # Flip the display to put your work on screen
        pygame.display.flip()

    pygame.quit()


running = [True]  # Create a list to hold the running state
simul_btn = tk.Button(root, text='Start', command=lambda: simul())
simul_btn.pack()
exit_btn = tk.Button(root, text='Exit', command=root.destroy)
exit_btn.pack()
winCentre(root)
root.mainloop()
