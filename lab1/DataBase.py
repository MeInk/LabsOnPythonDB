import Good
import Order


class DataBase:
    def __init__(self):
        self.goods = []
        self.orders = []

    def add_good(self, id_of_good, name, price, attribute):
        id_is_free = True
        for good in self.goods:
            if good.id_of_good == id_of_good:
                id_is_free = False
                break
        if id_is_free:
            self.goods.append(Good.Good(id_of_good, name, price, attribute))
            self.goods.sort(key=lambda x: x.id_of_good)
        else:
            print "This ID of good have already used. Try again!"

    def add_order(self, id_of_order, name, category, id_of_good):
        id_is_free = True
        for order in self.orders:
            if order.id_of_order == id_of_order:
                id_is_free = False
                break
        id_of_good_exist = False
        for good in self.goods:
            if good.id_of_good == id_of_good:
                id_of_good_exist = True
                break
        if id_is_free:
            if id_of_good_exist:
                self.orders.append(Order.Order(id_of_order, name, category, id_of_good))
                self.orders.sort(key=lambda x: x.id_of_order)
            else:
                print "This ID of good does not exist. Try again!"
        else:
            print "This ID of order have already used. Try again!"

    def print_all_goods(self):
        if len(self.goods) >= 1:
            print "||%10s||%15s||%12s||%12s||" % ("ID", "Name", "Price", "Attribute")
            print "-----------------------------------------------------------"
            for good in self.goods:
                print "||%10d||%15s||%12d||%12s||" % (int(good.id_of_good), good.name,
                                                      int(good.price), good.attribute)
        else:
            print "Table of goods is empty!"

    def print_all_orders(self):
        if len(self.orders) >= 1:
            print "||%10s||%15s||%12s||%12s||" % ("ID", "Name", "Category", "ID of good")
            print "-----------------------------------------------------------"
            for order in self.orders:
                print "||%10d||%15s||%12s||%12d||" % (int(order.id_of_order), order.name,
                                                      order.category, int(order.id_of_good))
        else:
            print "Table of orders is empty!"

    def print_all_orders_with_price_bigger_then(self, price_control):
        orders_cntrl = []
        for order in self.orders:
            for good in self.goods:
                if good.id_of_good == order.id_of_good:
                    if good.price >= price_control:
                        orders_cntrl.append(order)
        if len(orders_cntrl) >= 1:
            print "||%10s||%15s||%12s||%12s||" % ("ID", "Name", "Category", "ID of good")
            print "-----------------------------------------------------------"
            for order in orders_cntrl:
                print "||%10d||%15s||%12s||%12d||" % (int(order.id_of_order), order.name,
                                                      order.category, int(order.id_of_good))
        else:
            print "There are no such orders!"

    def print_good_with_id(self, id_of_good):
        for good in self.goods:
            if good.id_of_good == id_of_good:
                print "||%10s||%15s||%12s||%12s||" % ("ID", "Name", "Price", "Attribute")
                print "||%10d||%15s||%12d||%12s||" % (int(good.id_of_good), good.name,
                                                      int(good.price), good.attribute)
                return
        print("Good with this ID does`t exist. Try again!")

    def print_order_with_id(self, id_of_order):
        for order in self.orders:
            if order.id_of_order == id_of_order:
                print "||%10s||%15s||%12s||%12s||" % ("ID", "Name", "Category", "ID of good")
                print "||%10d||%15s||%12s||%12d||" % (int(order.id_of_order), order.name,
                                                      order.category, int(order.id_of_good))
                return
        print("Order with this ID does`t exist. Try again!")

    def change_good_with_id(self, id_of_good):
        for good in self.goods:
            if good.id_of_good == id_of_good:
                print "||%10s||%15s||%12s||%12s||" % ("ID", "Name", "Price", "Attribute")
                print "||%10d||%15s||%12d||%12s||" % (int(good.id_of_good), good.name,
                                                      int(good.price), good.attribute)
                try:
                    new_id_of_good = int(raw_input("New id: "))
                    new_name = str(raw_input("New name: "))
                    new_price = int(raw_input("New price: "))
                    new_attribute = str(raw_input("New attribute: "))
                except ValueError:
                    print "There are invalid values. Try again!"
                    return
                id_is_free = True
                for new_good in self.goods:
                    if new_good.id_of_good == new_id_of_good:
                        id_is_free = False
                        break
                if id_is_free:
                    for order in self.orders:
                        if order.id_of_good == id_of_good:
                            order.id_of_good = new_id_of_good
                    good.id_of_good = new_id_of_good
                    good.name = new_name
                    good.price = new_price
                    good.attribute = new_attribute
                    self.goods.sort(key=lambda x: x.id_of_good)
                    print "Done!"
                    return
                else:
                    print "This ID of good have already used. Try again!"
        print "Good with this ID does not exist. Try again!"

    def change_order_with_id(self, id_of_order):
        for order in self.orders:
            if order.id_of_order == id_of_order:
                print "||%10s||%15s||%12s||%12s||" % ("ID", "Name", "Category", "ID of good")
                print "||%10d||%15s||%12s||%12d||" % (int(order.id_of_order), order.name,
                                                      order.category, int(order.id_of_good))
                try:
                    new_id_of_order = int(raw_input("New id: "))
                    new_name = str(raw_input("New name: "))
                    new_category = str(raw_input("New category: "))
                    new_id_of_good = int(raw_input("New id of good: "))
                except ValueError:
                    print "There are invalid values. Try again!"
                    return
                id_exist = False
                for good in self.goods:
                    if good.id_of_good == new_id_of_good:
                        id_exist = True
                        break
                if id_exist:
                    order.id_of_order = new_id_of_order
                    order.name = new_name
                    order.category = new_category
                    order.id_of_good = new_id_of_good
                    self.orders.sort(key=lambda x: x.id_of_order)
                    print "Done!"
                    return
                else:
                    print "This ID of good does not exist. Try again!"
        print "Order with this ID does not exist. Try again!"

    def delete_good_with_id(self, id_of_good):
        for good in self.goods:
            if good.id_of_good == id_of_good:
                for order in self.orders:
                    if order.id_of_good == id_of_good:
                        print "We can not delete this good because of it using in the orders."
                        return
                self.goods.remove(good)
                print "Done!"
                return
        print "This ID of good does not exist. Try again!"

    def delete_order_with_id(self, id_of_order):
        for order in self.orders:
            if order.id_of_order == id_of_order:
                self.orders.remove(order)
                print "Done!"
                return
        print "This ID of order does not exist. Try again!"
