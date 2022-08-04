from audioop import add
from cgitb import reset
from re import template
import sqlite3
from turtle import color, st
import datetime
from datetime import timedelta, datetime
from warnings import catch_warnings
from termcolor import colored
import os

con = sqlite3.connect("Locum.db")
cur = con.cursor()

def new_invoice():
    print("THIS IS YOUR CURRENT INVOICES TEMPLATES")
    print("------------------------------------------")
    stmt = "SELECT templates.* , contactname from templates inner join contacts on templates.contactid = contacts.id;"
    e = cur.execute(stmt)
    template_id_list = []
    for each in e:
        print('ID:', colored(each[0], 'red'), " > " , each[10], " Rate: $ " , each[7], " - From:", each[1], "to", each[2])
        template_id_list.append(int(each[0]))
    print("------------------------------------------")
    template_id = input("Template ID: ")
    if (template_id=="q"):
        return

    if (int(template_id) not in template_id_list):
        if (input("The ID you entered is not in the list, do you want to create one first? ")=='y'):
            new_template()
            return
        else:
            menu()
    stmt = "SELECT * from templates where templateid = " + template_id + ";"
    e = cur.execute(stmt)
    for each in e:
        contact_id = str(each[6])

    
    date_worked = input("Date worked: dd/mm/yy: ")
    if (date_worked=="q"):
        return

    stmt = "INSERT INTO invoices (templateid, contactID, dateworked) VALUES (" + template_id + ", " + contact_id + ", '" + date_worked + "');"
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

def arrear():
    contact_id = input("Enter pharmacy id: ")
    total_paid = 0
    total_invoiced = 0

    stmt = "SELECT sum(payment.paymentamount) from payment where contactid = " + contact_id + ";"
    e = cur.execute(stmt)
    for each in e:
        total_paid = each[0]
    if total_paid is None:
        total_paid = 0.0
    print("------------------------------------------------------------")
    print("TOTAL PAID: $ " + colored(str(total_paid), 'yellow'))

    stmt = "SELECT sum(templates.total) from templates inner join invoices on templates.templateid = invoices.templateid where invoices.contactid = " + contact_id + ";"
    e = cur.execute(stmt)
    for each in e:
        total_invoiced = each[0]
    if (total_invoiced is None):
        total_invoiced = 0.0
        print(colored("You have never invoiced this pharmacy before.", 'red'))
    remain = total_invoiced - total_paid
    print("TOTAL INVOICED: $", colored(str(total_invoiced), 'yellow'))
    print("------------------------------------------------------------")
    print("REMAIN TO PAY: $", colored(str(remain), 'red'))
    print("------------------------------------------------------------")
def payment():
    contact_id = input("Enter pharmacy id: ")
    stmt = "SELECT * FROM contacts where id = " + contact_id + ";"
    e = cur.execute(stmt)
    print("Pharmacy entered is: ")
    for each in e:
        print(colored(each,'green'))
    
    if (input("Is this correct. Enter YES if correct ... ") == "YES"):

        payment_amount = input("Enter payment received $ ")
        try: payment_amount = float(payment_amount)
        except: return

        if (payment_amount==0.0):
            return
        else:
            payment_amount = str(payment_amount)

        print("You entered: $", colored(payment_amount, 'red'))

        if (input("Commit this payment? Enter YES/NO: ")== "YES"):
            stmt = "INSERT INTO payment(contactid, paymentamount) VALUES (" + contact_id + ", " + payment_amount + ");"
            cur.execute(stmt)
            con.commit()
            print(colored("SUCCESSFULLY RECORD PAYMENT.", 'CYAN'))
        else:
            return
    else:
        return


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
        print(colored(each, 'green'))

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

def show_invoices():
    result = cur.execute("SELECT invoiceid, dateworked, contactname, fromtime, totime, rate, hours, total FROM invoices inner join templates inner join contacts on  invoices.templateid = templates.templateid and templates.contactid = contacts.id ORDER BY invoiceID DESC;")
    for each in result:
        print(colored(each, 'cyan'))

def menu():
    input("PRESS ENTER TO CONTINUE...")
    print("-------")
    while (True):
        ask = input("1. New invoice \n2. Delete invoice \n3. New template \n4. New contact \n5. Show contact list \n6. Show current templates \nEnter your choice: ")
        if (ask == 'new invoice' or ask == '1'):
            print("------------------------------------------------------------")
            print('To create a new invoice, first select a template.')
            print('Then enter the date for this invoice.')
            print("------------------------------------------------------------")
            new_invoice()
            menu()
        elif(ask == 'delete invoice' or ask == '2'):
            delete_invoice()
            menu()
        elif (ask == 'new template' or ask == '3'):
            new_template()
            menu()
        elif (ask == 'new contact' or ask == '4'):
            new_contact()
            menu()
        elif (ask == '5' or ask == 'show contacts'):
            show_contacts()
            menu()
        elif(ask == '6' or ask == 'show templates'):
            show_templates()
            menu()
        elif (ask == '7' or ask == 'show invoices'):
            show_invoices()
            menu()
        elif (ask == 'sql'):
            sql()
        elif (ask == '10'):
            arrear()
            menu()
        elif (ask == "payment"):
            payment()
            menu()
        elif (ask == 'clear'):
            os.system('clear')
            os.system('python locum.py')
        elif (ask == 'q'):
            return
        else:
            return




menu()