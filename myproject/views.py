from flask import Flask, render_template, request, redirect, url_for,Blueprint
from .models import db, Product, CartItem, Order

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.sqlite'
db.init_app(app)
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def list_products():
    search_query = request.args.get('q','')
    category = request.args.get('category', '')

    if search_query:
        products = Product.query.filter(Product.name.ilike(f'%{search_query}%')).all()

    elif category:
        products = Product.query.filter_by(category=category).all()
    
    else:
        products = Product.query.all()
    message = ""
    if not products:
        message = "Product not found"

    return render_template('nike.html', products=products, message=message, category=category)

@main_bp.route('/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return render_template('product_detail.html', product=product)
    return 'Product not found.'

@main_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if product:
        cart_item = CartItem(product=product)
        db.session.add(cart_item)
        db.session.commit()
        return redirect(url_for('main.view_cart'))
    return 'Product not found.'

@main_bp.route('/cart')
def view_cart():
    cart_items = CartItem.query.all()
    cart_items_dict = {}
    cart_items_count = {}

    for cart_item in cart_items:
        product_id = cart_item.product.id
        if product_id not in cart_items_dict:
            cart_items_dict[product_id] = cart_item
            cart_items_count[product_id] = 1
        else:
            cart_items_count[product_id] += 1

    total_price = 0  # Initialize total price

    for product_id, count in cart_items_count.items():
        cart_item = cart_items_dict[product_id]
        total_price += cart_item.product.price * count

    return render_template('cart.html', cart_items_dict=cart_items_dict, cart_items_count=cart_items_count, total_price=total_price)


@main_bp.route('/remove_from_cart/<int:cart_item_id>', methods=['POST'])
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get(cart_item_id)
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
    return redirect(url_for('main.view_cart'))

@main_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address_line1 = request.form['address_line1']
        address_line2 = request.form['address_line2']
        phone = request.form['phone']
        pin = request.form['pin']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']

        cart_items = CartItem.query.all()
        products = [cart_item.product for cart_item in cart_items]
        products_string = ', '.join(str(product) for product in products)
        

        order = Order(
            first_name=first_name,
            last_name=last_name,
            address_line1=address_line1,
            address_line2=address_line2,
            phone=phone,
            pin=pin,
            city=city,
            state=state,
            country=country,
            products_string=products_string
        )
        db.session.add(order)
        db.session.commit()

        for cart_item in cart_items:
            db.session.delete(cart_item)
        db.session.commit()

        return render_template('order_complete.html')
    else:
        cart_items = CartItem.query.all()
        products = [cart_item.product for cart_item in cart_items]
        cart_items_count = {}
        cart_items_dict = {}
        for cart_item in cart_items:
            product_id = cart_item.product.id
            if product_id in cart_items_count:
                cart_items_count[product_id] += 1
            else:
                cart_items_count[product_id] = 1
                cart_items_dict[product_id] = cart_item

        return render_template('formfill.html', products=products, cart_items=cart_items, cart_items_count=cart_items_count, cart_items_dict=cart_items_dict)

@main_bp.route('/db', methods=['GET'])
def view_orders():
    orders = Order.query.all()
    product = Product.query.all()
    return render_template('orders.html', orders=orders,product=product)


@main_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        price = request.form['price']
        image_file = request.form['image_file']
        image_file1 = request.form['image_file1']
        image_file2 = request.form['image_file2']
        image_file3 = request.form['image_file3']

        with app.app_context():
            product = Product(name=name, price=price, description=description, image_file=image_file, image_file1=image_file1, image_file2=image_file2, image_file3=image_file3, category=category)
            db.session.add(product)
            db.session.commit()

        return 'Product added successfully!'
    else:
        return render_template('add_product.html')


