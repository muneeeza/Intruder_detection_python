import tkinter as tk
from PIL import ImageTk, Image
import pandas as pd
from searching import ApartmentIntrusionSolver
from ApartmentSprite import Apartment
from tkinter import messagebox



class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.label1 = tk.Label(self.root, text='Intruder Detection and Localization')
        self.label1.pack()
        self.simul_btn = tk.Button(self.root, text='Start', command=self.simul)
        self.simul_btn.pack()
        self.exit_btn = tk.Button(self.root, text='Exit', command=self.root.destroy)
        self.exit_btn.pack()
        self.winCentre()

        # Image instances
        self.broken_window_img = None
        self.broken_lock_img = None
        self.safe_img = None
        self.both_broken_img = None

    def winCentre(self):
        app_Width = 800
        app_Height = 600
        swidth = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (swidth / 2) - (app_Width / 2)
        y = (screen_height / 2) - (app_Height / 2)
        self.root.geometry(f'{app_Width}x{app_Height}+{int(x)}+{int(y)}')

    def load_images(self):
        self.broken_window_img = ImageTk.PhotoImage(
            Image.open('images/broken_window_only.png').resize((50, 50), Image.LANCZOS)
        )
        self.broken_lock_img = ImageTk.PhotoImage(
            Image.open('images/broken_lock_only.png').resize((100, 100), Image.LANCZOS)
        )
        self.nothing_broken_img = ImageTk.PhotoImage(
            Image.open('images/nothing_broken.png').resize((100, 100), Image.LANCZOS)
        )
        self.both_broken_img = ImageTk.PhotoImage(
            Image.open('images/broken_window_lock.png').resize((100, 100), Image.LANCZOS)
        )

    # ...
    # ...
    def simul(self):
        self.root.withdraw()
        simul_win = tk.Toplevel()
        simul_win.geometry('+50+50')  # Position the window at (50, 50) on the screen
        label1 = tk.Label(simul_win, text='Intrusion Simulation', font=20)
        label1.grid(row=0, column=0, padx=20, pady=20)  # Use grid() instead of pack()
        label2 = tk.Label(simul_win,
                          text='The following intrusion is tested 6-story apartment complex which has 4 apartments on each floor',
                          font=15)
        label2.grid(row=1, column=0)  # Use grid() instead of pack()

        broken_window_img = ImageTk.PhotoImage(
            Image.open('images/broken_window_only.png').resize((100, 100), Image.LANCZOS))
        broken_lock_img = ImageTk.PhotoImage(
            Image.open('images/broken_lock_only.png').resize((100, 100), Image.LANCZOS))
        nothing_broken_img = ImageTk.PhotoImage(
            Image.open('images/nothing_broken.png').resize((100, 100), Image.LANCZOS))
        both_broken_img = ImageTk.PhotoImage(
            Image.open('images/broken_window_lock.png').resize((100, 100), Image.LANCZOS))

        solver = ApartmentIntrusionSolver()
        solver.generate_intrusion()
        apartment_list = solver.locations
        target_apartment = solver.get_broken_apartments()
        # After generating the intrusion and creating the apartment_list
        df = pd.DataFrame(apartment_list, columns=['Floor', 'Apartment'])

        # calculating unique num of floors and apartments
        num_floors = df['Floor'].nunique()
        num_apartments = df['Apartment'].nunique()

        for index, row in df.iterrows():
            floor = row['Floor']
            apartment = row['Apartment']
            apartment_data = solver.apartments.loc[
                (solver.apartments['Floor'] == floor) & (solver.apartments['Apartment'] == apartment)]
            broken_window = apartment_data['Broken Window'].values[0]
            broken_lock = apartment_data['Broken Lock'].values[0]
            if target_apartment == (floor, apartment) and broken_lock and broken_window:
                both_broken_label = tk.Label(simul_win, image=both_broken_img)
                both_broken_label.image = both_broken_img  # Associate the image with the label
                both_broken_label.grid(row=floor + 2, column=apartment, padx=10, pady=10, sticky="nsew")  # Adjust row index
            elif broken_window:
                broken_window_label = tk.Label(simul_win, image=broken_window_img)
                broken_window_label.image = broken_window_img  # Associate the image with the label
                broken_window_label.grid(row=floor + 2, column=apartment, padx=10, pady=10, sticky="nsew")  # Adjust row index
            elif broken_lock:
                broken_lock_label = tk.Label(simul_win, image=broken_lock_img)
                broken_lock_label.image = broken_lock_img  # Associate the image with the label
                broken_lock_label.grid(row=floor + 2, column=apartment, padx=10, pady=10, sticky="nsew")  # Adjust row index
            else:
                nothing_broken_label = tk.Label(simul_win, image=nothing_broken_img)
                nothing_broken_label.image = nothing_broken_img  # Associate the image with the label
                nothing_broken_label.grid(row=floor + 2, column=apartment, padx=10, pady=10)
        # Find the shortest path
        start_apartment = (1, 1)
        end_apartment = target_apartment
        path = solver._perform_astar_search(start_apartment, end_apartment)

        if path:
            # Display the path using a pop-up message box
            path_message = "Shortest Path to the Apartment Intrusion:\n"
            for apt in path:
                path_message += f"Floor: {apt[0]}, Apartment: {apt[1]}\n"
            messagebox.showinfo("Shortest Path", path_message)
        else:
            messagebox.showinfo("Shortest Path", "No path found to the end apartment.")

    # ...

    def run(self):
        self.winCentre()
        self.root.mainloop()


if __name__ == '__main__':
    app = GUI()
    app.run()
