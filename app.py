# Flask Booking Management System
# This application manages a service booking system with admin and user interfaces
# Supports catalog management, booking requests, and appointment scheduling

from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages, session
import time
import os
from dotenv import load_dotenv
from werkzeug.security import check_password_hash
from models.catalog import load_catalog, add_item, load_filtered_catalog, update_item_details, delete_item
from models.bookings import booking_requests_table, create_booking_request, load_user_booking_requests, load_specific_user_booking_request, update_user_booking_request_status
from models.appointments import appointments_table, load_appointments, create_appointment, cancelled_appointment, completed_appointment


# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Configure file upload directory for catalog item images
UPLOAD_FOLDER = "static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = os.environ.get("SECRET_KEY")

# Ensure SECRET_KEY is configured for session management
if not app.secret_key:
    raise RuntimeError("SECRET_KEY is not set")

# Load admin credentials from environment variables
admin_username = os.environ.get("ADMIN_USERNAME")
admin_password_hash = os.environ.get("ADMIN_PASSWORD_HASH")

# Validate admin credentials are configured
if not admin_username or not admin_password_hash:
    raise RuntimeError("ADMIN_USERNAME and ADMIN_PASSWORD_HASH must be set")

# Initialize database tables for bookings and appointments
booking_requests_table()
appointments_table()

# ========== ADMIN ROUTES ==========

# Admin login route - handles authentication
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login_route():
    if request.method == "POST":
        # Retrieve login credentials from form
        attempted_username = request.form.get("username")
        attempted_password = request.form.get("password")
        next_page = request.args.get("next")

        # Validate credentials against admin credentials
        if admin_username == attempted_username and check_password_hash(admin_password_hash, attempted_password):
            session["user"] = admin_username
            flash(f'Welcome {admin_username}!', 'success')
            # Redirect to requested page or admin home
            return redirect(url_for(next_page) if next_page else url_for('admin_home_route'))

        flash('Invalid Credetials, please try again.', 'error')
    return render_template("admin/login.html")


# Admin home route - displays main admin dashboard
@app.route("/admin_home")
def admin_home_route():
    # Verify admin is logged in
    if "user" in session:
        return render_template("admin/home.html")

    return redirect(url_for('admin_login_route', next='admin_home_route'))


# Admin catalog route - displays all catalog items
@app.route("/admin_catalog")
def admin_catalog_route():
    if "user" in session:
        catalog = load_catalog()
        return render_template("admin/catalog.html", catalog=catalog)

    return redirect(url_for('admin_login_route', next='admin_catalog_route'))


# Add new catalog item route - allows admin to create new service offerings
@app.route("/admin_catalog/add_item", methods=["GET", "POST"])
def admin_add_route():
    if "user" not in session:
        return redirect(url_for('admin_login_route', next='admin_add_route')) 

    if request.method == "POST":
        # Collect item details from form
        item_name = request.form.get("item_name")
        item_price = request.form.get("item_price")
        item_category = request.form.get("item_category")
        item_image = request.files['item_image']
        item_description = request.form.get("item_description")
        item_created_at = time.strftime("%Y-%m-%d %H:%M:%S")
        item_updated_at = "Not updated yet"

        # Validate image file is provided
        if not item_image or item_image.filename == '':
            flash("Please upload an image for the catalog item.", "error")
            return render_template("admin/add.html")

        # Save image to static/images directory
        filename = item_image.filename
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        item_image.save(image_path)
        image_path = f"images/{filename}"

        # Add item to catalog database
        add_item(item_name, item_price, item_category, image_path, item_description, item_created_at, item_updated_at)
        print("Saved")
        return redirect(url_for("admin_catalog_route"))
    return render_template("admin/add.html")


# Edit catalog item route - allows admin to update item details
@app.route("/admin_catalog/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item_route(item_id):
    if "user" not in session:
        return redirect(url_for('admin_login_route', next='edit_item_route', item_id=item_id))
    else:
        catalog = load_catalog()
        # Find the specific item to edit
        item = next((item for item in catalog if item.get("item_id") == item_id), None)

        if request.method == "POST":
            # Collect updated item details
            item_name = request.form.get("item_name")
            item_price = request.form.get("item_price")
            item_category = request.form.get("item_category")
            item_image = request.files.get("item_image")
            item_description = request.form.get("item_description")
            created_at = item.get("created_at")
            updated_at = time.strftime("%Y-%m-%d %H:%M:%S")

            # Handle image update if new image is provided
            if item_image and item_image.filename != "":
                filename = item_image.filename
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                item_image.save(save_path)
                image_path = f"images/{filename}"
            else:
                # Keep existing image if no new image provided
                image_path = item.get("image")

            # Update item in database
            update_item_details(item_id, item_name, item_price, item_category, image_path, item_description, created_at, updated_at)
            print("Item updated")
            return redirect(url_for("admin_catalog_route"))
        return render_template("admin/edit_catalog.html", item=item)


# Delete catalog item route - removes item from catalog
@app.route("/admin_catalog/delete/<int:item_id>")
def delete_item_route(item_id):
    if "user" not in session:
        return redirect(url_for('admin_login_route', next='delete_item_route', item_id=item_id))
    
    # Remove item from database
    delete_item(item_id)
    return redirect(url_for("admin_catalog_route"))


# Admin appointments route - displays all scheduled appointments
@app.route("/admin_appointments", methods = ["GET"])
def admin_appointments_route():
    if "user" in session:
        appointments = load_appointments()
        return render_template("admin/appointments.html", appointments=appointments)

    return redirect(url_for('admin_login_route', next='admin_appointments_route'))


# Create appointment route - allows admin to manually create appointments
@app.route("/admin_create_appointment", methods=["GET","POST"])
def admin_create_appointment_route():
    if "user" not in session:
        return redirect(url_for('admin_login_route', next='admin_create_appointment_route'))

    if request.method == "POST":
        # Collect appointment details from form
        selected_service = request.form.get("selected-service")
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        preffered_date = request.form.get("date")
        preffered_time = request.form.get("time")
        message = request.form.get("message")
        created_at = time.strftime("%Y-%m-%d %H:%M:%S")
        created_by = "admin"

        # Create appointment in database
        create_appointment(
            None,
            selected_service,
            full_name,
            email,
            phone,
            preffered_date,
            preffered_time,
            message,
            created_at,
            created_by,
        )
        return redirect(url_for("admin_appointments_route"))
    return render_template("admin/create_appointment.html")   


# Cancel appointment route - marks appointment as cancelled
@app.route("/admin_appointments/cancel/<int:appointment_id>")
def admin_cancel_appointment_route(appointment_id):
    if "user" not in session:
        return redirect(url_for('admin_login_route', next='admin_cancel_appointment_route', appointment_id=appointment_id))

    # Find appointment by ID
    appointment = next((item for item in load_appointments() if item.get("appointment_id") == appointment_id), None)
    if appointment is None:
        flash("Appointment not found.", "error")
        return redirect(url_for('admin_appointments_route'))

    # Cancel the appointment
    cancelled_appointment(appointment_id, appointment.get("request_id"))
    flash("Appointment cancelled.", "success")
    return redirect(url_for('admin_appointments_route'))


# Complete appointment route - marks appointment as completed
@app.route("/admin_appointments/complete/<int:appointment_id>")
def admin_complete_appointment_route(appointment_id):
    if "user" not in session:
        return redirect(url_for('admin_login_route', next='admin_complete_appointment_route', appointment_id=appointment_id))

    # Find appointment by ID
    appointment = next((item for item in load_appointments() if item.get("appointment_id") == appointment_id), None)
    if appointment is None:
        flash("Appointment not found.", "error")
        return redirect(url_for('admin_appointments_route'))

    # Mark appointment as completed
    completed_appointment(appointment_id, appointment.get("request_id"))
    flash("Appointment completed.", "success")
    return redirect(url_for('admin_appointments_route'))


# Admin booking requests route - displays pending booking requests
@app.route("/admin_booking_requests")
def admin_booking_requests_route():
    if "user" in session:
        booking_requests = load_user_booking_requests()
        return render_template("admin/booking_requests.html", booking_requests=booking_requests)

    return redirect(url_for('admin_login_route', next='admin_booking_requests_route'))


# Booking history route - displays historical booking requests
@app.route("/admin_booking_requests/history")
def admin_booking_requests_history_route():
    if "user" in session:
        booking_requests = load_user_booking_requests()
        return render_template('admin/booking_history.html', booking_requests=booking_requests)

    return redirect(url_for('admin_login_route', next='admin_booking_requests_history_route'))


# Accept booking request route - converts booking request to appointment
@app.route("/admin_booking_requests/accept/<int:request_id>")
def admin_booking_request_accept_route(request_id):
    if "user" not in session:
        return redirect(url_for('admin_login_route', next='admin_booking_request_accept_route', request_id=request_id))
    
    # Load the specific booking request
    booking_request = load_specific_user_booking_request(request_id)
    if booking_request is None:
        flash("Booking request not found.", "error")
        return redirect(url_for("admin_booking_requests_route"))

    # Create appointment from booking request details
    create_appointment(
        booking_request["request_id"],
        booking_request["selected_service"],
        booking_request["full_name"],
        booking_request["email"],
        booking_request["phone"],
        booking_request["date"],
        booking_request["time"],
        booking_request["message"],
        time.strftime("%Y-%m-%d %H:%M:%S"),
        booking_request["created_by"],
    )
    flash("Booking request accepted.", "success")
    return redirect(url_for("admin_appointments_route"))


# Decline booking request route - rejects booking request
@app.route("/admin_booking_requests/decline/<int:request_id>")
def admin_booking_requests_decline_route(request_id):
    if "user" not in session:
        return redirect(url_for('admin_login_route', next='admin_booking_requests_decline_route', request_id=request_id))
    
    # Update booking request status to declined
    if update_user_booking_request_status(request_id, "Declined"):
        flash("Booking request declined.", "success")
    else:
        flash("Booking request not found.", "error")
    return redirect(url_for('admin_booking_requests_route'))


# Admin about route - displays admin information page
@app.route("/admin_about")
def admin_about_route():
    if "user" in session:
        return render_template("admin/about.html")

    return redirect(url_for('admin_login_route', next='admin_about_route'))


# Admin logout route - logs out admin and clears session
@app.route("/admin_exit")
def exit_admin_route():
    if "user" in session:
        # Clear user session
        session.pop("user", None)
        return redirect(url_for("admin_login_route"))
    
    return redirect(url_for("admin_login_route"))


# ========== USER ROUTES ==========

# User home route - displays main user page
@app.route("/")
@app.route("/user_home")
def user_home_route():
    return render_template("user/home.html")


# User catalog route - displays all services grouped by category
@app.route("/user_catalog")
def user_catalog_route():
    catalog = load_catalog()
    # Organize services by category
    wigs = [item for item in catalog if item.get("category") == "Wigs"]
    hairstyles = [item for item in catalog if item.get("category") == "Hairstyles"]
    nails = [item for item in catalog if item.get("category") == "Nails"]
    return render_template("user/catalog.html", wigs=wigs, hairstyles=hairstyles, nails=nails)


# Filtered catalog route - displays services for specific category
@app.route("/user_catalog/<string:category>")
def filtered_catalog_route(category):
    # Load and display services for selected category
    filtered_catalog = load_filtered_catalog(category)
    name = category
    return render_template("user/filtered_catalog.html", items=filtered_catalog, name=name)


# User booking request route - allows users to submit booking requests
@app.route("/user_booking_requests", methods=["GET", "POST"])
def user_booking_requests_route():
    # Get pre-selected service if provided
    selected_service = request.args.get("service", "")
    
    if request.method == "POST":
        # Collect booking details from form
        selected_service = request.form.get("selected-service")
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        preferred_date = request.form.get("date")
        preferred_time = request.form.get("time")
        message = request.form.get("message")

        # Create booking request in database
        create_booking_request("Pending", selected_service, full_name, email, phone, preferred_date, preferred_time, message, time.strftime("%Y-%m-%d %H:%M:%S"), "user")

        return redirect(url_for("user_booking_requests_route"))
    return render_template("user/booking.html", selected_service=selected_service)


# User about route - displays user information page
@app.route("/user_about")
def user_about_route():
    return render_template("user/about.html")


# ========== APPLICATION ENTRY POINT ==========

if __name__ == "__main__":
    # Run Flask application on specified port (default: 5000)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
