import json
from . import app
from .data_storage import manager, data, json_url
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    res = {picture["id"]: picture["pic_url"] for picture in data}
    return res, 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    manager_id = manager.checking_the_index(id)
    if manager_id is False:
        return "Not Found", 404
    return jsonify(data[manager_id])

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.get_json()
    if not new_picture:
        return {"Message": "Invalid input, no data provided"}, 400

    add_index = manager.add_index(new_picture["id"])
    if add_index is False:
        return {"Message": f"picture with id {new_picture['id']} already present"}, 302

    data.append(new_picture)
    return {"Message": "Picture created", "id": new_picture["id"]}, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    index = manager.checking_the_index(id)
    if index is False:
        return jsonify("The picture was not found"), 404
    our_data = data[index]
    get_data = request.get_json()
    for key in get_data.keys():
        our_data[key] = get_data[key]
    return 201


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if manager.checking_the_index(id) is False:
        return jsonify("The picture was not found"), 404
    manager.delete_index(id)
    return "", 204