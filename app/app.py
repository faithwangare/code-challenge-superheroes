from flask import Flask, jsonify, request
from models import db, Hero, Power, HeroPower
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''


@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = []
    for hero in heroes:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        }
        hero_list.append(hero_data)
    return jsonify(hero_list)


@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': []
        }
        for power in hero.powers:
            power_data = {
                'id': power.id,
                'name': power.name,
                'description': power.description
            }
            hero_data['powers'].append(power_data)
        return jsonify(hero_data)
    else:
        return jsonify({'error': 'Hero not found'}), 404


@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = []
    for power in powers:
        power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        power_list.append(power_data)
    return jsonify(power_list)


@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power(power_id):
    power = Power.query.get(power_id)
    if power:
        power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        return jsonify(power_data)
    else:
        return jsonify({'error': 'Power not found'}), 404


@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)
    if power:
        data = request.get_json()
        description = data.get('description')
        if description:
            power.description = description
            db.session.commit()
            return jsonify({
                'id': power.id,
                'name': power.name,
                'description': power.description
            })
        else:
            return jsonify({'error': 'Invalid data'}), 400
    else:
        return jsonify({'error': 'Power not found'}), 404


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    if not strength or not power_id or not hero_id:
        return jsonify({'error': 'Invalid data'}), 400

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero or not power:
        return jsonify({'error': 'Invalid hero or power'}), 400

    hero_power = HeroPower(
        strength=strength, hero_id=hero_id, power_id=power_id)
    db.session.add(hero_power)
    db.session.commit()

    return jsonify(get_hero(hero_id))


if __name__ == '__main__':
    app.run(port=5555)