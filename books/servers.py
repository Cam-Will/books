from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
app = Flask(__name__)
@app.route("/authors")
def authors():
    mysql = connectToMySQL('books')
    query = "SELECT * FROM books.authors;"
    authors = mysql.query_db(query)
    print(authors)
    return render_template("authors.html", authors = authors)

@app.route("/authors", methods=["POST"]) 
def add_author_to_db():
    mysql = connectToMySQL("books")
    query = "INSERT INTO `books`.`authors` (`name`) VALUES (%(dn)s);"
    data = {
        "dn": request.form["author"],
    }
    author = mysql.query_db(query, data)
    print(author)
    return redirect("/authors")

@app.route("/books")
def books():
    mysql = connectToMySQL('books')
    query = "SELECT * FROM books.books;"
    books = mysql.query_db(query)
    print(books)
    return render_template("books.html", books = books)

@app.route("/books", methods=["POST"]) 
def add_book_to_db():
    mysql = connectToMySQL("books")
    query = "INSERT INTO `books`.`books` (`title`, `num_of_pages`) VALUES (%(title)s, %(num)s);"
    data = {
        "title": request.form["title"],
        "num": request.form["number"]
    }
    author = mysql.query_db(query, data)
    print(author)
    return redirect("/books")

@app.route("/authors/<authors_id>")
def show_authfave(authors_id):
    mysql = connectToMySQL("books")
    query = "SELECT * FROM books.authors WHERE id = %(auth_id)s;"
    data = {
        "auth_id": authors_id
    }
    fave = mysql.query_db(query,data)
    print(fave)
    mysql = connectToMySQL("books")
    query = "SELECT * FROM books.books;"
    book = mysql.query_db(query,data)
    print(book)
    mysql = connectToMySQL("books")
    query = "SELECT * FROM favorites JOIN books ON favorites.books_id = books.id WHERE authors_id = %(auth_id)s;"
    data = {
        "auth_id": authors_id
    }
    books = mysql.query_db(query,data)
    print(books)
    return render_template("author_show.html", book = book, author = fave, books = books)

@app.route("/authors/<authors_id>", methods=["POST"] )
def add_book(authors_id):
    mysql = connectToMySQL("books")
    query = "INSERT INTO books.favorites (authors_id, books_id) VALUES (%(auth_id)s, %(book_id)s);"
    data = {
        "auth_id": authors_id,
        "book_id": request.form["book"]
    }
    fave = mysql.query_db(query,data)
    print(fave)
    return redirect(f"/authors/{authors_id}")

@app.route("/books/<books_id>")
def show_bookfave(books_id):
    mysql = connectToMySQL("books")
    query = "SELECT * FROM books.books WHERE id = %(book_id)s;"
    data = {
        "book_id": books_id
    }
    books = mysql.query_db(query,data)
    print(books)
    mysql = connectToMySQL("books")
    query = "SELECT * FROM books.authors;"
    author = mysql.query_db(query,data)
    print(author)
    mysql = connectToMySQL("books")
    query = "SELECT * FROM favorites LEFT JOIN authors ON favorites.authors_id = authors.id WHERE books_id = %(book_id)s;"
    data = {
        "book_id": books_id
    }
    connects = mysql.query_db(query,data)
    print(books)
    return render_template("books_show.html", books = books[0], authors = author, connects = connects)

@app.route("/books/<books_id>", methods=["POST"] )
def add_author(books_id):
    mysql = connectToMySQL("books")
    query = "INSERT INTO books.favorites (authors_id, books_id) VALUES (%(auth_id)s, %(book_id)s);"
    data = {
        "book_id": books_id,
        "auth_id": request.form["author"]
    }
    fave = mysql.query_db(query,data)
    print(fave)
    return redirect(f"/books/{books_id}")



if __name__ == "__main__":
    app.run(debug=True)