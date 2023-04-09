from flask import Flask, Response
from webargs import fields
from webargs.flaskparser import use_args

from application.services.create_table import create_table
from application.services.db_connection import DBConnection

app = Flask(__name__)


@app.route('/')
def home_work_7():  # put application's code here
    return """
    <html>
        <head>
            <title>Home work 7. Flask/DB</title>
        </head>
        <body>
            <h1>Home work 7. Flask/DB</h1>
            <a href=/contacts/read-all target="_blank">Read all contacts</a>
            <h2>Routes for interacting with the DB:</h2>
            <h4>Add new contact to DB -> /contacts/create?contact_name=&phone_value= </h4>
            <h4>Reading one of the contacts -> /contacts/read/<i>number</i></h4>
            <h4>Update one of the contacts -> /contacts/update/<i>number</i>?contact_name=&phone_value=</h4>
            <h4>Delete a contact -> /contacts/delete/<i>number</i></h4>
        </body>
    </html>
    """


@app.route("/contacts/create")
@use_args({"contact_name": fields.Str(required=True), "phone_value": fields.Int(required=True)}, location="query")
def contact__create(args):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "INSERT INTO phones (contact_name, phone_value) VALUES (:contact_name, :phone_value);",
                {"contact_name": args["contact_name"], "phone_value": args["phone_value"]},
            )
    return """
    <html>
        <body>
            <h3>Operation completed.</h3><br>
            <h3>Information successfully added to DB.</h3><br>
            <a href=/>To the main.</a>
        </body>
    </html>
    """


@app.route("/contacts/read-all")
def read_all_phones():
    with DBConnection() as connection:
        contacts = connection.execute("SELECT * FROM phones;").fetchall()
    return f"""
    {"<br>".join(
        [f'{contact["phone_id"]}: {contact["contact_name"]} - {contact["phone_value"]}' for contact in contacts]
    )}
    """


@app.route("/contacts/read/<int:phone_id>")
def phone__read(phone_id: int):
    with DBConnection() as connection:
        contact = connection.execute(
            "SELECT * " "FROM phones " "WHERE (phone_id=:phone_id);",
            {
                "phone_id": phone_id,
            },
        ).fetchone()
    return f"""
    <html>
        <head>
            <title>Contact read</title>
        </head>
        <body>
            {contact["phone_id"]}: {contact["contact_name"]} - {contact["phone_value"]}<br>
            <a href=/>To the main.</a>
        </body>
    </html>
    """


@app.route("/contacts/update/<int:phone_id>")
@use_args({"contact_name": fields.Str(), "phone_value": fields.Int()}, location="query")
def contact__update(args, phone_id: int):
    with DBConnection() as connection:
        with connection:
            contact_name = args.get("contact_name")
            phone_value = args.get("phone_value")
            if contact_name is None and phone_value is None:
                return Response(
                    "You didn't give any arguments to update the data!",
                    status=400
                )

            args_for_request = []
            if contact_name is not None:
                args_for_request.append("contact_name=:contact_name")
            if phone_value is not None:
                args_for_request.append("phone_value=:phone_value")

            args_2 = ", ".join(args_for_request)
            connection.execute(
                "UPDATE phones " f"SET {args_2} " "WHERE phone_id=:phone_id;",
                {
                    "phone_id": phone_id,
                    "contact_name": contact_name,
                    "phone_value": phone_value,
                },
            )
    return """
    <html>
        <head>
            <title>Update contacts</title>
        </head>
        <body>
            <h3>The operation is successful. Information updated.</h3><br>
            <a href=/>To the main.</a>
        </body>
    </html>
    """


@app.route("/contacts/delete/<int:phone_id>")
def contact__delete(phone_id):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "DELETE FROM phones WHERE (phone_id=:phone_id);",
                {
                    "phone_id": phone_id,
                },
            )
    return """
    <html>
        <head>
            <title>Contacts delete</title>
        </head>
        <body>
            <h3>Data deletion was successful.</h3><br>
            <a href=/>To the main.</a>
        </body>
    </html>
    """


create_table()

if __name__ == '__main__':
    app.run()
