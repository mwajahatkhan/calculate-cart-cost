from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

cart = []

HTML = """
<!doctype html>
<html lang="en">
<head>
  <title>Shopping Cart</title>
  <style>
    body {
      background: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      margin: 0;
      padding: 0;
    }
    .container {
      background: #fff;
      max-width: 600px;
      margin: 40px auto 0 auto;
      border-radius: 16px;
      box-shadow: 0 4px 24px rgba(0,0,0,0.12);
      padding: 32px 40px 40px 40px;
    }
    h2 {
      color: #ff6f61;
      text-align: center;
      margin-bottom: 24px;
    }
    form {
      display: flex;
      flex-direction: column;
      gap: 14px;
      margin-bottom: 32px;
      align-items: center;
    }
    input[type="text"], input[type="number"] {
      padding: 8px 12px;
      border: 1px solid #ddd;
      border-radius: 6px;
      font-size: 1rem;
      width: 220px;
      transition: border 0.2s;
    }
    input[type="text"]:focus, input[type="number"]:focus {
      border: 1.5px solid #ff6f61;
      outline: none;
    }
    input[type="submit"], .btn {
      background: #ff6f61;
      color: #fff;
      border: none;
      border-radius: 6px;
      padding: 6px 16px; /* Reduced size */
      font-size: 0.9rem; /* Reduced font size */
      font-weight: bold;
      cursor: pointer;
      margin-top: 8px;
      transition: background 0.2s;
    }
    input[type="submit"]:hover, .btn:hover {
      background: #ff9472;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
      background: #f9f9f9;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    th, td {
      padding: 10px 8px;
      text-align: center;
    }
    th {
      background: #ff9472;
      color: #fff;
      font-weight: 600;
    }
    tr:nth-child(even) {
      background: #ffe5d0;
    }
    tr:nth-child(odd) {
      background: #fff;
    }
    .totals {
      margin-top: 24px;
      text-align: right;
      font-size: 1.1rem;
      color: #333;
    }
    .actions {
      display: flex;
      justify-content: space-between;
      margin-top: 15px;
    }
    @media (max-width: 700px) {
      .container {
        padding: 18px 4vw 24px 4vw;
      }
      input[type="text"], input[type="number"] {
        width: 100%;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>Add items to Shopping Cart 🛒</h2>
    <form method="post" action="/">
      <div>
        <input type="text" name="name" placeholder="Item Name" required>
      </div>
      <div>
        <input type="number" step="0.01" name="price" placeholder="Price" required>
      </div>
      <div>
        <input type="number" name="quantity" placeholder="Quantity" required>
      </div>
      <input type="submit" value="Add Item">
    </form>
    <h2 style="margin-top:10px;">Cart Items</h2>
    <table>
      <tr>
        <th>Actions</th><th>S.No</th><th>Item Name</th><th>Price</th><th>Quantity</th><th>Subtotal</th>
      </tr>
      {% for item in cart_sorted %}
      <tr>
        <td>
          <form method="post" action="/remove/{{ loop.index0 }}" style="display:inline;">
            <button class="btn" type="submit">Remove</button>
          </form>
        </td>
        <td>{{ loop.index }}</td>
        <td>{{ item['name'] }}</td>
        <td>₹{{ '%.2f'|format(item['price']) }}</td>
        <td>{{ item['quantity'] }}</td>
        <td>₹{{ '%.2f'|format(item['price'] * item['quantity']) }}</td>
      </tr>
      {% endfor %}
      {% if cart_sorted|length == 0 %}
      <tr>
        <td colspan="6" style="color:#888;">No items in cart.</td>
      </tr>
      {% endif %}
    </table>
    <div class="totals">
      <p><b>Total Quantity:</b> {{ total_quantity }}</p>
      <p><b>Total Amount:</b> ₹{{ '%.2f'|format(total_cost) }}</p>
    </div>
    <div class="actions">
      <form method="post" action="/clear">
        <button class="btn" type="submit">Clear Cart</button>
      </form>
    </div>
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        quantity = int(request.form["quantity"])
        cart.append({"name": name, "price": price, "quantity": quantity})
        return redirect(url_for("index"))
    cart_sorted = sorted(cart, key=lambda x: x['name'].lower())
    total_cost = sum(item['price'] * item['quantity'] for item in cart_sorted)
    total_quantity = sum(item['quantity'] for item in cart_sorted)
    return render_template_string(
        HTML,
        cart_sorted=cart_sorted,
        total_cost=total_cost,
        total_quantity=total_quantity
    )

@app.route("/remove/<int:index>", methods=["POST"])
def remove_item(index):
    if 0 <= index < len(cart):
        cart.pop(index)
    return redirect(url_for("index"))

@app.route("/clear", methods=["POST"])
def clear_cart():
    cart.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
