from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages, session
from data_manager import load_catalog, add_item, generate_item_id, update_item, delete_item, filtered_catalog, add_user_booking_requests, load_user_booking_requests, generate_booking_request_id, load_appointments, create_appointment, generate_appointment_id, decline_appointment_status, cancel_appointment_status, accept_appointment_status, complete_appointment_status
import time
import os
from dotenv import load_dotenv
from werkzeug.security import check_password_hash


load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = "static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = os.environ.get("SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("SECRET_KEY is not set")

admin_username = os.environ.get("ADMIN_USERNAME")
admin_password_hash = os.environ.get("ADMIN_PASSWORD_HASH")

if not admin_username or not admin_password_hash:
    raise RuntimeError("ADMIN_USERNAME and ADMIN_PASSWORD_HASH must be set")

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login_route():
    if request.method == "POST":
        attempted_username = request.form.get("username")
        attempted_password = request.form.get("password")
        next_page = request.args.get("next")

        if admin_username == attempted_username and check_password_hash(admin_password_hash, attempted_password):
            session["user"] = admin_username
            flash(f'Welcome {admin_username}!', 'success')
            return redirect(url_for(next_page) if next_page else url_for('admin_home_route'))

        flash('Invalid Credetials, please try again.', 'error')
    return render_template("admin/login.html")


@app.route("/")
@app.route("/admin_home")
def admin_home_route():
    if "user" in session:
        return render_template("admin/home.html")

    return redirect(url_for('admin_login_route', next='admin_home_route'))


@app.route("/admin_catalog")
def admin_catalog_route():
    if "user" in session:
        catalog = load_catalog()
        return render_template("admin/catalog.html", catalog=catalog)

    return redirect(url_for('admin_login_route', next='admin_catalog_route'))


@app.route("/admin_catalog/add_item", methods=["GET", "POST"])
def admin_add_route():
    if "user" not in session:
        return redirect(url_for('admin_login_route', next='admin_add_route')) 

    item_id, _ = generate_item_id()

    if request.method == "POST":
        item_name = request.form.get("item_name")
        item_price = request.form.get("item_price")
        item_category = request.form.get("item_category")
        item_image = request.files['item_image']
        item_description = request.form.get("item_description")

        filename = None

        if item_image and item_image.filename != '':
            filename = item_image.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            item_image.save(image_path)

        image_path = f"images/{filename}" if filename else None

        new_item = {
            "item_id": item_id,
            "name": item_name,
            "price": item_price,
            "category": item_category,
            "image": image_path,
            "description": item_description,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": "Hasn't been updated"
        }

        add_item(new_item)
        print("Saved")
        return redirect(url_for("admin_catalog_route"))
    return render_template("admin/add.html")


@app.route("/admin_catalog/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item_route(item_id):
    if "user" not in session:
        return redirect(url_for('admin_login_route', next='edit_item_route', item_id=item_id))
    else:
        catalog = load_catalog()

        item = next((item for item in catalog if item.get("item_id") == item_id), None)

        if request.method == "POST":
            item_name = request.form.get("item_name")
            item_price = request.form.get("item_price")
            item_category = request.form.get("item_category")
            item_image = request.files.get("item_image")
            item_description = request.form.get("item_description")
            created_at = item.get("created_at")
            updated_at = time.strftime("%Y-%m-%d %H:%M:%S")

            if item_image and item_image.filename != "":
                filename = item_image.filename
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                item_image.save(save_path)
                image_path = f"images/{filename}"

            else:
                image_path = item.get('image')

            update_item(item_id, item_name, item_price, item_category, image_path, item_description, created_at, updated_at)
            print("Item updated")
            return redirect(url_for("admin_catalog_route"))
        return render_template("admin/edit_catalog.html", item=item)


@app.route("/admin_catalog/delete/<int:item_id>")
def delete_item_route(item_id):
    if "user" not in session:
        return redirect(url_for('admin_login_route', next='delete_item_route', item_id=item_id))
    
    delete_item(item_id)
    return redirect(url_for("admin_catalog_route"))


@app.route("/admin_appointments", methods = ["GET"])
def admin_appointments_route():
    if "user" in session:
        appointments = load_appointments()
        return render_template("admin/appointments.html", appointments=appointments)

    return redirect(url_for('admin_login_route', next='admin_appointments_route'))


@app.route("/create_appointment", methods=["GET","POST"])
def admin_create_appointment_route():
    if "user" not in session:
        return redirect(url_for('admin_login_route', next='admin_create_appointment_route'))

    if request.method == "POST":
        appointment_id, _ = generate_appointment_id()
        selected_service = request.form.get("selected-service")
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        preffered_date = request.form.get("date")
        preffered_time = request.form.get("time")
        message = request.form.get("message")
        created_at = time.strftime("%Y-%m-%d %H:%M:%S")
        created_by = "admin"

        admin_created_appointment = {
            "appointment_id": appointment_id,
            "selected_service": selected_service,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "date": preffered_date,
            "time": preffered_time,
            "message": message,
            "created_at": created_at,
            "created_by": created_by
        }

        create_appointment(admin_created_appointment)
        return redirect(url_for("admin_appointments_route"))
    return render_template("admin/create_appointment.html")   


@app.route("/admin_appointments/cancel/<int:appointment_id>")
def admin_cancel_appointment_route(appointment_id):
    if "user" not in session:
        return redirect(url_for('admin_login_route', next='admin_cancel_appointment_route', appointment_id=appointment_id))

    if cancel_appointment_status(appointment_id):
        flash("Appointment cancelled.", "success")
    else:
        flash("Appointment not found.", "error")
    return redirect(url_for('admin_appointments_route'))


@app.route("/admin_appointments/complete/<int:appointment_id>")
def admin_complete_appointment_route(appointment_id):
    if "user" not in session:
        return redirect(url_for('admin_login_route', next='admin_complete_appointment_route', appointment_id=appointment_id))

    if complete_appointment_status(appointment_id):
        flash("Appointment completed.", "success")
    else:
        flash("Appointment not found.", "error")
    return redirect(url_for('admin_appointments_route'))


@app.route("/admin_booking_requests")
def admin_booking_requests_route():
    if "user" in session:
        booking_requests = load_user_booking_requests()
        return render_template("admin/booking_requests.html", booking_requests=booking_requests)

    return redirect(url_for('admin_login_route', next='admin_booking_requests_route'))


@app.route("/admin_booking_requests/history")
def admin_booking_requests_history_route():
    if "user" in session:
        booking_requests = load_user_booking_requests()
        return render_template('admin/booking_history.html', booking_requests=booking_requests)

    return redirect(url_for('admin_login_route', next='admin_booking_requests_history_route'))


@app.route("/admin_booking_requests/accept/<int:request_id>")
def admin_booking_request_accept_route(request_id):
    if "user" not in session:
        return redirect(url_for('admin_login_route', next='admin_booking_request_accept_route', request_id=request_id))
    user_booking_requests = load_user_booking_requests()
    booking_request = next((item for item in user_booking_requests if item.get("request_id") == request_id), None)
    if booking_request is None:
        flash("Booking request not found.", "error")
        return redirect(url_for("admin_booking_requests_route"))
    appointment_id, _ = generate_appointment_id()
    appointment_details = {
            "appointment_id": appointment_id,
            "request_id": booking_request["request_id"],
            "selected_service": booking_request["selected_service"],
            "full_name": booking_request["full_name"],
            "email": booking_request["email"],
            "phone": booking_request["phone"],
            "date": booking_request["date"],
            "time": booking_request["time"],
            "message": booking_request["message"],
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "created_by": booking_request["created_by"]
        }
    create_appointment(appointment_details)
    accept_appointment_status(request_id)
    flash("Booking request accepted.", "success")
    return redirect(url_for("admin_appointments_route"))


@app.route("/admin_booking_requests/decline/<int:request_id>")
def admin_booking_requests_decline_route(request_id):
    if "user" not in session:
        return redirect(url_for('admin_login_route', next='admin_booking_requests_decline_route', request_id=request_id))
    
    decline_appointment_status(request_id)
    return redirect(url_for('admin_booking_requests_route'))


@app.route("/admin_about")
def admin_about_route():
    if "user" in session:
        return render_template("admin/about.html")

    return redirect(url_for('admin_login_route', next='admin_about_route'))


@app.route("/admin_exit")
def exit_admin_route():
    if "user" in session:
        session.pop("user", None)
        return redirect(url_for("admin_login_route"))
    
    return redirect(url_for("admin_login_route"))


@app.route("/user_home")
def user_home_route():
    return render_template("user/home.html")


@app.route("/user_catalog")
def user_catalog_route():
    catalog = load_catalog()
    wigs = [item for item in catalog if item.get("category") == "Wigs"]
    hairstyles = [item for item in catalog if item.get("category") == "Hairstyles"]
    nails = [item for item in catalog if item.get("category") == "Nails"]
    return render_template("user/catalog.html", wigs=wigs, hairstyles=hairstyles, nails=nails)


@app.route("/user_catalog/<string:category>")
def filtered_catalog_route(category):
    items = filtered_catalog(category)
    name = category
    return render_template("user/filtered_catalog.html", items=items, name=name)


@app.route("/user_booking_requests", methods=["GET", "POST"])
def user_booking_requests_route():
    selected_service = request.args.get("service", "")
    
    if request.method == "POST":
        selected_service = request.form.get("selected-service")
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        preffered_date = request.form.get("date")
        preffered_time = request.form.get("time")
        message = request.form.get("message")

        request_id, _ = generate_booking_request_id()

        new_request = {
            "request_id": request_id,
            "status": "pending",
            "selected_service": selected_service,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "date": preffered_date,
            "time": preffered_time,
            "message": message,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "created_by": "user"
        }

        add_user_booking_requests(new_request)
        return redirect(url_for("user_booking_requests_route"))
    return render_template("user/booking.html", selected_service=selected_service)


@app.route("/user_about")
def user_about_route():
    return render_template("user/about.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
