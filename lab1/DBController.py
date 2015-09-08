import DataBase
import pickle


class DBController:
    def __init__(self):
        try:
            _bd_txt = open("db.txt", "rb")
            self.db = pickle.load(_bd_txt)
            _bd_txt.close()
        except IOError:
            self.db = DataBase.DataBase()

    def add_good(self):
        id_of_good = raw_input("Id of good: ")
        name = raw_input("Name: ")
        price = raw_input("Price: ")
        attribute = raw_input("Attribute: ")
        try:
            self.db.add_good(int(id_of_good), str(name), int(price), str(attribute))
        except ValueError:
            print "There are invalid values. Try again!"

    def add_order(self):
        id_of_order = raw_input("Id of order: ")
        name = raw_input("Name: ")
        category = raw_input("Category: ")
        id_of_good = raw_input("Id of good: ")
        try:
            self.db.add_order(int(id_of_order), str(name), str(category), int(id_of_good))
        except ValueError:
            print "There are invalid values. Try again!"

    def change_good_by_id(self):
        id_of_good = raw_input("Change good with id: ")
        try:
            self.db.change_good_with_id(int(id_of_good))
        except ValueError:
            print "There are invalid values. Try again!"

    def change_order_by_id(self):
        id_of_order = raw_input("Change order with id: ")
        try:
            self.db.change_order_with_id(int(id_of_order))
        except ValueError:
            print "There are invalid values. Try again!"

    def show_good_by_id(self):
        id_of_good = raw_input("Show good with id: ")
        try:
            self.db.print_good_with_id(int(id_of_good))
        except ValueError:
            print "There are invalid values. Try again!"

    def show_order_by_id(self):
        id_of_order = raw_input("Show order with id: ")
        try:
            self.db.print_order_with_id(int(id_of_order))
        except ValueError:
            print "There are invalid values. Try again!"

    def show_all_goods(self):
        self.db.print_all_goods()

    def show_all_orders(self):
        self.db.print_all_orders()

    def find_orders_with_price(self):
        price_control = raw_input("Find orders with price, bigger then: ")
        try:
            self.db.print_all_orders_with_price_bigger_then(int(price_control))
        except ValueError:
            print "There are invalid values. Try again!"

    def delete_good_by_id(self):
        id_of_good = raw_input("Delete good with id: ")
        try:
            self.db.delete_good_with_id(int(id_of_good))
        except ValueError:
            print "There are invalid values. Try again!"

    def delete_order_by_id(self):
        id_of_order = raw_input("Delete order with id: ")
        try:
            self.db.delete_order_with_id(int(id_of_order))
        except ValueError:
            print "There are invalid values. Try again!"

    def exit_from_program(self):
        _bd_txt = open("db.txt", "wb")
        pickle.dump(self.db, _bd_txt)
        _bd_txt.close()
