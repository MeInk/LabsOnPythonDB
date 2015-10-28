from xml.dom import minidom
import MySQLdb as mdb
import sys


class DB(object):
    def __init__(self):
        self.connection = None

    def connect(self):
        if self.connection is not None:
            return
        try:
            self.connection = mdb.connect('127.0.0.1', 'root', '0000', 'mydb')

        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            self.connection = None

    def close(self):
        if self.connection is not None:
            self.connection.close()
        self.connection = None

    def get_sales_list(self):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute(
            "SELECT * FROM Sales_Fact, Customer_Dim, Product_Dim, Time_Dim WHERE Sales_Fact.ProductId=Product_Dim.ProductId AND Sales_Fact.CustomerId=Customer_Dim.CustomerId AND Sales_Fact.TimeId=Time_Dim.TimeId")
        self.close()
        return cur.fetchall()

    def save_sale(self, ProductName, CategoryName, ProductPrice, LineItemQuantity, LineItemDiscount, ContactName,
                  Address,
                  Phone, TheDate, Holiday, Weekend, Comment):
        self.connect()
        cur = self.connection.cursor()

        cur.execute("INSERT INTO Product_Dim (ProductName, CategoryName, ProductPrice) VALUES('%s', '%s', '%d')" %
                    (ProductName, CategoryName, ProductPrice,))
        cur.execute("SELECT * FROM Product_Dim ORDER BY ProductId DESC")
        ProductId = cur.fetchall()[0][0]
        print ProductId

        cur.execute("INSERT INTO Customer_Dim (ContactName, Address, Phone) VALUES('%s', '%s', '%d')" %
                    (ContactName, Address, Phone,))
        cur.execute("SELECT * FROM Customer_Dim ORDER BY CustomerId DESC")
        CustomerId = cur.fetchall()[0][0]
        print CustomerId

        cur.execute("INSERT INTO Time_Dim (TheDate, Holiday, Weekend) VALUES('%s', '%d', '%d')" %
                    (TheDate, Holiday, Weekend,))
        cur.execute("SELECT * FROM Time_Dim ORDER BY TimeId DESC")
        TimeId = cur.fetchall()[0][0]
        print TimeId

        cur.execute(
            "INSERT INTO Sales_Fact (ProductId, CustomerId, TimeId, LineItemQuantity, LineItemDiscount, Comment)"
            " VALUES('%d', '%d', '%d', '%d', '%d', '%s')" %
            (ProductId, CustomerId, TimeId, LineItemQuantity, LineItemDiscount, Comment,))
        cur.execute("SELECT * FROM Sales_Fact ORDER BY SaleId DESC")
        SaleId = cur.fetchall()[0][0]
        print SaleId
        cur.execute("commit")
        self.close()

    def remove_sale(self, id_of_sale):
        self.connect()

        cur = self.connection.cursor()

        cur.execute("SELECT * FROM Sales_Fact WHERE SaleId='%d'" % (id_of_sale,))
        tmp = cur.fetchall()
        ProductId = tmp[0][1]
        CustomerId = tmp[0][2]
        TimeId = tmp[0][3]

        cur.execute("DELETE FROM Sales_Fact WHERE SaleId='%d'" % (id_of_sale,))
        cur.execute("DELETE FROM Product_Dim WHERE ProductId='%d'" % (ProductId,))
        cur.execute("DELETE FROM Customer_Dim WHERE CustomerId='%d'" % (CustomerId,))
        cur.execute("DELETE FROM Time_Dim WHERE TimeId='%d'" % (TimeId,))
        cur.execute("commit")
        self.close()

    def change_sale(self, id_of_sale, ProductName, CategoryName, ProductPrice, LineItemQuantity, LineItemDiscount,
                    ContactName, Address,
                    Phone, TheDate, Holiday, Weekend, Comment):
        self.connect()

        cur = self.connection.cursor()

        cur.execute("SELECT ProductId, CustomerId, TimeId FROM Sales_Fact WHERE SaleId='%d'" % (id_of_sale,))
        tmp = cur.fetchone()
        print(tmp)
        ProductId = tmp[0]
        CustomerId = tmp[1]
        TimeId = tmp[2]
        print(ProductId, CustomerId, TimeId)

        cur.execute(
            "UPDATE Product_Dim SET ProductName='%s', CategoryName='%s', ProductPrice='%d' WHERE ProductId='%d'" %
            (ProductName, CategoryName, ProductPrice, ProductId,))
        cur.execute("UPDATE Customer_Dim SET ContactName='%s', Address='%s', Phone='%d' WHERE CustomerId='%d'" %
                    (ContactName, Address, Phone, CustomerId,))
        cur.execute("UPDATE Time_Dim SET TheDate='%s', Holiday='%d', Weekend='%d' WHERE TimeId='%d'" %
                    (TheDate, Holiday, Weekend, TimeId,))
        cur.execute(
            "UPDATE Sales_Fact SET LineItemQuantity='%d', LineItemDiscount='%d', Comment='%s' WHERE SaleId='%d'" %
            (LineItemQuantity, LineItemDiscount, Comment, id_of_sale,))

        cur.execute("commit")
        self.close()

    def get_sale(self, id_of_sale):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute(
            "SELECT * FROM Sales_Fact, Customer_Dim, Product_Dim, Time_Dim WHERE Sales_Fact.ProductId=Product_Dim.ProductId "
            "AND Sales_Fact.CustomerId=Customer_Dim.CustomerId AND Sales_Fact.TimeId=Time_Dim.TimeId "
            "AND Sales_Fact.SaleId='%d'" % (id_of_sale,))
        self.close()
        return cur.fetchone()

    def initialization(self):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute("DELETE FROM Sales_Fact ")
        cur.execute("ALTER TABLE Sales_Fact AUTO_INCREMENT = 1")
        cur.execute("commit")

        cur.execute("DELETE FROM Customer_Dim")
        cur.execute("ALTER TABLE Customer_Dim AUTO_INCREMENT = 1")
        cur.execute("commit")

        cur.execute("DELETE FROM Product_Dim")
        cur.execute("ALTER TABLE Product_Dim AUTO_INCREMENT = 1")
        cur.execute("commit")

        cur.execute("DELETE FROM Time_Dim")
        cur.execute("ALTER TABLE Time_Dim AUTO_INCREMENT = 1")
        cur.execute("commit")

        xmldoc = minidom.parse('tables.xml')

        customer_list = xmldoc.getElementsByTagName('customer')
        for customer in customer_list:
            contactName = str(customer.getElementsByTagName('ContactName')[0].firstChild.data)
            address = str(customer.getElementsByTagName('Address')[0].firstChild.data)
            phone = int(customer.getElementsByTagName('Phone')[0].firstChild.data)
            cur.execute("INSERT INTO Customer_Dim (ContactName, Address, Phone) VALUES('%s', '%s', '%d')" %
                        (contactName, address, phone,))
            cur.execute("commit")
            print(contactName, address, phone)

        customer_list = xmldoc.getElementsByTagName('product')
        for customer in customer_list:
            productName = str(customer.getElementsByTagName('ProductName')[0].firstChild.data)
            categoryName = str(customer.getElementsByTagName('CategoryName')[0].firstChild.data)
            productPrice = int(customer.getElementsByTagName('ProductPrice')[0].firstChild.data)
            cur.execute("INSERT INTO Product_Dim (ProductName, CategoryName, ProductPrice) VALUES('%s', '%s', '%d')" %
                        (productName, categoryName, productPrice,))
            cur.execute("commit")
            print(productName, categoryName, productPrice)

        customer_list = xmldoc.getElementsByTagName('time')
        for customer in customer_list:
            date = str(customer.getElementsByTagName('TheDate')[0].firstChild.data)
            print date
            holiday = int(customer.getElementsByTagName('Holiday')[0].firstChild.data)
            weekend = int(customer.getElementsByTagName('Weekend')[0].firstChild.data)
            cur.execute("INSERT INTO Time_Dim (TheDate, Holiday, Weekend) VALUES('%s', '%d', '%d')" %
                        (date, holiday, weekend,))
            cur.execute("commit")
            print(date, holiday, weekend)

        sales_list = xmldoc.getElementsByTagName('sale')
        for sale in sales_list:
            ProductId = int(sale.getElementsByTagName('ProductId')[0].firstChild.data)
            CustomerId = int(sale.getElementsByTagName('CustomerId')[0].firstChild.data)
            TimeId = int(sale.getElementsByTagName('TimeId')[0].firstChild.data)
            LineItemQuantity = int(sale.getElementsByTagName('LineItemQuantity')[0].firstChild.data)
            LineItemDiscount = int(sale.getElementsByTagName('LineItemDiscount')[0].firstChild.data)
            Comment = str(sale.getElementsByTagName('Comment')[0].firstChild.data)
            cur.execute(
                "INSERT INTO Sales_Fact (ProductId, CustomerId, TimeId, LineItemQuantity, LineItemDiscount, Comment) VALUES('%d', '%d', '%d', '%d', '%d', '%s')" %
                (ProductId, CustomerId, TimeId, LineItemQuantity, LineItemDiscount, Comment,))
            cur.execute("commit")
        self.close()

    def search_integer(self, price_min, price_max):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Sales_Fact, Product_Dim, Time_Dim, Customer_Dim WHERE Sales_Fact.ProductId = Product_Dim.ProductId AND Sales_Fact.TimeId = "
                    "Time_Dim.TimeId AND Sales_Fact.CustomerId = Customer_Dim.CustomerId AND Product_Dim.ProductPrice > '%d' AND  Product_Dim.ProductPrice < '%d'" %
                    (price_min, price_max))
        self.close()
        return cur.fetchall()

    def search_boolean(self, holiday, weekend):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Sales_Fact, Product_Dim, Time_Dim, Customer_Dim WHERE Sales_Fact.ProductId = Product_Dim.ProductId AND Sales_Fact.TimeId = "
                    "Time_Dim.TimeId AND Sales_Fact.CustomerId = Customer_Dim.CustomerId AND Time_Dim.Weekend = '%d' AND  Time_Dim.Holiday = '%d'" %
                    (weekend, holiday,))
        self.close()
        return cur.fetchall()

    def search_text(self, phrase):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)

        cur.execute("SELECT * FROM Sales_Fact, Product_Dim, Customer_Dim, Time_Dim Where (MATCH (Sales_Fact.Comment) "
                    "AGAINST ('%s' IN BOOLEAN MODE) or MATCH (Customer_Dim.ContactName, Customer_Dim.Address) AGAINST "
                    "('%s' IN BOOLEAN MODE) or MATCH (Product_Dim.ProductName, Product_Dim.CategoryName) AGAINST ('%s' IN BOOLEAN MODE))"
                    " And Sales_Fact.CustomerId = Customer_Dim.CustomerId and Sales_Fact.ProductId = Product_Dim.ProductId and Sales_Fact.TimeId = Time_Dim.TimeId" %
                    (phrase, phrase, phrase,))
        self.close()
        return cur.fetchall()
