from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

import streamlit as st


st.set_page_config(
    page_title="VendorHub Marketplace",
    page_icon="VH",
    layout="wide",
    initial_sidebar_state="expanded",
)


@dataclass
class Product:
    id: str
    vendor_id: str
    name: str
    category: str
    price: float
    description: str
    available: bool = True


@dataclass
class Vendor:
    id: str
    business_name: str
    category: str
    city: str
    contact_name: str
    email: str
    phone: str
    description: str
    status: str = "Pending review"
    products: list[Product] = field(default_factory=list)


def seed_vendors() -> list[Vendor]:
    vendors = [
        Vendor(
            id="vendor-1",
            business_name="Bright Basket Grocers",
            category="Food & Grocery",
            city="Austin",
            contact_name="Maya Chen",
            email="orders@brightbasket.example",
            phone="+1 555 0184",
            description="Fresh produce, pantry staples, and weekly household essentials.",
            status="Verified",
        ),
        Vendor(
            id="vendor-2",
            business_name="Northline Electronics",
            category="Electronics",
            city="Chicago",
            contact_name="Daniel Reed",
            email="sales@northline.example",
            phone="+1 555 0159",
            description="Phones, accessories, smart home devices, and repair supplies.",
            status="Verified",
        ),
        Vendor(
            id="vendor-3",
            business_name="Craft & Comfort Studio",
            category="Home & Lifestyle",
            city="Portland",
            contact_name="Ari Morgan",
            email="hello@craftcomfort.example",
            phone="+1 555 0127",
            description="Handmade home goods, decor, gifts, and seasonal bundles.",
            status="Verified",
        ),
    ]

    products = [
        Product("product-1", "vendor-1", "Weekly produce box", "Food & Grocery", 42.00, "A curated box of seasonal fruit and vegetables."),
        Product("product-2", "vendor-1", "Pantry refill kit", "Food & Grocery", 68.50, "Rice, pasta, spices, oils, and breakfast staples."),
        Product("product-3", "vendor-2", "Wireless charging stand", "Electronics", 29.99, "Fast charging stand for phones and earbuds."),
        Product("product-4", "vendor-2", "Smart security starter pack", "Electronics", 189.00, "Two cameras, a hub, and mobile setup support."),
        Product("product-5", "vendor-3", "Hand-poured candle set", "Home & Lifestyle", 36.00, "Three soy candles in warm, clean scents."),
        Product("product-6", "vendor-3", "Custom gift basket", "Home & Lifestyle", 75.00, "A personalized basket for holidays, birthdays, or corporate gifts."),
    ]

    by_id = {vendor.id: vendor for vendor in vendors}
    for product in products:
        by_id[product.vendor_id].products.append(product)

    return vendors


def ensure_state() -> None:
    if "vendors" not in st.session_state:
        st.session_state.vendors = seed_vendors()
    if "cart" not in st.session_state:
        st.session_state.cart = []
    if "requests" not in st.session_state:
        st.session_state.requests = []
    if "orders" not in st.session_state:
        st.session_state.orders = []


def all_products() -> list[Product]:
    return [
        product
        for vendor in st.session_state.vendors
        for product in vendor.products
        if product.available and vendor.status == "Verified"
    ]


def vendor_by_id(vendor_id: str) -> Vendor | None:
    return next((vendor for vendor in st.session_state.vendors if vendor.id == vendor_id), None)


def money(value: float) -> str:
    return f"${value:,.2f}"


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 1.35rem;
                padding-bottom: 2rem;
                max-width: 1180px;
            }
            .hero {
                border: 1px solid #d8dee8;
                border-radius: 8px;
                padding: clamp(1rem, 3vw, 2rem);
                background: linear-gradient(135deg, #f7fafc 0%, #eef6f3 52%, #fff8e6 100%);
                margin-bottom: 1rem;
            }
            .hero h1 {
                font-size: clamp(2rem, 5vw, 4.25rem);
                line-height: 1;
                margin: 0 0 .7rem 0;
                letter-spacing: 0;
                color: #17202a;
            }
            .hero p {
                max-width: 760px;
                font-size: 1.04rem;
                line-height: 1.65;
                color: #425466;
                margin: 0;
            }
            .metric-row {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: .75rem;
                margin: 1rem 0;
            }
            .stat {
                border: 1px solid #d8dee8;
                border-radius: 8px;
                padding: .85rem;
                background: #ffffff;
            }
            .stat span {
                display: block;
                color: #667085;
                font-size: .84rem;
            }
            .stat strong {
                display: block;
                color: #111827;
                font-size: 1.35rem;
                margin-top: .2rem;
            }
            .vendor-card {
                border: 1px solid #d8dee8;
                border-radius: 8px;
                padding: 1rem;
                background: #ffffff;
                min-height: 205px;
            }
            .vendor-card h3 {
                font-size: 1.05rem;
                margin: 0 0 .35rem 0;
                color: #17202a;
            }
            .vendor-card p {
                margin: .25rem 0;
                color: #475467;
                line-height: 1.45;
            }
            .tag {
                display: inline-flex;
                border: 1px solid #b7d5c8;
                border-radius: 999px;
                padding: .18rem .55rem;
                color: #1f5f46;
                background: #eef8f3;
                font-size: .78rem;
                margin-bottom: .5rem;
            }
            div[data-testid="stButton"] button {
                border-radius: 8px;
            }
            @media (max-width: 760px) {
                .metric-row {
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }
                .hero {
                    padding: 1rem;
                }
            }
            @media (max-width: 520px) {
                .metric-row {
                    grid-template-columns: 1fr;
                }
                .block-container {
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    products = all_products()
    verified_vendors = [vendor for vendor in st.session_state.vendors if vendor.status == "Verified"]
    categories = sorted({vendor.category for vendor in st.session_state.vendors})
    orders = st.session_state.orders

    st.markdown(
        """
        <section class="hero">
            <h1>VendorHub Marketplace</h1>
            <p>Discover registered vendors, request custom items or services, buy available products, and give local businesses a polished online presence from one responsive storefront.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="metric-row">
            <div class="stat"><span>Verified vendors</span><strong>{len(verified_vendors)}</strong></div>
            <div class="stat"><span>Available items</span><strong>{len(products)}</strong></div>
            <div class="stat"><span>Categories</span><strong>{len(categories)}</strong></div>
            <div class="stat"><span>Orders placed</span><strong>{len(orders)}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_marketplace() -> None:
    st.subheader("Shop Registered Vendors")
    products = all_products()
    categories = ["All categories", *sorted({product.category for product in products})]
    selected_category = st.selectbox("Category", categories, label_visibility="collapsed")
    search = st.text_input("Search products, vendors, or locations", placeholder="Search products, vendors, or locations")

    filtered_products = []
    for product in products:
        vendor = vendor_by_id(product.vendor_id)
        haystack = f"{product.name} {product.category} {product.description} {vendor.business_name if vendor else ''} {vendor.city if vendor else ''}".lower()
        matches_category = selected_category == "All categories" or product.category == selected_category
        matches_search = not search or search.lower() in haystack
        if matches_category and matches_search:
            filtered_products.append(product)

    if not filtered_products:
        st.info("No products match that search yet.")
        return

    for index in range(0, len(filtered_products), 3):
        columns = st.columns(3)
        for column, product in zip(columns, filtered_products[index : index + 3]):
            vendor = vendor_by_id(product.vendor_id)
            with column:
                st.markdown(
                    f"""
                    <div class="vendor-card">
                        <span class="tag">{product.category}</span>
                        <h3>{product.name}</h3>
                        <p>{product.description}</p>
                        <p><strong>{money(product.price)}</strong></p>
                        <p>{vendor.business_name if vendor else "Vendor"} · {vendor.city if vendor else ""}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("Add to cart", key=f"cart-{product.id}", use_container_width=True):
                    st.session_state.cart.append(product.id)
                    st.toast(f"{product.name} added to cart.")


def render_requests() -> None:
    st.subheader("Request Any Item or Service")
    verified_vendors = [vendor for vendor in st.session_state.vendors if vendor.status == "Verified"]
    vendor_options = ["Open request to all matching vendors", *[vendor.business_name for vendor in verified_vendors]]

    with st.form("request-form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            customer_name = st.text_input("Your name")
            customer_email = st.text_input("Email")
            item_name = st.text_input("What do you need?")
            category = st.selectbox("Category", sorted({vendor.category for vendor in st.session_state.vendors}))
        with col_b:
            preferred_vendor = st.selectbox("Preferred vendor", vendor_options)
            quantity = st.number_input("Quantity", min_value=1, value=1)
            budget = st.number_input("Budget", min_value=0.0, value=50.0, step=5.0)
            needed_by = st.date_input("Needed by")

        details = st.text_area("Details", placeholder="Include size, delivery location, timing, or special instructions.")
        submitted = st.form_submit_button("Send request", use_container_width=True)

    if submitted:
        missing = [label for label, value in {"name": customer_name, "email": customer_email, "item": item_name}.items() if not value.strip()]
        if missing:
            st.error("Please add your name, email, and requested item.")
        else:
            st.session_state.requests.append(
                {
                    "id": str(uuid4())[:8],
                    "customer_name": customer_name,
                    "customer_email": customer_email,
                    "item_name": item_name,
                    "category": category,
                    "preferred_vendor": preferred_vendor,
                    "quantity": int(quantity),
                    "budget": float(budget),
                    "needed_by": needed_by.isoformat(),
                    "details": details,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "status": "Open",
                }
            )
            st.success("Request sent. Vendors can now respond with availability and pricing.")

    if st.session_state.requests:
        st.divider()
        st.caption("Recent requests")
        for request in reversed(st.session_state.requests[-5:]):
            st.markdown(
                f"**{request['item_name']}** · {request['category']} · Qty {request['quantity']} · Budget {money(request['budget'])} · {request['status']}"
            )


def render_vendors() -> None:
    st.subheader("Vendor Directory")
    for index in range(0, len(st.session_state.vendors), 3):
        columns = st.columns(3)
        for column, vendor in zip(columns, st.session_state.vendors[index : index + 3]):
            with column:
                st.markdown(
                    f"""
                    <div class="vendor-card">
                        <span class="tag">{vendor.status}</span>
                        <h3>{vendor.business_name}</h3>
                        <p>{vendor.category} · {vendor.city}</p>
                        <p>{vendor.description}</p>
                        <p>{vendor.email}<br>{vendor.phone}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def render_vendor_registration() -> None:
    st.subheader("Register Your Vendor Business")
    st.caption("Create an online presence and make your products searchable to customers.")

    with st.form("vendor-registration", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            business_name = st.text_input("Business name")
            category = st.selectbox(
                "Business category",
                ["Food & Grocery", "Electronics", "Home & Lifestyle", "Health & Beauty", "Professional Services", "Fashion", "Other"],
            )
            city = st.text_input("City")
            contact_name = st.text_input("Contact person")
        with col_b:
            email = st.text_input("Business email")
            phone = st.text_input("Phone")
            first_product = st.text_input("First product or service")
            first_price = st.number_input("Starting price", min_value=0.0, value=25.0, step=5.0)

        description = st.text_area("Business description")
        product_description = st.text_area("Product or service description")
        submitted = st.form_submit_button("Register vendor", use_container_width=True)

    if submitted:
        required = [business_name, city, contact_name, email, phone, first_product]
        if any(not value.strip() for value in required):
            st.error("Please complete the required business and product fields.")
            return

        vendor_id = f"vendor-{uuid4()}"
        product = Product(
            id=f"product-{uuid4()}",
            vendor_id=vendor_id,
            name=first_product,
            category=category,
            price=float(first_price),
            description=product_description or "New vendor product or service.",
        )
        vendor = Vendor(
            id=vendor_id,
            business_name=business_name,
            category=category,
            city=city,
            contact_name=contact_name,
            email=email,
            phone=phone,
            description=description or "Vendor profile pending full description.",
            status="Pending review",
            products=[product],
        )
        st.session_state.vendors.append(vendor)
        st.success("Vendor registered. The profile is saved as pending review and ready for approval.")


def render_cart() -> None:
    st.subheader("Cart & Checkout")
    if not st.session_state.cart:
        st.info("Your cart is empty. Add products from the marketplace to begin checkout.")
        return

    product_lookup = {product.id: product for product in all_products()}
    cart_products = [product_lookup[product_id] for product_id in st.session_state.cart if product_id in product_lookup]
    total = sum(product.price for product in cart_products)

    for product in cart_products:
        vendor = vendor_by_id(product.vendor_id)
        st.write(f"**{product.name}** · {vendor.business_name if vendor else 'Vendor'} · {money(product.price)}")

    st.markdown(f"### Total: {money(total)}")

    with st.form("checkout-form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("Customer name")
            email = st.text_input("Email address")
        with col_b:
            fulfillment = st.selectbox("Fulfillment", ["Delivery", "Pickup", "Vendor will confirm"])
            payment = st.selectbox("Payment method", ["Card on delivery", "Bank transfer", "Cash on pickup"])
        address = st.text_area("Delivery or pickup details")
        submitted = st.form_submit_button("Place order", use_container_width=True)

    if submitted:
        if not name.strip() or not email.strip():
            st.error("Please add your name and email to place the order.")
            return

        order = {
            "id": str(uuid4())[:8].upper(),
            "customer": name,
            "email": email,
            "items": [product.name for product in cart_products],
            "total": total,
            "fulfillment": fulfillment,
            "payment": payment,
            "address": address,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": "Submitted",
        }
        st.session_state.orders.append(order)
        st.session_state.cart = []
        st.success(f"Order {order['id']} placed. Vendors will confirm availability and final fulfillment details.")


def render_admin_snapshot() -> None:
    st.subheader("Operations Snapshot")
    pending_vendors = [vendor for vendor in st.session_state.vendors if vendor.status == "Pending review"]
    open_requests = [request for request in st.session_state.requests if request["status"] == "Open"]

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Pending vendors", len(pending_vendors))
    col_b.metric("Open requests", len(open_requests))
    col_c.metric("Submitted orders", len(st.session_state.orders))

    if pending_vendors:
        st.caption("Pending vendor approvals")
        for vendor in pending_vendors:
            with st.expander(vendor.business_name):
                st.write(vendor.description)
                st.write(f"{vendor.contact_name} · {vendor.email} · {vendor.phone}")
                if st.button("Approve vendor", key=f"approve-{vendor.id}"):
                    vendor.status = "Verified"
                    st.success(f"{vendor.business_name} is now verified.")
                    st.rerun()

    if st.session_state.orders:
        st.caption("Recent orders")
        for order in reversed(st.session_state.orders[-5:]):
            st.write(f"**{order['id']}** · {order['customer']} · {money(order['total'])} · {order['status']}")


def main() -> None:
    ensure_state()
    inject_styles()
    render_header()

    with st.sidebar:
        st.title("VendorHub")
        st.write("Marketplace tools")
        st.metric("Cart items", len(st.session_state.cart))
        st.caption("This prototype keeps data in the browser session. Connect a database and payments provider before production use.")

    tabs = st.tabs(
        [
            "Marketplace",
            "Request Item",
            "Vendors",
            "Vendor Registration",
            "Cart",
            "Admin",
        ]
    )
    with tabs[0]:
        render_marketplace()
    with tabs[1]:
        render_requests()
    with tabs[2]:
        render_vendors()
    with tabs[3]:
        render_vendor_registration()
    with tabs[4]:
        render_cart()
    with tabs[5]:
        render_admin_snapshot()


if __name__ == "__main__":
    main()
