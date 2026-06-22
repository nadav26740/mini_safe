import argparse
from core import DataDB, PasswordManager, Actions
import pyperclip
import getpass
import sys

DB_DEFAULT_PATH = ".temp/mini_cryptodata.db"

def main():
    parser = argparse.ArgumentParser(description="small simple project to hold sensitive data using password based cryptography")
    
    parser.add_argument("--get", metavar='name', help="Retrieve and display the data for the given name.")
    parser.add_argument("--set", nargs=2, metavar=('name', 'data'), help="Store the given data under the given name.")
    parser.add_argument("--force", "-f", action="store_true", help="Store the given data under the given name.")
    parser.add_argument("--get-all", action="store_true", help="display all stored data (names).")
    parser.add_argument(
        "--db_path",
        type=str,
        help="Path to the SQLite database file. If the file does not exist, it will be created.",
    )
    parser.add_argument("--metadata", action="store_true", help="Display database metadata.")
    parser.add_argument("--clip", action="store_true", help="Copy retrieved data to clipboard instead of displaying it.")
    parser.add_argument("--init", "--create-db", action="store_true", 
                        help="Create the database if it does not exist. If the database already exists, this option will be ignored.",)
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        print(f"{sys.argv[0]} --help")
        return
    
    if args.db_path is None:
        db = DataDB(DB_DEFAULT_PATH)
    else:
        db = DataDB(args.db_path)

    db.Connect()


    # verify inputs!
    if args.get and args.set:
        print("Error: --get and --set options cannot be used together.")
        return

    password = PasswordManager(getpass.getpass("Enter password: ").encode('utf-8'))
    actions = Actions(db, password)

    # calls
    try:
        if args.init:
            handle_init(args, actions)
            return

        if db.verify_tables() is False:
            print("Database tables do not exist. Use --init to create the database.")
            return

        if args.get:
            handle_get(args, actions)

        elif args.set:
            handle_set(args, actions)

        elif args.get_all:
            handle_get_all(args, actions)

        elif args.metadata:
            handle_metadata(args, actions)

    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        db.Close()

def handle_init(args, actions):
    actions.init_db(args.force)
    print("Database created successfully.")


def handle_get(args, actions):
    data = actions.get(args.get)
    if args.clip:            
        pyperclip.copy(data)
        print(f"{args.get} copied to clipboard.")
    else:
        print(f"{args.get}: {data}")


def handle_set(args, actions):
    actions.insert(args.set[0], args.set[1], args.force)
    print(f"{args.set[0]} stored successfully.")


def handle_get_all(args, actions):
    print("Stored data names:")
    for name in actions.get_all():
        print(name)


def handle_metadata(args, actions):
    print("Database metadata:")
    for key, value in actions.get_metadata().items():
        print(f"{key}: {value}")


def help():
    print(f"{sys.argv[0]} --help")
    print("--get <name>", Actions.get.__doc__)
    print("--set <name> <data>", Actions.insert.__doc__)
    print("--init", Actions.init_db.__doc__)

if __name__ == "__main__":
    main()