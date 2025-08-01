from flask import Blueprint, request, jsonify
from extensions import db
from models import Order, Restaurant

order_bp = Blueprint("order", __name__)

@order_bp.route("/place", methods=["POST"])
def place_order():
    data = request.json
    new_order = Order(
        user_id=data["user_id"],
        restaurant_id=data["restaurant_id"],
        total_amount=data["total_amount"],
        status="pending"
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order placed successfully", "order_id": new_order.id})

# ✅ Fetch user's past orders
@order_bp.route("/myorders/<int:user_id>", methods=["GET"])
def get_user_orders(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    result = []
    for o in orders:
        restaurant = Restaurant.query.get(o.restaurant_id)
        result.append({
            "order_id": o.id,
            "restaurant": restaurant.name if restaurant else "Unknown",
            "total_amount": o.total_amount,
            "status": o.status
        })
    return jsonify(result)

@order_bp.route("/cancel/<int:order_id>", methods=["POST"])
def cancel_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404

    if order.status == "delivered":
        return jsonify({"message": "Cannot cancel delivered order"}), 400

    order.status = "cancelled"
    db.session.commit()
    return jsonify({"message": f"Order #{order.id} cancelled successfully"})

@order_bp.route("/update_status/<int:order_id>", methods=["POST"])
def update_order_status(order_id):
    data = request.get_json()
    new_status = data.get("status")

    order = Order.query.get(order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404

    order.status = new_status
    db.session.commit()
    return jsonify({"message": f"Order #{order.id} updated to {new_status}"})
