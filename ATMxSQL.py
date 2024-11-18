import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", password="")
print(mydb)
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS ATM")
mycursor.execute("USE ATM")
db = """
CREATE TABLE IF NOT EXISTS ATM_DATABASE (
    ACCOUNT_NO INT(8) PRIMARY KEY, 
    ATM_PIN INT(6), 
    ACCOUNT_HOLDER VARCHAR(100), 
    BALANCE INT DEFAULT 0, 
    WITHDRAWAL INT DEFAULT 0,
    SAVINGS INT DEFAULT 0
)
"""
mycursor.execute(db)

conn = mysql.connector.connect(host="localhost", user="root", password="", database="ATM")
con = conn.cursor()


print("Welcome to Online Banking\n"
      "*************************\n"
      "1. LOGIN\n"
      "2. CREATE ACCOUNT\n"
      "3. EXIT\n"
      "*************************")
choice = int(input("What would you like to do?: "))


if choice == 2:
    while True:
        an = int(input("Enter an 8-digit account number: "))
        cd = "SELECT * FROM ATM_DATABASE WHERE ACCOUNT_NO = %s"
        con.execute(cd, (an,))
        d = con.fetchall()

        if len(d) > 0:
            print("***************************************")
            print("   Account number already exists!")
            c = input("Do you want to continue (y/n): ")
            print("***************************************")
            if c.lower() == "y":
                continue
            else:
                print("***************************************")
                print("   Thank you for your transaction.")
                print("***************************************")
                break
        else:
            name = input("Enter your full name (SURNAME, FIRST NAME, MIDDLE NAME): ")
            passw = int(input("Enter your PIN (6 digits): "))
            ab = "INSERT INTO ATM_DATABASE (ACCOUNT_NO, ATM_PIN, ACCOUNT_HOLDER) VALUES (%s, %s, %s)"
            con.execute(ab, (an, passw, name))
            conn.commit()

            print("Account created successfully!")
            dep = int(input("Enter the amount you want to deposit: "))
            sav = "UPDATE ATM_DATABASE SET SAVINGS = %s, BALANCE = %s WHERE ACCOUNT_NO = %s"
            con.execute(sav, (dep, dep, an))
            conn.commit()

            print("Deposit successful. Thank you!")
            break


elif choice == 1:
    logged_in = False
    current_user = {}

    while not logged_in:
        acc = int(input("Enter your account number: "))
        cd = "SELECT * FROM ATM_DATABASE WHERE ACCOUNT_NO = %s"
        con.execute(cd, (acc,))
        d = con.fetchall()

        if len(d) > 0:
            pas = int(input("Enter your PIN: "))
            p = "SELECT ATM_PIN FROM ATM_DATABASE WHERE ACCOUNT_NO = %s"
            con.execute(p, (acc,))
            a = con.fetchone()

            if pas == a[0]:
                logged_in = True
                current_user = {
                    "ACCOUNT_NO": d[0][0],
                    "ATM_PIN": d[0][1],
                    "ACCOUNT_HOLDER": d[0][2],
                }
                print(f"Welcome {current_user['ACCOUNT_HOLDER']}")
            else:
                print("Incorrect PIN.")
        else:
            print("Account does not exist.")

    while logged_in:
        print("*************************\n"
              "1. Check Balance\n"
              "2. Withdraw\n"
              "3. Deposit\n"
              "4. Transfer money\n"
              "5. Exit\n"
              "*************************")
        c1 = int(input("Choose an option: "))

        if c1 == 1:
            b = "SELECT BALANCE FROM ATM_DATABASE WHERE ACCOUNT_NO = %s"
            con.execute(b, (current_user["ACCOUNT_NO"],))
            k = con.fetchone()
            print(f"Your balance is: {k[0]}")
            t = input("Would you like to do another transaction? y/n: ")
            if t.casefold() == "y":
                continue
            else:
                print("Thank you for your transaction.")
                print("Have a nice day!")
                break

        elif c1 == 2:
            amt = int(input("Enter withdrawal amount: "))
            ba = "SELECT BALANCE FROM ATM_DATABASE WHERE ACCOUNT_NO = %s"
            con.execute(ba, (current_user["ACCOUNT_NO"],))
            bal = con.fetchone()[0]

            if amt > bal:
                print("Insufficient balance.")
            else:
                sr = "UPDATE ATM_DATABASE SET BALANCE = BALANCE - %s, SAVINGS = SAVINGS - %s, WITHDRAWAL = WITHDRAWAL + %s WHERE ACCOUNT_NO = %s"
                con.execute(sr, (amt, amt, amt, current_user["ACCOUNT_NO"]))
                conn.commit()
                print("Withdrawal successful. Please collect your money.")
                t = input("Would you like to do another transaction? y/n: ")
                if t.casefold() == "y":
                    continue
                else:
                    print("Thank you for your transaction.")
                    print("Have a nice day!")
                    break

        elif c1 == 3: 
            amt = int(input("Enter deposit amount: "))
            sav = "UPDATE ATM_DATABASE SET BALANCE = BALANCE + %s, SAVINGS = SAVINGS + %s WHERE ACCOUNT_NO = %s"
            con.execute(sav, (amt, amt, current_user["ACCOUNT_NO"]))
            conn.commit()
            print("Deposit successful.")
            t = input("Would you like to do another transaction? y/n: ")
            if t.casefold() == "y":
                continue
            else:
                print("Thank you for your transaction.")
                print("Have a nice day!")
                break



        elif c1 == 4: 
            trf = int(input("Enter the account number to transfer money to: "))
            
            cb = "SELECT * FROM ATM_DATABASE WHERE ACCOUNT_NO = %s"
            con.execute(cb, (trf,))
            target_account = con.fetchone()
            if target_account:
                print(f"Account number {trf} exists.")
                m = int(input("Enter the amount to be transferred: "))
                
                bal_query = "SELECT BALANCE FROM ATM_DATABASE WHERE ACCOUNT_NO = %s"
                con.execute(bal_query, (current_user["ACCOUNT_NO"],))
                result = con.fetchone()
                current_balance = result[0] if result and result[0] is not None else 0 
                if m > current_balance:
                    print("Insufficient balance.")
                    print("Try transferring within the amount of your remaining balance.")
                else:
                    
                    deduct_query = "UPDATE ATM_DATABASE SET BALANCE = BALANCE - %s WHERE ACCOUNT_NO = %s"
                    con.execute(deduct_query, (m, current_user["ACCOUNT_NO"]))
                    
                    add_query = "UPDATE ATM_DATABASE SET BALANCE = BALANCE + %s WHERE ACCOUNT_NO = %s"
                    con.execute(add_query, (m, trf))
                    
                    update_withdrawal = "UPDATE ATM_DATABASE SET WITHDRAWAL = WITHDRAWAL + %s WHERE ACCOUNT_NO = %s"
                    con.execute(update_withdrawal, (m, current_user["ACCOUNT_NO"]))
                    
                    conn.commit()
                    print(f"Amount successfully transferred to account number {trf}.")
            else:
                print("The target account number does not exist. Please try again.")
            
            t = input("Would you like to do another transaction? y/n: ")
            if t.lower() == "y":
                continue
            else:
                print("Thank you for your transaction. Have a nice day!")
                break

        elif c1 == 5:
            print("Thank you for using our service!")
            logged_in = False

        else:
            print("Invalid option.")
