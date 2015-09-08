import DBController


db_obj = DBController.DBController()
menu = {}
menu['1'] = "Add good."
menu['2'] = "Add order."
menu['3'] = "Change good by id."
menu['4'] = "Change order by id."
menu['5'] = "Show good by id."
menu['6'] = "Show order by id."
menu['7'] = "Show all goods."
menu['8'] = "Show all orders."
menu['9'] = "Find orders with price."
menu['10'] = "Delete good by id."
menu['11'] = "Delete order by id."
menu['12'] = "Exit."
while True:
    options = menu.keys()
    options.sort()
    for entry in options:
        print entry, menu[entry]

    selection = raw_input("Please Select:")
    if selection == '1':
        db_obj.add_good()
    elif selection == '2':
        db_obj.add_order()
    elif selection == '3':
        db_obj.change_good_by_id()
    elif selection == '4':
        db_obj.change_order_by_id()
    elif selection == '5':
        db_obj.show_good_by_id()
    elif selection == '6':
        db_obj.show_order_by_id()
    elif selection == '7':
        db_obj.show_all_goods()
    elif selection == '8':
        db_obj.show_all_orders()
    elif selection == '9':
        db_obj.find_orders_with_price()
    elif selection == '10':
        db_obj.delete_good_by_id()
    elif selection == '11':
        db_obj.delete_order_by_id()
    elif selection == '12':
        db_obj.exit_from_program()
        break
    else:
        print "Unknown Option Selected!"
