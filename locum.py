from audioop import add
from cgitb import reset
from re import template
import sqlite3
from turtle import st
import datetime
from datetime import timedelta, datetime


con = sqlite3.connect("Locum.db")
cur = con.cursor()

def new_invoice():
    print("THIS IS YOUR CURRENT INVOICES TEMPLATES")
    print("------------------------------------------")
    stmt = "SELECT templates.* , contactname from templates inner join contacts on templates.contactid = contacts.id;"
    e = cur.execute(stmt)
    for each in e:
        print("ID", each[0], " > " , each[10], " Rate: $ " , each[7], " - From:", each[1], "to", each[2])
    print("------------------------------------------")
    template_id = input("Template ID: ")
    date_worked = input("Date worked: dd/mm/yy: ")
    stmt = "INSERT INTO invoices (templateid, dateworked) VALUES (" + template_id + ", '" + date_worked + "');"
    cur.execute(stmt)
    con.commit()

    stmt = "SELECT * FROM INVOICES;"
    e = cur.execute(stmt)
    for each in e:
        print(each)

def delete_invoice():
    stmt = "SELECT invoiceID, Contactname, dateworked, total from invoices inner join templates inner join contacts on invoices.templateid = templates.templateid and templates.contactid = contacts.id;"

    invoice_number = input("Enter invoice number: ")
    stmt = "delete from invoices where invoiceid = " + invoice_number + ";"
    cur.execute(stmt)
    con.commit()


def invoice_sum():
    stmt = "SELECT sum(total) from templates inner join invoices on templates.templateid = invoices.templateid;"
    result = cur.execute(stmt)
    for each in result:
        print(each)


def new_template():
    for i in cur.execute("SELECT * FROM TEMPLATES;"):
        print(i)

    from_time = input("From time (format HH:MM 24 HR PERIOD): ")
    from_time_ = datetime.strptime(from_time, "%H:%M")
 
    to_time = input("To time: ")
    to_time_ = datetime.strptime(to_time, "%H:%M")

    time_diff = to_time_ - from_time_
    

    time_break = input("Break (minutes): ")
    time_diff_ = time_diff.total_seconds()/(60*60) - float(time_break)/60
    super_rate = input("Super % ")
    gst = input("GST % ")
    for i in cur.execute("SELECT * FROM contacts"):
        print(i)

    pharmacy = input("Pharmacy ID: ")
    rate = input("Rate per hour: $ ")
    
    hours = str(time_diff_)

    total = float(hours) * float(rate)

    total = total * (1+float(super_rate)/100)
    string_total = str(total)
    print(total)
    q = "('" + from_time + "','" + to_time + "'," + time_break + "," + super_rate + ","+ gst + ","+ pharmacy + "," + rate + "," + hours + "," + str(total) + "); "
    print(q)
    stmt = "INSERT INTO templates (fromTime, toTime, break, super, gst, contactid, rate, hours, total) VALUES " + q 
    cur.execute(stmt)
    con.commit()


def new_contact():
    pharmacy = input("Pharmacy name: ")
    address = input("Pharmacy address: ")
    ABN = input("Pharmacy ABN: " )
    q = "('" + pharmacy + "', '" + address + "', '" + ABN + "');"
    stmt = "INSERT INTO CONTACTS (contactname, abn, address) VALUES " + q
    cur.execute(stmt)
    con.commit()
    stmt = "SELECT * FROM CONTACTS WHERE ID = (SELECT MAX(ID) FROM CONTACTS);"
    e = cur.execute(stmt)
    print("Success. Inserted new Contact as")
    for each in e:
        print(each)

def show_contacts():
    stmt = "SELECT * FROM Contacts;"
    e = cur.execute(stmt)
    for each in e:
        print(each)

def show_templates():
    stmt = "SELECT templates.* , contactname from templates inner join contacts on templates.contactid = contacts.id;"
    e = cur.execute(stmt)
    for each in e:
        print("ID", each[0], " > " , each[10], " Rate: $ " , each[7], " - From:", each[1], "to", each[2])

def sql():
    q = input("Enter your SQL Statement: ")
    print('"'+q+';"')
    e = cur.execute(q)
    for each in e:
        print(each)
    
    a = input("SQL Statement executed successfully.\nDo you want to commit? ")
    if a == 'yes':
        con.commit()
    else:
        return


def menu():
    while (True):
        ask = input("1. New invoice \n2. Delete invoice \nEnter your choice: ")
        if ask == 'new invoice' or ask == '1':
            new_invoice()
            menu()
        elif ask == 'delete invoice' or ask == '2':
            delete_invoice()
            menu()
        elif ask == 'new template' or ask == '3':
            new_template()
            menu()
        elif ask == 'new contact' or ask == '4':
            new_contact()
            menu()
        elif ask == '5' or ask == 'show contacts':
            show_contacts()
            menu()
        elif ask == '6' or ask == 'show templates':
            show_templates()
            menu()
        elif ask == 'sql':
            sql()
        elif ask == 'q':
            break
        else:
            break


    result = cur.execute("SELECT invoiceid, dateworked, contactname, fromtime, totime, rate, hours, total FROM invoices inner join templates inner join contacts on  invoices.templateid = templates.templateid and templates.contactid = contacts.id ORDER BY invoiceID DESC;")
    for each in result:
        print(each)

menu()