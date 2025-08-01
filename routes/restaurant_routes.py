from flask import Blueprint, request, jsonify
from extensions import db
from models import Restaurant, Dish

restaurant_bp = Blueprint("restaurant", __name__)

# Get all restaurants
@restaurant_bp.route("/", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([
        {"id": r.id, "name": r.name, "location": r.location, "rating": r.rating}
        for r in restaurants
    ])

# Get menu for restaurant
@restaurant_bp.route("/<int:restaurant_id>/menu", methods=["GET"])
def get_menu(restaurant_id):
    dishes = Dish.query.filter_by(restaurant_id=restaurant_id).all()
    return jsonify([
        {"id": d.id, "name": d.name, "price": d.price} for d in dishes
    ])

# ✅ Admin: Add restaurant
@restaurant_bp.route("/add", methods=["POST"])
def add_restaurant():
    data = request.json
    new_restaurant = Restaurant(
        name=data["name"],
        location=data["location"],
        rating=data.get("rating", 4.0)
    )
    db.session.add(new_restaurant)
    db.session.commit()
    return jsonify({"message": "Restaurant added successfully!"})

# ✅ Admin: Add dish
@restaurant_bp.route("/<int:restaurant_id>/add_dish", methods=["POST"])
def add_dish(restaurant_id):
    data = request.json
    new_dish = Dish(
        name=data["name"],
        price=data["price"],
        restaurant_id=restaurant_id
    )
    db.session.add(new_dish)
    db.session.commit()
    return jsonify({"message": "Dish added successfully!"})

# ✅ Admin: Delete restaurant
@restaurant_bp.route("/delete/<int:restaurant_id>", methods=["DELETE"])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return jsonify({"message": "Restaurant not found"}), 404
    Dish.query.filter_by(restaurant_id=restaurant_id).delete()
    db.session.delete(restaurant)
    db.session.commit()
    return jsonify({"message": "Restaurant deleted successfully!"})

# ✅ Admin: Delete dish
@restaurant_bp.route("/delete_dish/<int:dish_id>", methods=["DELETE"])
def delete_dish(dish_id):
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({"message": "Dish not found"}), 404
    db.session.delete(dish)
    db.session.commit()
    return jsonify({"message": "Dish deleted successfully!"})

# ✅ Add Dish
@restaurant_bp.route("/<int:restaurant_id>/menu/add", methods=["POST"])
def add_dish(restaurant_id):
    data = request.get_json()
    new_dish = Dish(
        name=data["name"],
        price=data["price"],
        image_url=data["image_url"],
        restaurant_id=restaurant_id
    )
    db.session.add(new_dish)
    db.session.commit()
    return jsonify({"message": "✅ Dish added successfully!"})

# ✅ Edit Dish
@restaurant_bp.route("/menu/edit/<int:dish_id>", methods=["PUT"])
def edit_dish(dish_id):
    data = request.get_json()
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({"message": "Dish not found"}), 404

    dish.name = data.get("name", dish.name)
    dish.price = data.get("price", dish.price)
    dish.image_url = data.get("image_url", dish.image_url)
    db.session.commit()
    return jsonify({"message": "✅ Dish updated successfully!"})

# ✅ Delete Dish
@restaurant_bp.route("/menu/delete/<int:dish_id>", methods=["DELETE"])
def delete_dish(dish_id):
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({"message": "Dish not found"}), 404
    db.session.delete(dish)
    db.session.commit()
    return jsonify({"message": "✅ Dish deleted successfully!"})
