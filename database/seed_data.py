import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from extensions import db, bcrypt
from models import User, Restaurant, Dish

app = create_app()

with app.app_context():
    print("🔄 Resetting database...")
    db.drop_all()
    db.create_all()

    # ✅ Admin User
    admin_password = bcrypt.generate_password_hash("admin123").decode("utf-8")
    admin_user = User(name="Admin", email="admin@dinedash.com", password=admin_password, role="admin")
    db.session.add(admin_user)

    # ✅ Restaurants
    restaurants = [
        Restaurant(
            name="Spice Villa",
            location="Mumbai, India",
            rating=4.7,
            category="Indian",
            image_url="/static/images/restaurants/spice_villa.jpg"
        ),
        Restaurant(
            name="Pasta Palace",
            location="Rome, Italy",
            rating=4.6,
            category="Italian",
            image_url="/static/images/restaurants/pasta_palace.jpg"
        ),
        Restaurant(
            name="Dragon Wok",
            location="Beijing, China",
            rating=4.5,
            category="Chinese",
            image_url="/static/images/restaurants/dragon_wok.jpg"
        )
    ]
    db.session.add_all(restaurants)
    db.session.commit()

    # ✅ Dishes with Realistic Indian Pricing
    dishes = [
        # 🇮🇳 Indian
        Dish(name="Butter Chicken", price=299.00, image_url="/static/images/dishes/butter_chicken.jpg", restaurant_id=restaurants[0].id),
        Dish(name="Paneer Tikka", price=249.00, image_url="/static/images/dishes/paneer_tikka.jpg", restaurant_id=restaurants[0].id),
        Dish(name="Hyderabadi Biryani", price=349.00, image_url="/static/images/dishes/biryani.jpg", restaurant_id=restaurants[0].id),
        Dish(name="Gulab Jamun (2 pcs)", price=99.00, image_url="/static/images/dishes/gulab_jamun.jpg", restaurant_id=restaurants[0].id),

        # 🇮🇹 Italian
        Dish(name="Margherita Pizza", price=399.00, image_url="/static/images/dishes/margherita_pizza.jpg", restaurant_id=restaurants[1].id),
        Dish(name="Pasta Alfredo", price=449.00, image_url="/static/images/dishes/pasta_alfredo.jpg", restaurant_id=restaurants[1].id),
        Dish(name="Tiramisu", price=199.00, image_url="/static/images/dishes/tiramisu.jpg", restaurant_id=restaurants[1].id),
        Dish(name="Lasagna", price=499.00, image_url="/static/images/dishes/lasagna.jpg", restaurant_id=restaurants[1].id),

        # 🇨🇳 Chinese
        Dish(name="Kung Pao Chicken", price=329.00, image_url="/static/images/dishes/kung_pao.jpg", restaurant_id=restaurants[2].id),
        Dish(name="Dim Sum (6 pcs)", price=259.00, image_url="/static/images/dishes/dim_sum.jpg", restaurant_id=restaurants[2].id),
        Dish(name="Sweet & Sour Pork", price=369.00, image_url="/static/images/dishes/sweet_sour_pork.jpg", restaurant_id=restaurants[2].id),
        Dish(name="Veg Fried Rice", price=199.00, image_url="/static/images/dishes/fried_rice.jpg", restaurant_id=restaurants[2].id),
    ]

    db.session.add_all(dishes)
    db.session.commit()

    print("✅ Sample data inserted with REAL Indian pricing!")
    print("🔑 Admin Login: admin@dinedash.com | Password: admin123")
