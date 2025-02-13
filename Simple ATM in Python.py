import time
from colorama import Fore, Style, init
from datetime import datetime
import sys
import getpass

# Initialize colorama
init(autoreset=True)

# Sample account data
accounts = {
    '0503092205': {
        'pin': '0322',
        'balance': 3092202.50,
        'transactions': [],
        'name': 'John Marc'
    }
}

def clear_screen():
    """Clear the console screen"""
    print("\033c", end="")

def progress_bar(duration):
    """Show a progress bar"""
    for i in range(101):
        time.sleep(duration/100)
        sys.stdout.write(f"\r[{i*'#'}{(100-i)*' '}] {i}%")
        sys.stdout.flush()
    print()

def print_header():
    """Display ATM header"""
    clear_screen()
    print(Fore.CYAN + """
    ╔══════════════════════════════╗
    ║        JM ATM 3000           ║
    ║  "Your Financial Partner"    ║
    ╚══════════════════════════════╝
    """)

def authenticate():
    """Handle user authentication"""
    attempts = 3
    while attempts > 0:
        print_header()
        print(Fore.YELLOW + "  Please authenticate yourself")
        account_number = input(Fore.WHITE + "  Enter account number: ")
        pin = getpass.getpass(Fore.WHITE + "  Enter PIN: ")

        if account_number in accounts and accounts[account_number]['pin'] == pin:
            return account_number
        else:
            print(Fore.RED + "\n  Invalid credentials!")
            attempts -= 1
            time.sleep(1.5)
            if attempts > 0:
                print(Fore.YELLOW + f"  {attempts} attempts remaining")
                time.sleep(1)
    print(Fore.RED + "\n  Account locked! Please contact your bank.")
    sys.exit()

def show_menu():
    """Display main menu"""
    print(Fore.MAGENTA + """
    [1] Check Balance      [3] Withdraw
    [2] Deposit           [4] Transaction History
    [5] Exit
    """)
    return input(Fore.WHITE + "  Select option (1-5): ")

def handle_deposit(account):
    """Handle deposit operation"""
    print_header()
    print(Fore.GREEN + "  ─── DEPOSIT ───")
    try:
        amount = float(input(Fore.WHITE + "  Enter amount to deposit: $"))
        if amount <= 0:
            raise ValueError
        accounts[account]['balance'] += amount
        record_transaction(account, f"Deposit: +${amount:.2f}")
        print(Fore.GREEN + "\n  Processing...")
        progress_bar(2)
        print(Fore.GREEN + f"  Success! New balance: ${accounts[account]['balance']:.2f}")
    except ValueError:
        print(Fore.RED + "  Invalid amount! Please enter positive numbers only.")
    time.sleep(2)

def handle_withdraw(account):
    """Handle withdrawal operation"""
    print_header()
    print(Fore.BLUE + "  ─── WITHDRAW ───")
    try:
        amount = float(input(Fore.WHITE + "  Enter amount to withdraw: $"))
        if amount <= 0:
            raise ValueError
        if amount > accounts[account]['balance']:
            print(Fore.RED + "  Insufficient funds!")
        elif amount % 10 != 0:
            print(Fore.RED + "  Amount must be in multiples of $10")
        else:
            accounts[account]['balance'] -= amount
            record_transaction(account, f"Withdrawal: -${amount:.2f}")
            print(Fore.BLUE + "\n  Processing...")
            progress_bar(2)
            print(Fore.BLUE + f"  Please take your cash!\n  New balance: ${accounts[account]['balance']:.2f}")
    except ValueError:
        print(Fore.RED + "  Invalid amount! Please enter positive numbers only.")
    time.sleep(2)

def record_transaction(account, description):
    """Record transaction with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    accounts[account]['transactions'].append(f"{timestamp} - {description}")

def show_history(account):
    """Display transaction history"""
    print_header()
    print(Fore.YELLOW + "  ─── TRANSACTION HISTORY ───")
    if not accounts[account]['transactions']:
        print(Fore.WHITE + "  No transactions yet")
    else:
        for trans in accounts[account]['transactions']:
            print(Fore.WHITE + f"  {trans}")
    input("\n  Press Enter to continue...")

def atm_machine():
    """Main ATM function"""
    account = authenticate()
    print_header()
    print(Fore.GREEN + f"  Welcome, {accounts[account]['name']}!")
    time.sleep(1.5)
    
    while True:
        print_header()
        print(Fore.CYAN + f"  Current Balance: ${accounts[account]['balance']:.2f}")
        choice = show_menu()
        
        if choice == '1':
            print_header()
            print(Fore.CYAN + f"  Available Balance: ${accounts[account]['balance']:.2f}")
            input("\n  Press Enter to continue...")
        elif choice == '2':
            handle_deposit(account)
        elif choice == '3':
            handle_withdraw(account)
        elif choice == '4':
            show_history(account)
        elif choice == '5':
            print_header()
            print(Fore.MAGENTA + "  Thank you for banking with us!")
            print(Fore.YELLOW + "  Please take your card")
            time.sleep(2)
            break
        else:
            print(Fore.RED + "  Invalid choice!")
            time.sleep(1)

if __name__ == "__main__":
    atm_machine()