from pymongo import MongoClient

def show_all_records(collection):
    
    cursor = collection.find()
    found = False
    for document in cursor:
        found = True
        print(f"ID: {document.get('_id')}, bikes_name: {document.get('bikes_name')}, "
              f"price: {document.get('price')}, passing : {document.get('passing')}")
    if not found:
        print("No records found.")

def insert_record(collection):
    
    bikes_name = input("Enter name of bike: ")
    price = int(input("Enter price: "))
    passing = input("Enter Passing Place: ")
    collection.insert_one({"bikes_name": bikes_name, "price": price, "passing" : passing})
    print("Record inserted successfully.")

def delete_record(collection):
    
    bikes_name = input("Enter the name of bikes to delete: ")
    result = collection.delete_one({"bikes_name": bikes_name})
    if result.deleted_count > 0:
        print(f"Record with name '{bikes_name}' deleted successfully.")
    else:
        print(f"No record found with name '{bikes_name}'.")

def update_record(collection):
    
    bikes_name = input("Enter the name of bikes to update: ")
    record = collection.find_one({"bikes_name": bikes_name})

    if record:
        print("Record found. Enter the new values (press Enter to skip):")
        new_name = input(f"Enter new name (current: {record['bikes_name']}): ") or record["bikes_name"]
        new_price = input(f"Enter new price (current: {record['price']}): ") or record["price"]
        new_passing = input(f"Enter new passing place (current: {record['passing']}): ") or record["passing"]

        
        collection.update_one(
            {"_id": record["_id"]},
            {"$set": {"bikes_name": new_name, "price": int(new_price), "passing": new_passing}}
        )
        print("Record updated successfully.")
    else:
        print(f"No record found with name '{bikes_name}'.")


def search_record(collection):
    bikes_name = input("Enter bike name to search: ")
    cursor = collection.find({"bikes_name": {"$regex": bikes_name, "$options": "i"}})

    for document in cursor:
        print(f"ID: {document['_id']}, bikes_name: {document['bikes_name']}, "
              f"price: {document['price']}, passing: {document['passing']}")
        return
    
    print(f"No records found for '{bikes_name}'.")


def main():
    
    mongo = MongoClient("localhost", 27017)
    print("Connected successfully")

    db = mongo["Info"]
    collection = db["Personal"]

    while True:
        print("\n--- Menu ---")
        print("1. Insert a record")
        print("2. Delete a record")
        print("3. Update a record")
        print("4. Show all records")
        print("5. Search Record")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            insert_record(collection)
        elif choice == '2':
            delete_record(collection)
        elif choice == '3':
            update_record(collection)
        elif choice == '4':
            show_all_records(collection)
        elif choice == '5' :
            search_record(collection)
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()