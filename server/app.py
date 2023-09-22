from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
#to give permisiion to the server about the API in order to access the website
CORS(app)
#or use the @cross_origin() decorator on specific routes
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    messages = Message.query.all()
    messages_serialized = [message.to_dict() for message in messages]

    response = make_response(
        messages_serialized,
        200
    )
    return response
    return ''

@app.route('/messages/<int:id>')
def messages_by_id(id):

    messages = Message.query.filter_by(id=id).first()
    messages_serialized = messages.to_dict()

    response = make_response(
        messages_serialized,
        200
    )
    return response
@app.route('/messages',methods=['GET'])
def messages_created_at():
        request.method == 'GET'
        messages_created_at= []
        for message_created_at in Message.query.all():
            message_created_at_dict = message_created_at.to_dict()
            messages_created_at.append(message_created_at_dict)

        response = make_response(
            jsonify(messages_created_at),
            200
        )

        return response


@app.route('/messages',methods=['POST'])
def messages_updated_at():
        request.method == 'POST'
        new_message_updated_at =Message (
            body=request.form.get("body"),
            username=request.form.get("username"),
        )

        db.session.add(new_message_updated_at)
        db.session.commit()

        baked_message_updated_at_dict = new_message_updated_at.to_dict()

        response = make_response(
            jsonify(baked_message_updated_at_dict),
            201
        )

        return response
@app.route('/messages/<int:id>',methods=['PATCH'])
def messager_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if message == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(jsonify(response_body), 404)

        return response

    else:
            
            request.method == 'PATCH'
            message= Message.query.filter_by(id=id).first()

            for attr in request.form:
                setattr(message, attr, request.form.get(attr))

            db.session.add(message)
            db.session.commit()

            message_dict = message.to_dict()

            response = make_response(
                jsonify(message_dict),
                200
            )

            return response

@app.route('/messages/<int:id>',methods=['DELETE'])
def messaged_by_id(id):
      message = Message.query.filter_by(id=id).first()

      if message == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(jsonify(response_body), 404)

        return response
      elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "bakery deleted."    
            }

            response = make_response(
                jsonify(response_body),
                200
            )

            return response
     
     

if __name__ == '__main__':
    app.run(port=5555)
