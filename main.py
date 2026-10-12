import sqlite3

con = sqlite3.connect("inventory.db")
c = con.cursor()


def signup():
    print("\n========== SIGN UP ==========")

    username = input("Enter username: ")
    password = input("Enter password: ")

    print("\n1. User")
    print("2. Owner")

    choice = input("Choose role: ")

    if choice == "1":
        role = "user"

    elif choice == "2":
        code = input("Enter owner authorization code: ")

        if code != "OWNER123":
            print("\nInvalid authorization code.")
            return

        role = "owner"

    else:
        print("Invalid role.")
        return

    try:
        c.execute('''
            INSERT INTO users(username, password, role)
            VALUES (?, ?, ?)
        ''', (username, password, role))

        con.commit()

        print("\nAccount created successfully!")

    except sqlite3.IntegrityError:
        print("\nUsername already exists.")


def signin():

    print("\n========== SIGN IN ==========")

    username = input("Enter username: ")
    password = input("Enter password: ")

    c.execute('''
        SELECT userid, username, role
        FROM users
        WHERE username = ? AND password = ?
    ''', (username, password))

    user = c.fetchone()

    if user:

        print("\nLogin successful!")
        print("Welcome,", user[1])

        if user[2] == "user":
            user_dashboard()

        elif user[2] == "owner":
            owner_dashboard()

    else:
        print("\nInvalid username or password.")

def view_products():
    print("\n========================================")
    print("             ALL PRODUCTS")
    print("========================================")

    c.execute('''
        SELECT products.productid,
               products.productname,
               categories.categoryname,
               products.price,
               products.quantity
        FROM products
        JOIN categories
        ON products.categoryid = categories.categoryid
    ''')

    products = c.fetchall()

    if products:
        print("\nID   Product              Category              Price      Stock")
        print("-----------------------------------------------------------------")

        for product in products:
            print(f"{product[0]:<5}{product[1]:<22}{product[2]:<22}{product[3]:<11}{product[4]:<5}")
    else:
        print("\nNo products available.")


def check_stock():

    print("\n========== CHECK STOCK ==========")

    productname = input("Enter product name: ")

    c.execute('''
        SELECT productname, quantity
        FROM products
        WHERE productname = ?
    ''', (productname,))

    product = c.fetchone()

    if product:
        print("\nProduct:", product[0])
        print("Available Stock:", product[1])

    else:
        print("\nProduct not found.")


def search_by_name():
    print("\n========== SEARCH BY PRODUCT NAME ==========")

    productname = input("Enter product name: ")

    c.execute('''
        SELECT products.productid,
               products.productname,
               categories.categoryname,
               products.price,
               products.quantity
        FROM products
        JOIN categories
        ON products.categoryid = categories.categoryid
        WHERE products.productname LIKE ?
    ''', ('%' + productname + '%',))

    products = c.fetchall()

    if products:
        print("\nID   Product        Category        Price    Stock")
        print("--------------------------------------------------")

        for product in products:
            print(f"{product[0]:<5}{product[1]:<22}{product[2]:<22}{product[3]:<11}{product[4]:<5}")

    else:
        print("\nProduct not found.")



def search_by_category():
    print("\n========== SEARCH BY CATEGORY ==========")

    categoryname = input("Enter category name: ")

    c.execute('''
        SELECT products.productid,
               products.productname,
               categories.categoryname,
               products.price,
               products.quantity
        FROM products
        JOIN categories
        ON products.categoryid = categories.categoryid
        WHERE categories.categoryname LIKE ?
    ''', ('%' + categoryname + '%',))

    products = c.fetchall()

    if products:
        print("\nID   Product        Category        Price    Stock")
        print("--------------------------------------------------")

        for product in products:
            print(product[0], "  ", product[1], "  ", product[2], "  ", product[3], "  ", product[4])

    else:
        print("\nNo products found in this category.")




def search_product():
    while True:
        print("\n========== SEARCH PRODUCT ==========")
        print("\n1. Search by Product Name")
        print("2. Search by Category")
        print("3. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            search_by_name()

        elif choice == "2":
            search_by_category()

        elif choice == "3":
            break

        else:
            print("\nInvalid choice.")





def user_dashboard():

    while True:

        print("\n========================================")
        print("             USER DASHBOARD")
        print("========================================")

        print("\n1. View Products")
        print("2. Check Stock")
        print("3. Search Product")
        print("4. Logout")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_products()

        elif choice == "2":
            check_stock()

        elif choice == "3":
            search_product()

        elif choice == "4":
            print("\nLogged out successfully.")
            break

        else:
            print("\nInvalid choice.")






def add_category():

    print("\n========== ADD CATEGORY ==========")

    categoryname = input("Enter category name: ")

    try:

        c.execute('''
            INSERT INTO categories(categoryname)
            VALUES (?)
        ''', (categoryname,))

        con.commit()

        print("\nCategory added successfully!")

    except sqlite3.IntegrityError:

        print("\nCategory already exists.")

def view_categories():

    print("\n========== CATEGORIES ==========")

    c.execute('''
        SELECT categoryid, categoryname
        FROM categories
    ''')

    categories = c.fetchall()

    if categories:

        print("\nID   Category")
        print("------------------------")

        for category in categories:
            print(f"{category[0]:<5}{category[1]:<20}")
    else:
        print("\nNo categories available.")


def update_category():
    print("\n========== UPDATE CATEGORY ==========")

    categoryid = input("Enter category ID: ")
    newname = input("Enter new category name: ")

    try:
        c.execute('''
            UPDATE categories
            SET categoryname = ?
            WHERE categoryid = ?
        ''', (newname, categoryid))

        con.commit()

        if c.rowcount > 0:
            print("\nCategory updated successfully!")
        else:
            print("\nCategory not found.")

    except sqlite3.IntegrityError:
        print("\nCategory name already exists.")


def delete_category():
    print("\n========== DELETE CATEGORY ==========")

    categoryid = input("Enter category ID: ")

    try:
        c.execute('''
            DELETE FROM categories
            WHERE categoryid = ?
        ''', (categoryid,))

        con.commit()

        if c.rowcount > 0:
            print("\nCategory deleted successfully!")
        else:
            print("\nCategory not found.")

    except sqlite3.IntegrityError:
        print("\nCannot delete this category because products are using it.")

        

def category_management():

    while True:

        print("\n========================================")
        print("          CATEGORY MANAGEMENT")
        print("========================================")

        print("\n1. Add Category")
        print("2. View Categories")
        print("3. Update Category")
        print("4. Delete Category")
        print("5. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_category()

        elif choice == "2":
            view_categories()

        elif choice == "3":
            update_category()

        elif choice == "4":
            delete_category()

        elif choice == "5":
            break

        else:
            print("\nInvalid choice.")

def add_product():

    print("\n========== ADD PRODUCT ==========")

    productname = input("Enter product name: ")
    categoryid = input("Enter category ID: ")
    price = input("Enter price: ")
    quantity = input("Enter quantity: ")

    try:

        c.execute('''
            INSERT INTO products(productname, categoryid, price, quantity)
            VALUES (?, ?, ?, ?)
        ''', (productname, categoryid, price, quantity))

        con.commit()

        print("\nProduct added successfully!")

    except sqlite3.IntegrityError:

        print("\nProduct could not be added.")


def view_products():

    print("\n========================================")
    print("             ALL PRODUCTS")
    print("========================================")

    c.execute('''
        SELECT products.productid,
               products.productname,
               categories.categoryname,
               products.price,
               products.quantity
        FROM products
        JOIN categories
        ON products.categoryid = categories.categoryid
    ''')

    products = c.fetchall()

    if products:

        print("\nID   Product              Category              Price      Stock")
        print("-----------------------------------------------------------------")

    for product in products:
        print(f"{product[0]:<5}{product[1]:<22}{product[2]:<22}{product[3]:<11}{product[4]:<5}")

    else:
        print("\nNo products available.")


def update_product():
    print("\n========== UPDATE PRODUCT ==========")

    productid = input("Enter product ID: ")

    productname = input("Enter new product name: ")
    categoryid = input("Enter new category ID: ")
    price = input("Enter new price: ")
    quantity = input("Enter new quantity: ")

    try:
        c.execute('''
            UPDATE products
            SET productname = ?,
                categoryid = ?,
                price = ?,
                quantity = ?
            WHERE productid = ?
        ''', (productname, categoryid, price, quantity, productid))

        con.commit()

        if c.rowcount > 0:
            print("\nProduct updated successfully!")
        else:
            print("\nProduct not found.")

    except sqlite3.IntegrityError:
        print("\nProduct could not be updated.")


def delete_product():
    print("\n========== DELETE PRODUCT ==========")

    productid = input("Enter product ID: ")

    try:
        c.execute('''
            DELETE FROM products
            WHERE productid = ?
        ''', (productid,))

        con.commit()

        if c.rowcount > 0:
            print("\nProduct deleted successfully!")
        else:
            print("\nProduct not found.")

    except sqlite3.IntegrityError:
        print("\nCannot delete this product.")



     


def product_management():

    while True:

        print("\n========================================")
        print("          PRODUCT MANAGEMENT")
        print("========================================")

        print("\n1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Search Product")
        print("6. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_product()

        elif choice == "2":
            view_products()

        elif choice == "3":
            update_product()

        elif choice == "4":
            delete_product()

        elif choice == "5":
            search_product()

        elif choice == "6":
            break

        else:
            print("\nInvalid choice.")


def add_stock():
    print("\n========== ADD STOCK ==========")

    productid = input("Enter product ID: ")
    quantity = input("Enter quantity to add: ")

    try:
        c.execute('''
            UPDATE products
            SET quantity = quantity + ?
            WHERE productid = ?
        ''', (quantity, productid))

        if c.rowcount > 0:

            c.execute('''
                INSERT INTO stock_transactions
                (productid, transaction_type, quantity, transaction_date)
                VALUES (?, ?, ?, date('now'))
            ''', (productid, "IN", quantity))

            con.commit()

            print("\nStock added successfully!")

        else:
            print("\nProduct not found.")

    except sqlite3.Error:
        print("\nError while adding stock.")
        

def remove_stock():
    print("\n========== REMOVE STOCK ==========")

    productid = input("Enter product ID: ")
    quantity = input("Enter quantity to remove: ")

    try:
        c.execute('''
            SELECT quantity
            FROM products
            WHERE productid = ?
        ''', (productid,))

        product = c.fetchone()

        if product:
            current_stock = product[0]

            if int(quantity) <= current_stock:

                c.execute('''
                    UPDATE products
                    SET quantity = quantity - ?
                    WHERE productid = ?
                ''', (quantity, productid))

                c.execute('''
                    INSERT INTO stock_transactions
                    (productid, transaction_type, quantity, transaction_date)
                    VALUES (?, ?, ?, date('now'))
                ''', (productid, "OUT", quantity))

                con.commit()

                print("\nStock removed successfully!")
                print("Remaining Stock:", current_stock - int(quantity))

            else:
                print("\nNot enough stock available.")

        else:
            print("\nProduct not found.")

    except ValueError:
        print("\nPlease enter a valid quantity.")

    except sqlite3.Error:
        print("\nError while removing stock.")


def inventory_overview():
    print("\n========== INVENTORY OVERVIEW ==========")

    c.execute('''
        SELECT COUNT(*)
        FROM products
    ''')
    total_products = c.fetchone()[0]

    c.execute('''
        SELECT COUNT(*)
        FROM categories
    ''')
    total_categories = c.fetchone()[0]

    c.execute('''
        SELECT SUM(quantity)
        FROM products
    ''')
    total_stock = c.fetchone()[0]

    c.execute('''
        SELECT SUM(price * quantity)
        FROM products
    ''')
    total_value = c.fetchone()[0]

    print("\nTotal Products       :", total_products)
    print("Total Categories     :", total_categories)
    print("Total Stock          :", total_stock)
    print("Total Inventory Value: ₹", total_value)



def low_stock_alert():
    print("\n========== LOW STOCK ALERT ==========")

    c.execute('''
        SELECT products.productid,
               products.productname,
               categories.categoryname,
               products.quantity
        FROM products
        JOIN categories
        ON products.categoryid = categories.categoryid
        WHERE products.quantity < 5
    ''')

    products = c.fetchall()

    if products:
        print("\nID   Product              Category              Stock")
        print("------------------------------------------------------")

        for product in products:
            print(f"{product[0]:<5}{product[1]:<22}{product[2]:<22}{product[3]:<5}")
    else:
        print("\nNo low stock products.")




def owner_dashboard():

    while True:

        print("\n========================================")
        print("            OWNER DASHBOARD")
        print("========================================")

        print("\n1. Product Management")
        print("2. Category Management")
        print("3. Add Stock")
        print("4. Remove Stock")
        print("5. Inventory Overview")
        print("6. Low Stock Alert")
        print("7. Logout")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            product_management()

        elif choice == "2":
            category_management()

        elif choice == "3":
            add_stock()

        elif choice == "4":
            remove_stock()

        elif choice == "5":
            inventory_overview()

        elif choice == "6":
            low_stock_alert()

        elif choice == "7":
            print("\nLogged out successfully.")
            break

        else:
            print("\nInvalid choice.")









def main():

    while True:

        print("\n========================================")
        print("       Inventory Management System")
        print("========================================")

        print("\n1. Sign Up")
        print("2. Sign In")
        print("3. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            signup()

        elif choice == "2":
            signin()

        elif choice == "3":
            print("\nThank you")
            break

        else:
            print("\nInvalid choice.")


main()