import sqlite3
con=sqlite3.connect("inventory.db")
c=con.cursor()

c.execute('''
    create table if not exists users(
    userid integer primary key autoincrement,
    username text unique not null,
    password text not null,
    role text not null
    )
''')

c.execute('''
    create table if not exists categories(
    categoryid integer primary key autoincrement,
    categoryname text unique not null
    )
''')

c.execute('''
    create table if not exists products(
    productid integer primary key autoincrement,
    productname text unique not null,
    categoryid integer not null,
    price real not null,
    quantity int not null,
    foreign key(categoryid) references categories(categoryid)
    )
''')

c.execute('''
    create table if not exists stock_transactions(
    transactionid integer primary key autoincrement,
    productid integer not null,
    transaction_type text not null,
    quantity int not null,
    transaction_date text not null,
    foreign key(productid) references products(productid)
    )
''')

con.commit()
con.close()


