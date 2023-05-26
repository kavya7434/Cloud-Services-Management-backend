from flask import *

from flask_cors import CORS

from db_manage import Db_management

app = Flask(__name__)

CORS(app)

db_manager = Db_management()


# Endpoint to add a new category
# y to the sidebar
@app.route('/add-category', methods=['POST'])
def add_category():
    category_name = request.json.get('categoryName')
    resp = make_response({'message': ("(%s)", db_manager.add_category(category_name))})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# Endpoint to remove a category from the sidebar
@app.route('/remove-category/<string:category_name>', methods=['DELETE'])
def remove_category(category_name):
    # resp = make_response({'message': ("(%s)", db_manager.delete_category(category_name))})
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    return db_manager.delete_category(category_name)


# Endpoint to add a new service to a category
@app.route('/add-service', methods=['POST'])
def add_service():
    category_name = request.json.get('categoryName')
    service_name = request.json.get('serviceName')
    resp = make_response({'message': ("(%s)", db_manager.add_service(category_name, service_name))})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# Endpoint to remove a service from a category
@app.route('/remove-service/<string:category_name>/<string:service_name>', methods=['DELETE'])
def remove_service(category_name, service_name):
    # resp = make_response({'message': ("(%s)", db_manager.delete_service(category_name, service_name))})
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    db_manager.delete_service(category_name, service_name)
    return "deleted successfully"


# Endpoint to add a new field to a service
@app.route('/add-field', methods=['POST'])
def add_field():
    category_name = request.json.get('categoryName')
    service_name = request.json.get('serviceName')
    field_name = request.json.get('fieldName')
    field_value = request.json.get('fieldValue')
    field_type = request.json.get('fieldType')
    resp = make_response(
        {'message': ("(%s)", db_manager.add_field(category_name, service_name, field_name, field_value, field_type))})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/update-field', methods=['PUT'])
def update_field():
    category_name = request.json.get('categoryName')
    service_name = request.json.get('serviceName')
    field_name = request.json.get('fieldName')
    new_field_value = request.json.get('fieldValue')
    resp = make_response(
        {'message': ("(%s)", db_manager.update_field(category_name, service_name, field_name, new_field_value))})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/update-fields', methods=['PUT'])
def update_fields():
    category_name = request.json.get('categoryName')
    service_name = request.json.get('serviceName')
    fields = request.json.get('fields')

    for field_name, field_value in fields.items():
        db_manager.update_field(category_name, service_name, field_name, field_value)
    resp = make_response({'message': "fields updated"})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/remove-field', methods=['POST'])
def remove_field():
    category_name = request.json.get('categoryName')
    service_name = request.json.get('serviceName')
    field_name = request.json.get('fieldName')

    db_manager.delete_field(category_name, service_name, field_name)
    return "deleted"


@app.route('/dto', methods=['GET'])
def get_dto():
    dto = db_manager.get_dto()
    return jsonify(dto)


@app.route('/cat_service', methods=['GET'])
def get_category_service():
    dto = db_manager.get_cat_services()
    return jsonify(dto)


@app.route('/fields/<string:category_name>/<string:service_name>', methods=['GET'])
def get_fields(category_name, service_name):
    dto = db_manager.get_fields(category_name, service_name)
    return jsonify(dto)


@app.route('/reset/<string:admin>', methods=['POST'])
def reset_dto(admin):
    # if admin == "admin":
    #     db.reset_dto()
    #     return jsonify({'message': 'Data reset successful'})
    return jsonify({'message': 'no access'})


if __name__ == '__main__':
    app.run()
