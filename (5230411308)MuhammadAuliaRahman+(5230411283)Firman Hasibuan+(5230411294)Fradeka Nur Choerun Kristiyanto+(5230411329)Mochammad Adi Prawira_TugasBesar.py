import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector


# Inisialisasi database
def init_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bioskop"
    )
    cur = conn.cursor()

    # Drop table if exists and create table
    cur.execute("DROP TABLE IF EXISTS movies")
    cur.execute("""
        CREATE TABLE movies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            studio VARCHAR(255),
            showtimes VARCHAR(255),
            seat_number VARCHAR(50)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


# Fungsi untuk menampilkan seluruh data film
def show_all_movies():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bioskop"
    )
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies')
    movies = cursor.fetchall()
    conn.close()

    # Menampilkan data dalam messagebox
    movies_text = "\n".join([f"id: {movie[0]},Name: {movie[1]}, Studio: {movie[2]}, Showtimes: {movie[3]}, Seats: {movie[4]}" for movie in movies])
    messagebox.showinfo("Daftar Film", movies_text if movies else "Tidak ada data film.")

# Fungsi untuk menambah data film
def add_movie(name, studio, showtimes, seats):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bioskop"
    )
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO movies (name, studio, showtimes, seat_number)
    VALUES (%s, %s, %s, %s)
    ''', (name, studio, showtimes, seats))
    conn.commit()
    conn.close()

# Fungsi untuk menghapus data film berdasarkan ID
def delete_movie(movie_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bioskop"
    )
    cursor = conn.cursor()
    cursor.execute('DELETE FROM movies WHERE id = %s', (movie_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
# Fungsi untuk mengupdate data film
def update_movie(id, name, studio, showtimes, seats):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bioskop"
    )
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE movies
    SET name = %s, studio = %s, showtimes = %s, seat_number = %s
    WHERE id = %s
    ''', (name, studio, showtimes, seats, id,))
    conn.commit()
    conn.close()

class TicketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Tiket Bioskop")
        self.root.geometry("500x500")

        # Inisialisasi database
        init_db()

        self.widget_create()

    def widget_create(self):
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menambahkan menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=file_menu)
        file_menu.add_command(label="Tampilkan Semua Data", command=show_all_movies)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.root.quit)

        manage_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Kelola Data Film", menu=manage_menu)
        manage_menu.add_command(label="Tambah Data Film", command=self.add_movie_window)
        manage_menu.add_command(label="Edit Data Film", command=self.edit_movie_window)
        manage_menu.add_command(label="Hapus Data Film", command=self.delete_movie_window)

        # Label judul
        title_label = tk.Label(self.root, text="Aplikasi Tiket Bioskop", font=("Arial", 16))
        title_label.pack(pady=10)

        # Pilihan film
        self.movie_label = tk.Label(self.root, text="Pilih Film:")
        self.movie_label.pack()
        self.movie_combobox = ttk.Combobox(self.root)
        self.movie_combobox.pack()
        self.movie_combobox.bind("<<ComboboxSelected>>", self.update_showtimes)

        # Pemilihan jadwal film
        self.showtime_label = tk.Label(self.root, text="Pilih Jadwal Tayang:")
        self.showtime_label.pack()
        self.showtime_combobox = ttk.Combobox(self.root)
        self.showtime_combobox.pack()
        self.showtime_combobox.bind("<<ComboboxSelected>>", self.update_showtimes)

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

        self.update_movie_combobox()  # Memperbarui daftar film

    def update_showtimes(self, event):
        selected_movie = self.movie_combobox.get()
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bioskop"
    )
        cursor = conn.cursor()
        cursor.execute('SELECT showtimes FROM movies WHERE name = %s', (selected_movie,))
        showtimes = cursor.fetchone()[0].split(",")
        conn.close()

        self.showtime_combobox['values'] = showtimes
        self.showtime_combobox.current(0)

    def generate_ticket(self):
        movie = self.movie_combobox.get().strip()
        showtime = self.showtime_combobox.get().strip()
        seat = self.seat_spinbox.get().strip()

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
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bioskop"
        )
        cursor = conn.cursor()
        cursor.execute('SELECT studio FROM movies WHERE name = %s', (movie,))
        studio = cursor.fetchone()[0]
        conn.close()

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


    def update_movie_combobox(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bioskop"
        )
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM movies')
        movies = cursor.fetchall()
        conn.close()

        movie_names = [movie[0] for movie in movies]
        self.movie_combobox['values'] = movie_names
        if movie_names:
            self.movie_combobox.current(0)
            self.update_showtimes(None)


    def new_method(self, conn):
        cursor = conn.cursor()
        return cursor # Memperbarui jadwal tayang berdasarkan film pertama

    def add_movie_window(self):
        # Jendela untuk menambah data film baru
        add_window = tk.Toplevel(self.root)
        add_window.title("Tambah Data Film")

        name_label = tk.Label(add_window, text="Nama Film:")
        name_label.pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()

        studio_label = tk.Label(add_window, text="Studio:")
        studio_label.pack()
        studio_entry = tk.Entry(add_window)
        studio_entry.pack()

        showtimes_label = tk.Label(add_window, text="Jadwal Tayang (pisahkan dengan koma):")
        showtimes_label.pack()
        showtimes_entry = tk.Entry(add_window)
        showtimes_entry.pack()

        seats_label = tk.Label(add_window, text="Jumlah Kursi:")
        seats_label.pack()
        seats_entry = tk.Entry(add_window)
        seats_entry.pack()

        def save_movie():
            name = name_entry.get()
            studio = studio_entry.get()
            showtimes = showtimes_entry.get()
            seats = seats_entry.get()

            if name and studio and showtimes and seats.isdigit():
                add_movie(name, studio, showtimes, int(seats))
                messagebox.showinfo("Sukses", "Film berhasil ditambahkan!")
                add_window.destroy()
                self.update_movie_combobox()  # Memperbarui combobox film setelah menambah data
            else:
                messagebox.showerror("Error", "Silakan isi semua data dengan benar!")

        save_button = tk.Button(add_window, text="Simpan", command=save_movie)
        save_button.pack(pady=10)

    def edit_movie_window(self):
        # Jendela untuk mengedit data film
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Data Film")

        # Ambil daftar film dari database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bioskop"
        )
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM movies')
        movies = cursor.fetchall()
        conn.close()

        if not movies:
            messagebox.showinfo("Info", "Tidak ada film untuk diedit.")
            return

        movie_names = [movie[1] for movie in movies]
        movie_combobox = ttk.Combobox(edit_window, values=movie_names)
        movie_combobox.pack()

        name_label = tk.Label(edit_window, text="Nama Film Baru:")
        name_label.pack()
        name_entry = tk.Entry(edit_window)
        name_entry.pack()

        studio_label = tk.Label(edit_window, text="Studio Baru:")
        studio_label.pack()
        studio_entry = tk.Entry(edit_window)
        studio_entry.pack()

        showtimes_label = tk.Label(edit_window, text="Jadwal Tayang Baru (pisahkan dengan koma):")
        showtimes_label.pack()
        showtimes_entry = tk.Entry(edit_window)
        showtimes_entry.pack()

        seats_label = tk.Label(edit_window, text="Jumlah Kursi Baru:")
        seats_label.pack()
        seats_entry = tk.Entry(edit_window)
        seats_entry.pack()

        def save_edit():
            movie_name = movie_combobox.get()
            movie_id = next(movie[0] for movie in movies if movie[1] == movie_name)
            name = name_entry.get()
            studio = studio_entry.get()
            showtimes = showtimes_entry.get()
            seats = seats_entry.get()

            if name and studio and showtimes and seats.isdigit():
                update_movie(movie_id, name, studio, showtimes, int(seats))
                messagebox.showinfo("Sukses", "Data film berhasil diperbarui!")
                edit_window.destroy()
                self.update_movie_combobox()  # Memperbarui combobox film setelah mengedit data
            else:
                messagebox.showerror("Error", "Silakan isi semua data dengan benar!")

        save_button = tk.Button(edit_window, text="Simpan Perubahan", command=save_edit)
        save_button.pack(pady=10)

    def delete_movie_window(self):
        # Jendela untuk menghapus data film
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Hapus Data Film")

        # Ambil daftar film dari database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bioskop"
        )
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM movies')
        movies = cursor.fetchall()
        conn.close()

        if not movies:
            messagebox.showinfo("Info", "Tidak ada film untuk dihapus.")
            return

        movie_names = [movie[1] for movie in movies]
        movie_combobox = ttk.Combobox(delete_window, values=movie_names)
        movie_combobox.pack()

        def delete_movie_data():
            movie_name = movie_combobox.get()
            movie_id = next(movie[0] for movie in movies if movie[1] == movie_name)
            delete_movie(movie_id)
            messagebox.showinfo("Sukses", f"Film '{movie_name}' berhasil dihapus!")
            delete_window.destroy()
            self.update_movie_combobox()  # Memperbarui combobox film setelah menghapus data

        delete_button = tk.Button(delete_window, text="Hapus Film", command=delete_movie_data)
        delete_button.pack(pady=10)


if __name__ == '__main__':
    root = tk.Tk()
    app = TicketApp(root)
    root.mainloop()
