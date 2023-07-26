from tkinter import ttk
from tkinter import *

import sqlite3

class Product:

    db_name = 'database.db'

    
    def __init__(self, window):
        self.wind = window
        self.wind.title('Punto de Venta')

        # Creating a Frame Container
        frame = LabelFrame(self.wind, text = 'Agregar un nuevo producto')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
        
        # Name Input
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        #Price Input
        Label(frame, text = 'Precio: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        #Button add Product
        ttk.Button(frame, text = 'Guardar Producto', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

        # Output messages
        self. message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Table
        self.tree = ttk.Treeview(height = 10, columns= 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Precio', anchor = CENTER)

        self.get_products()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def get_products(self):
        # Cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # Quearing Data
        query = 'SELECT * FROM Productos ORDER BY nombre DESC'
        db_rows = self.run_query(query)
        # Filling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])
        
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0 

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO Productos VALUES(NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            print('Datos guardados')
        else:
            print('Nombre y Precio es requerido')
        self.get_products()


if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
