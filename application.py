from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_cors import  CORS ,cross_origin
app = Flask(__name__)
cors=CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['CORS_HEADERS']='Content-Type'
db = SQLAlchemy(app)


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(180))

    def __repr__(self):
        return str({'id': self.id,
                    'name': self.name,
                    'description': self.description
                    })


@app.route('/')
@cross_origin()
def index():
    return 'hello from flask'


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    output = [{'id': drink.id, 'name': drink.name, 'description': drink.description} for drink in drinks]
    print(f"*******{drinks}*******{type(drinks[0])}")
    print(f"*******{output}*******{type(output[0])}")
    return {'drinks': output}


@app.route('/drink/<id>')
def get_drink_by_id(id):
    drink = Drink.query.get_or_404(id)
    return {'id': drink.id, "name": drink.name, 'description': drink.description}


@app.route('/add-drink', methods=['POST'])
# {
    # "name": drink.name,
    # 'description': drink.description
# }
def add_drink():
    drink = Drink(
        name=request.json['name'],
        description=request.json['description']
    )
    db.session.add(drink)
    db.session.commit()
    return {
        'id':drink.id,
        'name':drink.name,
        'description':drink.description
    }

@app.route('/del-drink/<id>',methods=['DELETE'])
def delete_drink(id):
    drink=Drink.query.get(id)
    db.session.delete(drink)
    db.session.commit()
    return {'id':drink.id}