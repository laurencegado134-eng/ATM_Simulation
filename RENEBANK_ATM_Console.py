import os
import csv
import random
import time
import sys
from datetime import date


class Account:
    def __init__(self):
        self.FName = ""
        self.LName = ""
        self.AccountNumber = ""
        self.PinCode = ""
        self.encryptedPIN = ""
        self.Birthday = ""
        self.ContactNumber = ""
        self.Balance = 0
        self.next = None


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def headDisplay():
    print("\n|==============================================|")
    print("|                   RENEBANK                   |")
    print("|==============================================|")


def encryptPIN(pin):
    result = ""

    for c in pin:
        encrypted = ord(c) ^ 7
        result += format(encrypted, "02x")

    return result


class ATM:
    def __init__(self):
        self.head = None
        self.current = None
        self.drivePath = ""
        self.cardFile = ""

    def Start(self):
        while True:
            clear_screen()
            headDisplay()
            print("|                                              |")
            print("| " + "[1] - Insert Card / Login".ljust(45) + "|")
            print("| " + "[2] - Enroll your Card".ljust(45) + "|")
            print("| " + "[3] - Exit".ljust(45) + "|")
            print("|                                              |")
            print("|==============================================|")
            choice = input("| => ")

            if choice == "1":
                if self.load_account():
                    self.password()
            elif choice == "2":
                self.create_account()
            elif choice == "3":
                self.quit()
            else:
                print("\nPlease choose between 1-3!\n")
                pause()

    def create_account(self):
        clear_screen()
        headDisplay()
        print("|==============================================|")
        print("|                CARD ENROLLMENT               |")
        print("|==============================================|")
        print("|                                              |")
        print("| Enter your Flash Drive path.                 |")
        print("| Example: E:\\\\  |  D:\\\\                       |")
        print("|                                              |")
        self.drivePath = input("| Path: ")

        # i-che-check kung may naka insert na card
        if not self.checkFlashDrive():
            return

        self.cardFile = self.drivePath
        if not self.cardFile.endswith("\\"):
            self.cardFile += "\\"

        self.cardFile += "CARD_DATA_INFORMATION.csv"

        if os.path.isfile(self.cardFile):
            headDisplay()
            print("|==============================================|")
            print("|            CARD ALREADY ENROLLED!            |")
            print("|==============================================|")
            print("|                                              |")
            print("|    This Card is already registered to an     |")
            print("|               account.                       |")
            print("|                                              |")
            print("|    One Card can only be enrolled to ONE      |")
            print("|               account.                       |")
            print("|                                              |")
            print("|==============================================|")
            pause()
            return

        newAccount = Account()
        newAccount.next = None
        newAccount.Balance = 0

        # Same account-number generation as the original C++ program.
        for i in range(6):
            newAccount.AccountNumber += chr(ord('0') + random.randint(0, 5))

        newAccount.AccountNumber = newAccount.AccountNumber[:5]

        while True:
            clear_screen()
            headDisplay()
            print("|==============================================|")
            print("|                   SECURITY                   |")
            print("|==============================================|")
            print("|                                              |")
            tempPIN = input("| Enter your 6 Digit PIN: ")

            if len(tempPIN) != 6:
                print("|==============================================|")
                print("|                 INVALID PIN                  |")
                print("|==============================================|")
                print("|                                              |")
                print("| PIN must be exactly 6 digits!                |")
                print("|                                              |")
                print("|==============================================|")
                pause()
                continue

            valid = True
            for i in range(6):
                if tempPIN[i] < '0' or tempPIN[i] > '9':
                    valid = False
                    break

            if not valid:
                print("|==============================================|")
                print("|                 INVALID PIN                  |")
                print("|==============================================|")
                print("|                                              |")
                print("| PIN must contain numbers only!               |")
                print("|                                              |")
                print("|==============================================|")
                pause()
                continue

            if tempPIN == "000000":
                print("|==============================================|")
                print("|                 INVALID PIN                  |")
                print("|==============================================|")
                print("|                                              |")
                print("| This is a default password!                  |")
                print("| Please choose another PIN.                   |")
                print("|                                              |")
                print("|==============================================|")
                pause()
                continue

            if tempPIN == "123456":
                print("|==============================================|")
                print("|                 INVALID PIN                  |")
                print("|==============================================|")
                print("|                                              |")
                print("| This is an easy password!                    |")
                print("| Please choose another PIN.                   |")
                print("|                                              |")
                print("|==============================================|")
                pause()
                continue

            newAccount.PinCode = tempPIN
            newAccount.encryptedPIN = encryptPIN(newAccount.PinCode)
            break

        newAccount.FName = input("| First Name: ")
        newAccount.LName = input("| Last Name: ")

        while True:
            newAccount.Birthday = input("| Birthday (MMDDYY): ")

            # if letter sinulat
            valid = True
            for i in range(len(newAccount.Birthday)):
                if not newAccount.Birthday[i].isdigit():
                    print("|==============================================|")
                    print("|              INVALID BIRTHDAY                |")
                    print("|==============================================|")
                    print("|                                              |")
                    print("| Birthday must contain numbers only.          |")
                    print("|                                              |")
                    print("|==============================================|")
                    valid = False
                    break

            if not valid:
                pause()
                continue

            # yung haba
            if len(newAccount.Birthday) != 6:
                print("|==============================================|")
                print("|              INVALID BIRTHDAY                |")
                print("|==============================================|")
                print("|                                              |")
                print("| Birthday must be exactly 6 digits.           |")
                print("| Format: MMDDYY                               |")
                print("|                                              |")
                print("|==============================================|")
                pause()
                continue

            # icoconvert sa numbers
            month = int(newAccount.Birthday[0:2])
            day = int(newAccount.Birthday[2:4])
            year = int(newAccount.Birthday[4:6])

            # icoconvert yung 2 digit year sa 4 digit year
            if year <= 26:
                fullYear = 2000 + year
            else:
                fullYear = 1000 + year

            # kung kasing tanda naba ni enrile
            if fullYear < 1800:
                print("|==============================================|")
                print("|              INVALID BIRTHDAY                |")
                print("|==============================================|")
                print("|                                              |")
                print("| Invalid birth year.                          |")
                print("|                                              |")
                print("|==============================================|")
                continue

            # png check ng month
            if month < 1 or month > 12:
                print("|==============================================|")
                print("|              INVALID BIRTHDAY                |")
                print("|==============================================|")
                print("|                                              |")
                print("| Month must be between 01 and 12.             |")
                print("| Example: 01 = January, 12 = December         |")
                print("|                                              |")
                print("|==============================================|")
                pause()
                continue

            # png check ng day
            if month == 2:  # if feb
                # if leap year
                if (fullYear % 400 == 0) or (fullYear % 4 == 0 and fullYear % 100 != 0):
                    maxDays = 29
                else:
                    maxDays = 28
            elif month == 4 or month == 6 or month == 9 or month == 11:
                maxDays = 30
            else:
                maxDays = 31

            if day < 1 or day > maxDays:
                print("|==============================================|")
                print("|              INVALID BIRTHDAY                |")
                print("|==============================================|")
                print("|                                              |")
                print("| Day is not valid for this month.             |")
                print("|                                              |")
                print("|==============================================|")
                pause()
                continue

            # date now
            now = date.today()
            currentYear = now.year
            currentMonth = now.month
            currentDay = now.day

            # pangcheck kung yung nilagay ng user is dili pa sha nabuhay
            if (fullYear > currentYear or
                (fullYear == currentYear and month > currentMonth) or
                (fullYear == currentYear and month == currentMonth and day > currentDay)):
                print("|==============================================|")
                print("|              INVALID BIRTHDAY                |")
                print("|==============================================|")
                print("|                                              |")
                print("| Birthday cannot be in the future.            |")
                print("|                                              |")
                print("|==============================================|")
                pause()
                continue

            age = currentYear - fullYear

            if currentMonth < month or (currentMonth == month and currentDay < day):
                age -= 1

            if age < 18:
                print("|==============================================|")
                print("|              INVALID BIRTHDAY                |")
                print("|==============================================|")
                print("|                                              |")
                print("| You must be at least 18 years old.           |")
                print("|                                              |")
                print("|==============================================|")
                pause()
                continue

            break

        while True:
            newAccount.ContactNumber = input("| Contact Number: ")

            valid = True
            for i in range(len(newAccount.ContactNumber)):
                if not newAccount.ContactNumber[i].isdigit():
                    print("|==============================================|")
                    print("|            INVALID CONTACT NUMBER            |")
                    print("|==============================================|")
                    print("|                                              |")
                    print("| Contact Number must contain numbers only.    |")
                    print("|                                              |")
                    print("|==============================================|")
                    valid = False
                    break

            if not valid:
                pause()
                continue

            if len(newAccount.ContactNumber) != 11:
                print("|==============================================|")
                print("|            INVALID CONTACT NUMBER            |")
                print("|==============================================|")
                print("|                                              |")
                print("| Contact Number must be exactly 11 digits!    |")
                print("|                                              |")
                print("|==============================================|")
                pause()
                continue

            if newAccount.ContactNumber[0] != '0' or newAccount.ContactNumber[1] != '9':
                print("|==============================================|")
                print("|            INVALID CONTACT NUMBER            |")
                print("|==============================================|")
                print("|                                              |")
                print("| Contact Number must start with 09!           |")
                print("|                                              |")
                print("|==============================================|")
                pause()
                continue

            break

        while True:
            newAccount.Balance = int(input("| Deposit (min. 5000): "))

            if newAccount.Balance < 5000:
                print("|==============================================|")
                print("|                INVALID BALANCE               |")
                print("|==============================================|")
                print("|                                              |")
                print("| Minimum Balance Required: 5000               |")
                print("|                                              |")
                print("|==============================================|")
                continue
            else:
                break

        if self.head is None:
            self.head = newAccount
        else:
            p = self.head
            while p.next is not None:
                p = p.next
            p.next = newAccount

        self.current = newAccount

        self.save_account()

        clear_screen()
        headDisplay()
        print("|===============================================|")
        print("|         ACCOUNT ENROLLED SUCCESSFULLY!        |")
        print("|===============================================|")
        print("| " + ("Account Number: " + newAccount.AccountNumber).ljust(45) + " |")
        print("| " + ("  Account Name: " + self.current.FName + " " + self.current.LName).ljust(43) + "    |")
        print("| " + ("Contact Number: " + self.current.ContactNumber).ljust(45) + " |")
        print("| " + ("      Birthday: " + self.current.Birthday).ljust(39) + "       |")
        print("|-----------------------------------------------|")
        print("| " + "Card Status: ENROLLED".ljust(45) + " |")
        print("| " + ("       Balance: PHP " + str(self.current.Balance)).ljust(38) + "       |")
        print("|===============================================|")
        pause()
        self.password()

    def checkFlashDrive(self):
        # Python equivalent of checking whether the entered drive path exists.
        if not os.path.isdir(self.drivePath):
            clear_screen()
            headDisplay()
            print("|==============================================|")
            print("|                  CARD ERROR                  |")
            print("|==============================================|")
            print("|                                              |")
            print("| Card is not inserted or cannot be            |")
            print("| detected by the computer.                    |")
            print("|                                              |")
            print("| Please insert your Flash Drive and try       |")
            print("| again.                                       |")
            print("|                                              |")
            print("|==============================================|")
            pause()
            return False
        return True

    def load_account(self):
        clear_screen()
        headDisplay()
        print("| " + "Enter Card Path.".ljust(45) + "|")
        print("| " + "Example: E:\\".ljust(45) + "|")
        self.drivePath = input("| Path: ")

        # i-che-check nito kung naka insert na ang card
        if not self.checkFlashDrive():
            return False

        self.cardFile = self.drivePath
        if not self.cardFile.endswith("\\"):
            self.cardFile += "\\"
        self.cardFile += "CARD_DATA_INFORMATION.csv"

        if not os.path.isfile(self.cardFile):
            headDisplay()
            print("|===============================================|")
            print("|                CARD NOT FOUND!                |")
            print("|===============================================|")
            print("|                                               |")
            print("| " + "This Card is not yet enrolled.".ljust(45) + "|")
            print("|                                               |")
            print("|===============================================|")
            pause()
            return False

        newAccount = Account()

        with open(self.cardFile, "r", newline="") as file:
            reader = csv.reader(file)
            header = next(reader, None)
            row = next(reader, [])

        # Preserve the original C++ load order:
        # AccountNumber, LastName, FirstName, Birthday, ContactNumber, PIN, Balance.
        newAccount.AccountNumber = row[0]
        newAccount.LName = row[1]
        newAccount.FName = row[2]
        newAccount.Birthday = row[3]
        newAccount.ContactNumber = row[4]
        newAccount.encryptedPIN = row[5]
        newAccount.Balance = int(row[6])

        if self.head is not None:
            temp = self.head
            while temp is not None:
                deleteNode = temp
                temp = temp.next
                del deleteNode
            self.head = None

        self.head = newAccount
        self.current = newAccount

        headDisplay()
        print("|==============================================|")
        print("|           CARD DETECTED SUCCESSFULLY!        |")
        print("|==============================================|")
        print("|                                              |")
        print("| " + ("Account Number: " + self.current.AccountNumber).ljust(45) + "|")
        print("| " + ("  Account Name: " + self.current.FName + " " + self.current.LName).ljust(45) + "|")
        print("|                                              |")
        print("|==============================================|")
        pause()
        return True

    def save_account(self):
        try:
            with open(self.cardFile, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["AccountNumber", "FistName", "LastName",
                                 "Birthday", "ContactNumber", "PIN", "Balance"])
                writer.writerow([
                    self.current.AccountNumber,
                    self.current.FName,
                    self.current.LName,
                    self.current.Birthday,
                    self.current.ContactNumber,
                    self.current.encryptedPIN,
                    self.current.Balance
                ])
        except OSError:
            print("|==============================================|")
            print("|                      ERROR                   |")
            print("|==============================================|")
            print("|                                              |")
            print("|           UNABLE TO SAVE ACCOUNT!            |")
            print("|                                              |")
            print("|==============================================|")

    def password(self):
        count = 3
        for i in range(count):
            clear_screen()
            headDisplay()
            print("|                                              |")
            print("| Account Number: " + self.current.AccountNumber.ljust(29) + "|")

            accountName = self.current.FName + " " + self.current.LName
            print("| Account Name: " + accountName.ljust(31) + "|")

            print("|                                              |")
            TempPinCode = input("| ENTER 6 DIGIT PIN: ")

            if encryptPIN(TempPinCode) == self.current.encryptedPIN:
                print("|==============================================|")
                print("|              LOGIN SUCCESSFUL                |")
                print("|==============================================|")
                pause()
                self.menu()
                return
            else:
                print("|==============================================|")
                print("|                 WRONG PIN                    |")
                print("|==============================================|")
                print("|                                              |")

                if i < count - 1:
                    print("| Attempts remaining: " + str(count - i - 1).ljust(22) + "   |")

                print("|                                              |")
                print("|==============================================|")
                pause()

        clear_screen()
        print("|==============================================|")
        print("|                 ACCOUNT LOCKED               |")
        print("|==============================================|")
        print("|                                              |")

        for i in range(5, 0, -1):
            print("\r| Account will be unlocked in " + str(i) + " second(s).", end="")
            print("                 |", end="", flush=True)
            time.sleep(1)

        print("\n|                                              |")
        print("| Account is now unlocked.                     |")
        print("|                                              |")
        print("|==============================================|")
        pause()

    def menu(self):
        while True:
            clear_screen()
            headDisplay()
            print("|==============================================|")
            print("| Good Day, " + (self.current.FName + " " + self.current.LName).ljust(35) + "|")
            print("|==============================================|")
            print("|                                              |")
            print("| " + "[1] - Check Balance".ljust(45) + "|")
            print("| " + "[2] - Deposit Money".ljust(45) + "|")
            print("| " + "[3] - Withdraw Money".ljust(45) + "|")
            print("| " + "[4] - Transfer Money".ljust(45) + "|")
            print("| " + "[5] - Change PIN".ljust(45) + "|")
            print("| " + "[6] - Remove Card / Logout".ljust(45) + "|")
            print("|                                              |")
            print("|==============================================|")
            Choice = input("| => ")

            if Choice == "1":
                self.Check_Balance()
            elif Choice == "2":
                self.Deposit_Money()
            elif Choice == "3":
                self.Withdraw_Money()
            elif Choice == "4":
                self.Transfer_Money()
            elif Choice == "5":
                self.Change_PinCode()
            elif Choice == "6":
                self.save_account()

                print("|==============================================|")
                print("|                 REMOVE CARD                  |")
                print("|==============================================|")
                print("|                                              |")
                print("| Saving account...                            |")
                print("| Card removed.                                |")
                print("| Logged out successfully!                     |")
                print("|                                              |")
                print("|==============================================|")
                self.current = None

                pause()
                return
            else:
                print("|==============================================|")
                print("|              INVALID CHOICE                  |")
                print("|==============================================|")
                print("|                                              |")
                print("| Please choose between 1-6!                   |")
                print("|                                              |")
                print("|==============================================|")
                pause()

    def Change_PinCode(self):
        count = 3

        for i in range(count):
            clear_screen()
            headDisplay()
            print("|==============================================|")
            print("|                   SECURITY                   |")
            print("|==============================================|")
            print("|                                              |")
            PinCodeTemp = input("| Enter your current PIN: ")

            if encryptPIN(PinCodeTemp) == self.current.encryptedPIN:
                PinCodeTemp2 = input("| Change PIN: ")

                if len(PinCodeTemp2) != 6:
                    print("|==============================================|")
                    print("|                 INVALID PIN                  |")
                    print("|==============================================|")
                    print("|                                              |")
                    print("| PIN must be exactly 6 digits!                |")
                    print("|                                              |")
                    print("|==============================================|")
                    pause()
                    return

                valid = True
                for j in range(6):
                    if PinCodeTemp2[j] < '0' or PinCodeTemp2[j] > '9':
                        valid = False
                        break

                if not valid:
                    print("|==============================================|")
                    print("|                 INVALID PIN                  |")
                    print("|==============================================|")
                    print("|                                              |")
                    print("| PIN must contain numbers only!               |")
                    print("|                                              |")
                    print("|==============================================|")
                    pause()
                    return

                if PinCodeTemp2 == "000000":
                    print("|==============================================|")
                    print("|                 INVALID PIN                  |")
                    print("|==============================================|")
                    print("|                                              |")
                    print("| This is a default password!                  |")
                    print("| Please choose another PIN.                   |")
                    print("|                                              |")
                    print("|==============================================|")
                    pause()
                    return

                if PinCodeTemp2 == "123456":
                    print("|==============================================|")
                    print("|                 INVALID PIN                  |")
                    print("|==============================================|")
                    print("|                                              |")
                    print("| This is an easy password!                    |")
                    print("| Please choose another PIN.                   |")
                    print("|                                              |")
                    print("|==============================================|")
                    pause()
                    return

                PinCodeTemp3 = input("| Re-Enter PIN: ")

                if PinCodeTemp2 == PinCodeTemp3:
                    self.current.PinCode = PinCodeTemp2
                    self.current.encryptedPIN = encryptPIN(self.current.PinCode)
                    self.save_account()
                    print("|==============================================|")
                    print("|           PIN CHANGED SUCCESSFULLY           |")
                    print("|==============================================|")
                    print("|                                              |")
                    print("| Your PIN has been successfully changed!      |")
                    print("|                                              |")
                    print("|==============================================|")
                    pause()
                    return
                else:
                    print("|==============================================|")
                    print("|                 PIN MISMATCH                 |")
                    print("|==============================================|")
                    print("|                                              |")
                    print("| PINs do not match!                           |")
                    print("|                                              |")
                    print("|==============================================|")
                    pause()
                    return
            else:
                print("|==============================================|")
                print("|                  WRONG PIN                   |")
                print("|==============================================|")
                print("|                                              |")
                print("| Wrong PIN!                                   |")
                print("|                                              |")
                print("|==============================================|")
                pause()

        for i in range(5, 0, -1):
            clear_screen()
            print("|==============================================|")
            print("|                ACCOUNT LOCKED                |")
            print("|==============================================|")
            print("| " + ("Account will open again in " + str(i) + " second(s).").ljust(44) + "|")
            print("| " + "Please contact customer service.".ljust(44) + "|")
            print("|==============================================|")
            time.sleep(1)

        pause()

    def Deposit_Money(self):
        clear_screen()
        headDisplay()
        Deposit = int(input("| Enter Amount (min. PHP100): "))

        if Deposit < 100:
            print("| " + "Minimum deposit is PHP100!".ljust(45) + "|")
        else:
            self.current.Balance += Deposit
            self.save_account()
            print("| " + "Transaction Complete!".ljust(45) + "|")
            print("| " + ("New Balance: PHP " + str(self.current.Balance)).ljust(45) + "|")

        pause()

    def Withdraw_Money(self):
        clear_screen()
        headDisplay()
        if self.current.Balance == 0:
            print("|==============================================|")
            print("|             INSUFFICIENT BALANCE             |")
            print("|==============================================|")
            print("|                                              |")
            print("| Your account has no available balance.       |")
            print("|                                              |")
            print("|==============================================|")
            pause()
            return

        if self.current.Balance <= 5000:
            print("|==============================================|")
            print("|           WITHDRAWAL UNAVAILABLE             |")
            print("|==============================================|")
            print("|                                              |")
            print("| Your account must maintain a minimum         |")
            print("| balance of PHP5000.                          |")
            print("|                                              |")
            print("| Withdrawal Unavailable.                      |")
            print("|                                              |")
            print("|==============================================|")
            pause()
            return

        Withdraw = int(input("| Enter Amount (min. PHP100): "))

        if Withdraw < 100:
            print("|==============================================|")
            print("|              INVALID AMOUNT                  |")
            print("|==============================================|")
            print("|                                              |")
            print("| Minimum withdrawal is PHP100!                |")
            print("|                                              |")
            print("|==============================================|")
        elif Withdraw > self.current.Balance:
            print("|==============================================|")
            print("|           INSUFFICIENT BALANCE               |")
            print("|==============================================|")
            print("|                                              |")
            print("| You must maintain PHP5000 in your account.   |")
            print("|                                              |")
            print("| Available to withdraw: PHP" +
                  str(self.current.Balance - 5000).ljust(25) + "|")
            print("|                                              |")
            print("|==============================================|")
        else:
            self.current.Balance -= Withdraw
            self.save_account()
            print("|==============================================|")
            print("|           TRANSACTION COMPLETED              |")
            print("|==============================================|")
            print("|                                              |")
            print("| Withdrawal successful!                       |")
            print("|                                              |")
            print("| Remaining Balance: PHP" +
                  str(self.current.Balance).ljust(23) + "|")
            print("|                                              |")
            print("|                                              |")
            print("|==============================================|")

        pause()

    def Transfer_Money(self):
        clear_screen()
        headDisplay()
        if self.current.Balance == 0:
            print("|==============================================|")
            print("|             INSUFFICIENT BALANCE             |")
            print("|==============================================|")
            print("|                                              |")
            print("| Your account has no available balance.       |")
            print("|                                              |")
            print("|==============================================|")
            pause()
            return

        if self.current.Balance <= 5000:
            print("|==============================================|")
            print("|            TRANSFER UNAVAILABLE              |")
            print("|==============================================|")
            print("|                                              |")
            print("| Your account must maintain a minimum         |")
            print("| balance of PHP5000.                          |")
            print("|                                              |")
            print("| Transfer Unavailable.                        |")
            print("|                                              |")
            print("|==============================================|")
            pause()
            return

        TransferAccountNumber = input("| Account Number: ")
        while True:
            valid = True
            for i in range(len(TransferAccountNumber)):
                if not TransferAccountNumber[i].isdigit():
                    print("|==============================================|")
                    print("|            INVALID ACCOUNT NUMBER            |")
                    print("|==============================================|")
                    print("|                                              |")
                    print("| Account Number must contain numbers only.    |")
                    print("|                                              |")
                    print("|==============================================|")
                    valid = False
                    break

            if not valid:
                pause()
                TransferAccountNumber = input("| Account Number: ")
                continue

            if len(TransferAccountNumber) != 5:
                print("|==============================================|")
                print("|            INVALID ACCOUNT NUMBER            |")
                print("|==============================================|")
                print("|                                              |")
                print("| Account Number must be exactly 5 digits!     |")
                print("|                                              |")
                print("|==============================================|")
                pause()
                return
            break

        recipient = input("| Account Name: ")
        Transfer = int(input("| Enter Amount (min. PHP100): "))

        if Transfer > self.current.Balance:
            print("|==============================================|")
            print("|           INSUFFICIENT BALANCE               |")
            print("|==============================================|")
            print("|                                              |")
            print("| You must maintain PHP5000 in your account.   |")
            print("|                                              |")
            print("| Balance: PHP" +
                  str(self.current.Balance - 5000).ljust(39) + "|")
            print("|                                              |")
            print("|==============================================|")
        else:
            self.current.Balance -= Transfer
            self.save_account()
            print("|==============================================|")
            print("|           TRANSACTION COMPLETED             |")
            print("|==============================================|")
            print("|                                              |")
            print("| Transfer successful!                        |")
            print("|                                              |")
            print("| Recipient Name: " + recipient.ljust(28) + "|")
            print("| Account Number: " + TransferAccountNumber.ljust(28) + "|")
            print("| Amount Transferred: PHP" + str(Transfer).ljust(21) + "|")
            print("|                                              |")
            print("| Remaining Balance: PHP" + str(self.current.Balance).ljust(22) + "|")
            print("|                                              |")
            print("|==============================================|")

        pause()

    def Check_Balance(self):
        clear_screen()
        name = self.current.FName + " " + self.current.LName
        accountNumber = self.current.AccountNumber
        balance = "PHP" + str(self.current.Balance)
        headDisplay()
        print("|==============================================|")
        print("|               ACCOUNT BALANCE                |")
        print("|==============================================|")
        print("| " + ("Account Number: " + accountNumber).ljust(45) + "|")
        print("| " + ("Account Name: " + name).ljust(45) + "|")
        print("| " + ("Balance: " + balance).ljust(45) + "|")
        print("|==============================================|")
        print("| ", end="")
        pause()

    def quit(self):
        print("\t\033[1;31mExiting...\033[0m")
        sys.exit(0)


if __name__ == "__main__":
    random.seed(time.time())

    bank = ATM()
    bank.Start()
