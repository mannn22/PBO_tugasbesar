import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


movies = {
    "Alien VS Predator": {"showtimes": ["10:00", "13:00", "16:00"], "seats": 50, "studio": "Studio 1"},
    "The Avengers": {"showtimes": ["11:00", "14:00", "17:00"], "seats": 50, "studio": "Studio 2"},
    "Pus in Both 2": {"showtimes": ["12:00", "15:00", "18:00"], "seats": 50, "studio": "Studio 3"},
    "Pengabdi Setan": {"showtimes": ["09:00", "12:00", "15:00"], "seats": 50, "studio": "Studio 4"},
    "Gladiator II": {"showtimes": ["10:30", "13:30", "16:30"], "seats": 50, "studio": "Studio 5"},
    "John Wick": {"showtimes": ["13:30", "17:00", "20:30"], "seats": 50, "studio": "Studio 6"},
    "moana": {"showtimes": ["09:30", "15:00", "18:30"], "seats": 50, "studio": "Studio 7"},
}

class TicketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Tiket Bioskop")
        self.root.geometry("400x400")
        
        self.widget_create()

    def widget_create(self):
        title_label = tk.Label(self.root, text="Aplikasi Tiket Bioskop", font=("Arial", 16))
        title_label.pack(pady=10)

        # Pilihan film
        self.movie_label = tk.Label(self.root, text="Pilih Film:")
        self.movie_label.pack()
        self.movie_combobox = ttk.Combobox(self.root, values=list(movies.keys()))
        self.movie_combobox.pack()
        self.movie_combobox.bind("<<ComboboxSelected>>", self.update_showtimes)

        # Pemilihan jadwal film
        self.showtime_label = tk.Label(self.root, text="Pilih Jadwal Tayang:")
        self.showtime_label.pack()
        self.showtime_combobox = ttk.Combobox(self.root)
        self.showtime_combobox.pack()

        # Pemilihan kursi bioskop
        self.seat_label = tk.Label(self.root, text="Pilih Kursi:")
        self.seat_label.pack()
        self.seat_spinbox = tk.Spinbox(self.root, from_=1, to=50)
        self.seat_spinbox.pack()

        # Tombol untuk menghasilkan tiket
        self.generate_button = tk.Button(self.root, text="Cetak Tiket", command=self.generate_ticket)
        self.generate_button.pack(pady=10)

        # Menampilkan tiket
        self.ticket_display = tk.Label(self.root, text="", justify="left", font=("Arial", 12), bg="lightgray", relief="sunken", padx=10, pady=10)
        self.ticket_display.pack(pady=15)

    def update_showtimes(self, event):
        selected_movie = self.movie_combobox.get()
        showtimes = movies[selected_movie]["showtimes"]
        self.showtime_combobox['values'] = showtimes
        self.showtime_combobox.current(0)
        
    def generate_ticket(self):
        movie = self.movie_combobox.get().strip()
        showtime = self.showtime_combobox.get().strip()
        seat = self.seat_spinbox.get().strip()

        # Validasi input
        if not movie:
            messagebox.showerror("Error", "Silakan pilih film!")
            return
        if not showtime:
            messagebox.showerror("Error", "Silakan pilih jadwal tayang!")
            return
        if not seat.isdigit() or int(seat) <= 0 or int(seat) > 50:
            messagebox.showerror("Error", "Silakan pilih kursi yang valid (1-50)!")
            return

        tanggal = datetime.now().strftime("%d %B %Y")
        studio = movies[movie]["studio"]

        ticket_text = (
            f"====================\n"
            f"        BIOSKOP 69      \n"
            f"====================\n"
            f"Film: {movie}\n"
            f"Studio: {studio}\n" 
            f"Tanggal: {tanggal}\n"  
            f"Jadwal: {showtime}\n"
            f"Kursi: {seat}\n"
            f"====================\n"
            f"Terima kasih telah memesan!\n"
            f"===================="
        )

        self.ticket_display.config(text=ticket_text)

if __name__ == '__main__':
    root = tk.Tk()
    app = TicketApp(root)
    root.mainloop()
