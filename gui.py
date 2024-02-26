import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
from searching import Searching


class ApartmentIntrusionDetector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg='white')  # Set background color to a dim shade of blue
        self.label1 = tk.Label(self.root, text='Intruder Detection and Localization',font=('HelvLight',20),bg = 'white')
        self.label1.pack(padx= 20,pady=20)

        self.simul_btn = tk.Button(self.root, text='Start', command=self.simul)
        self.simul_btn.pack(padx= 20,pady=20)

        self.exit_btn = tk.Button(self.root, text='Exit', command=self.root.destroy)
        self.exit_btn.pack(padx= 20,pady=5)

        self.winCentre(self.root)
        self.searcher = Searching()

    def winCentre(self, window):
        app_Width = 900
        app_Height = 700
        swidth = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (swidth / 2) - (app_Width / 2)
        y = (screen_height / 2) - (app_Height / 2)
        window.geometry(f'{app_Width}x{app_Height}+{int(x)}+{int(y)}')

    def finding_shortest_path(self):
        output = self.searcher.get_output()
        messagebox.showinfo("Output", output)

    def simul(self):
        self.root.withdraw()
        simul_win = tk.Toplevel()
        self.winCentre(simul_win)
        simul_win.configure(bg = 'white')
        label1 = tk.Label(simul_win, text='Intrusion Simulation', font=('HelvLight', 20),bg = 'white')
        label1.pack(padx= 20,pady=20)

        label2 = tk.Label(simul_win, text='The following intrusion is tested 6-story apartment complex which has 4 apartments on each floor',
                          font=('HelvLight', 15),bg = 'white')
        label2.pack(padx= 20,pady=20)

        apartment_img = ImageTk.PhotoImage(Image.open('images/Apartment.png').resize((400, 400), Image.LANCZOS))
        apartment_label = tk.Label(simul_win, image=apartment_img)
        apartment_label.image = apartment_img
        apartment_label.pack(padx= 20,pady=20)

        detection_btn = tk.Button(simul_win, text='Run Detection', command=self.finding_shortest_path)
        detection_btn.pack(padx= 20,pady=20)

        exit_btn = tk.Button(simul_win, text='Exit', command=simul_win.destroy)
        exit_btn.pack(padx= 20,pady=5)

        simul_win.mainloop()

    def run(self):
        self.winCentre(self.root)
        self.root.mainloop()


if __name__ == '__main__':
    app = ApartmentIntrusionDetector()
    app.run()
