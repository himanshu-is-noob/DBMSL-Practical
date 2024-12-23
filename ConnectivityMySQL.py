import mysql.connector as mc

options = {
    "host": "localhost",
    "user": "root",       # Ensure this user exists
    "password": "password",   # Enter Your Password here
    "database": "TECO2425A006",  #Enter Your Database Name
}


class Connection:
    def __init__(self, options):
        try:
            self.client = mc.connect(**options)
            self.cursor = self.client.cursor()
            if self.client.is_connected():
                print("Connected to database successfully!")
        except mc.Error as err:
            print(f"Error: {err}")
            self.client = None
            self.cursor = None
    
    def _check_connection(self):
        if self.cursor is None or self.client is None:
            print("Database connection not established. Please check your connection settings.")
            return False
        return True
    
    def list_rows(self):
        if not self._check_connection():
            return
        try:
            self.cursor.execute("SELECT * FROM publisher")
            results = self.cursor.fetchall()

            print("bookID\tBook Name\t\t\t\tAuthor\t\t\tprice")
            for row in results:
                print(
                    "{0}\t{1}\t\t\t\t{2}\t\t{3}".format(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                    )   
                )
        except mc.Error as err:
            print(f"Error: {err}")

    def create_row(self):
        if not self._check_connection():
            return
        try:
            print("\nenter new book details")
            book_name = input("name of book : ")
            author = input("name of Author : ")
            price = float(input("price of book : "))

            self.cursor.execute(
                "INSERT INTO publisher(book_name,author,price) VALUES(%s,%s,%s)", 
                (book_name, author, price),
            )
            self.client.commit()

            print("\nnew book added !")
        except mc.Error as err:
            print(f"Error: {err}")

    def delete_row(self):
        if not self._check_connection():
            return
        try:
            bookID = int(input("\nenter id of book to remove : "))
            self.cursor.execute(f"delete from publisher where bookID={bookID}")
            self.client.commit()
            print("Successfully Deleted the Book !")
            
        except mc.Error as err:
            print(f"Error: {err}")

    def update_row(self):
        if not self._check_connection():
            return
        try:
            bookID = int(input("\nenter book id to update : "))

            price = float(input("price of book : "))

            #query = "update publisher set price={0} where bookID={1}".format(price, bookID)
            #self.cursor.execute(query)

            self.cursor.execute(
                f"update publisher set price = {price} where bookID = {bookID}"
            )
            self.client.commit()

           

            print("\nbook data updated Successfully!")
        except mc.Error as err:
            print(f"Error: {err}")

    def search_row(self):
        if not self._check_connection():
            return
        try:
            authorName = input("enter name of author : ")
            self.cursor.execute(
                f"SELECT * FROM publisher WHERE author LIKE '%{authorName}%'"
            )
            results = self.cursor.fetchall()
            print("bookID\tBook Name\t\tAuthor\t\tprice")
            for row in results:
                print(
                    "{0}\t{1}\t\t\t\t{2}\t\t{3}".format(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                    )
                )
        except mc.Error as err:
            print(f"Error: {err}")
        
        if len(results) == 0:
            print(f"No books found for author: {authorName}")

        
        

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.client:
            self.client.close()


client = Connection(options)
while True:
    print("\n\t\t\tLibrary\t\t\t")
    print("1. Add Book")    
    print("2. Show Every Book")
    print("3. Update Book")
    print("4. Delete Book")
    print("5. Search Book")

    try:
        ch = int(input("\nenter option : "))

        if ch == 1:
            client.create_row()

        elif ch == 2:
            
            client.list_rows()

        elif ch == 3:
            client.update_row()
        elif ch == 4:
            client.delete_row()

        elif ch == 5:
            client.search_row()

        elif ch > 6:
            client.close()
            print("thank you !")
            break
    except ValueError:
        print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")