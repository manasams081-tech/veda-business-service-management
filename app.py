from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
from pathlib import Path
import json
import csv
import io
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "app" / "templates"),
    static_folder=str(BASE_DIR / "app" / "static"),
    static_url_path="/static",
)
app.secret_key = "veda-nexus-demo-secret-key"

DATA_FILES = {
    "services": DATA_DIR / "services.json",
    "programs": DATA_DIR / "programs.json",
    "customers": DATA_DIR / "customers.json",
    "inquiries": DATA_DIR / "inquiries.json",
}

DEFAULTS = {
    "services": [
        {"id": 1, "name": "Cloud Operations", "category": "Digital Services", "owner": "Platform Team", "status": "Active", "priority": "High", "description": "Cloud setup, monitoring and operational support."},
        {"id": 2, "name": "Data Analytics Studio", "category": "Digital Services", "owner": "Data Team", "status": "Active", "priority": "Medium", "description": "Business dashboards, analytics and reporting services."},
        {"id": 3, "name": "Managed Cyber Support", "category": "Technology", "owner": "Security Team", "status": "Active", "priority": "High", "description": "Security reviews, awareness and incident readiness support."},
        {"id": 4, "name": "Website Modernization", "category": "Technology", "owner": "Product Team", "status": "Planned", "priority": "Medium", "description": "Modern web experience planning and implementation."},
        {"id": 5, "name": "Automation Advisory", "category": "Consulting", "owner": "Solutions Team", "status": "Active", "priority": "Low", "description": "Process automation and productivity improvement advisory."},
    ],
    "programs": [
        {"id": 1, "name": "Python Engineering Accelerator", "type": "Training", "duration": "8 Weeks", "coordinator": "Learning Team", "status": "Running", "seats": 30},
        {"id": 2, "name": "Digital Internship Program", "type": "Internship", "duration": "12 Weeks", "coordinator": "Talent Team", "status": "Open", "seats": 50},
        {"id": 3, "name": "Business Automation Bootcamp", "type": "Training", "duration": "4 Weeks", "coordinator": "Solutions Team", "status": "Planned", "seats": 25},
        {"id": 4, "name": "Cloud Foundations", "type": "Technology Program", "duration": "6 Weeks", "coordinator": "Platform Team", "status": "Running", "seats": 40},
    ],
    "customers": [
        {"id": 1, "name": "Aster Retail Group", "email": "contact@aster.example", "phone": "+91 90000 10001", "segment": "Enterprise", "service": "Data Analytics Studio", "status": "Active"},
        {"id": 2, "name": "Nova Learning Hub", "email": "hello@nova.example", "phone": "+91 90000 10002", "segment": "Education", "service": "Python Engineering Accelerator", "status": "Active"},
        {"id": 3, "name": "BluePeak Logistics", "email": "ops@bluepeak.example", "phone": "+91 90000 10003", "segment": "SMB", "service": "Cloud Operations", "status": "Onboarding"},
        {"id": 4, "name": "Cedar Health Systems", "email": "it@cedar.example", "phone": "+91 90000 10004", "segment": "Enterprise", "service": "Managed Cyber Support", "status": "Active"},
        {"id": 5, "name": "Orbit Media Labs", "email": "team@orbit.example", "phone": "+91 90000 10005", "segment": "Startup", "service": "Website Modernization", "status": "Prospect"},
    ],
    "inquiries": [
        {"id": 1, "customer": "Aster Retail Group", "subject": "Dashboard enhancement", "type": "Service Request", "priority": "High", "status": "In Progress", "assignee": "Data Team", "created": "2026-10-02"},
        {"id": 2, "customer": "BluePeak Logistics", "subject": "Cloud migration consultation", "type": "Inquiry", "priority": "Medium", "status": "Open", "assignee": "Platform Team", "created": "2026-10-04"},
        {"id": 3, "customer": "Nova Learning Hub", "subject": "Internship cohort registration", "type": "Program", "priority": "Low", "status": "Resolved", "assignee": "Talent Team", "created": "2026-09-29"},
        {"id": 4, "customer": "Cedar Health Systems", "subject": "Security readiness review", "type": "Service Request", "priority": "High", "status": "Open", "assignee": "Security Team", "created": "2026-10-05"},
        {"id": 5, "customer": "Orbit Media Labs", "subject": "Website modernization quote", "type": "Inquiry", "priority": "Medium", "status": "Open", "assignee": "Product Team", "created": "2026-10-06"},
    ],
}


def ensure_data():
    for key, path in DATA_FILES.items():
        if not path.exists():
            path.write_text(json.dumps(DEFAULTS[key], indent=2), encoding="utf-8")


def load_data(key):
    ensure_data()
    try:
        return json.loads(DATA_FILES[key].read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return DEFAULTS[key].copy()


def save_data(key, records):
    DATA_FILES[key].write_text(json.dumps(records, indent=2), encoding="utf-8")


def next_id(records):
    return max((int(r.get("id", 0)) for r in records), default=0) + 1


def filtered(records, fields):
    query = request.args.get("q", "").strip().lower()
    status = request.args.get("status", "All").strip()
    if query:
        records = [r for r in records if any(query in str(r.get(field, "")).lower() for field in fields)]
    if status and status != "All":
        records = [r for r in records if str(r.get("status", "")) == status]
    return records


@app.context_processor
def inject_globals():
    return {"year": datetime.now().year, "active_page": request.endpoint}


@app.route("/")
def dashboard():
    services = load_data("services")
    programs = load_data("programs")
    customers = load_data("customers")
    inquiries = load_data("inquiries")
    stats = {
        "services": len(services),
        "active_services": sum(s.get("status") == "Active" for s in services),
        "programs": len(programs),
        "customers": len(customers),
        "open_inquiries": sum(i.get("status") in {"Open", "In Progress"} for i in inquiries),
        "high_priority": sum(i.get("priority") == "High" and i.get("status") != "Resolved" for i in inquiries),
    }
    recent = sorted(inquiries, key=lambda x: x.get("created", ""), reverse=True)[:5]
    return render_template("dashboard.html", stats=stats, recent=recent)


@app.route("/services", methods=["GET", "POST"])
def services():
    records = load_data("services")
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Service name is required.", "error")
        else:
            records.append({
                "id": next_id(records), "name": name,
                "category": request.form.get("category", "Technology").strip(),
                "owner": request.form.get("owner", "Unassigned").strip(),
                "status": request.form.get("status", "Active"),
                "priority": request.form.get("priority", "Medium"),
                "description": request.form.get("description", "").strip(),
            })
            save_data("services", records)
            flash("Service added successfully.", "success")
        return redirect(url_for("services"))
    records = filtered(records, ["name", "category", "owner", "description"])
    return render_template("services.html", services=records)


@app.route("/services/delete/<int:record_id>", methods=["POST"])
def delete_service(record_id):
    records = load_data("services")
    updated = [r for r in records if r.get("id") != record_id]
    save_data("services", updated)
    flash("Service removed.", "success")
    return redirect(url_for("services"))


@app.route("/programs", methods=["GET", "POST"])
def programs():
    records = load_data("programs")
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Program name is required.", "error")
        else:
            try:
                seats = max(1, int(request.form.get("seats", "1")))
            except ValueError:
                seats = 1
            records.append({
                "id": next_id(records), "name": name,
                "type": request.form.get("type", "Training"),
                "duration": request.form.get("duration", "4 Weeks").strip(),
                "coordinator": request.form.get("coordinator", "Unassigned").strip(),
                "status": request.form.get("status", "Planned"), "seats": seats,
            })
            save_data("programs", records)
            flash("Program added successfully.", "success")
        return redirect(url_for("programs"))
    records = filtered(records, ["name", "type", "coordinator", "duration"])
    return render_template("programs.html", programs=records)


@app.route("/customers", methods=["GET", "POST"])
def customers():
    records = load_data("customers")
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        if not name or "@" not in email:
            flash("Enter a customer name and a valid email.", "error")
        else:
            records.append({
                "id": next_id(records), "name": name, "email": email,
                "phone": request.form.get("phone", "").strip(),
                "segment": request.form.get("segment", "SMB"),
                "service": request.form.get("service", "General Support").strip(),
                "status": request.form.get("status", "Prospect"),
            })
            save_data("customers", records)
            flash("Customer added successfully.", "success")
        return redirect(url_for("customers"))
    records = filtered(records, ["name", "email", "segment", "service"])
    return render_template("customers.html", customers=records)


@app.route("/inquiries", methods=["GET", "POST"])
def inquiries():
    records = load_data("inquiries")
    if request.method == "POST":
        subject = request.form.get("subject", "").strip()
        customer = request.form.get("customer", "").strip()
        if not subject or not customer:
            flash("Customer and subject are required.", "error")
        else:
            records.append({
                "id": next_id(records), "customer": customer, "subject": subject,
                "type": request.form.get("type", "Inquiry"), "priority": request.form.get("priority", "Medium"),
                "status": request.form.get("status", "Open"), "assignee": request.form.get("assignee", "Unassigned").strip(),
                "created": datetime.now().strftime("%Y-%m-%d"),
            })
            save_data("inquiries", records)
            flash("Inquiry logged successfully.", "success")
        return redirect(url_for("inquiries"))
    records = filtered(records, ["customer", "subject", "type", "assignee"])
    return render_template("inquiries.html", inquiries=records)


@app.route("/inquiries/status/<int:record_id>", methods=["POST"])
def update_inquiry(record_id):
    records = load_data("inquiries")
    new_status = request.form.get("status", "Open")
    for record in records:
        if record.get("id") == record_id:
            record["status"] = new_status
            break
    save_data("inquiries", records)
    flash("Inquiry status updated.", "success")
    return redirect(url_for("inquiries"))


@app.route("/reports")
def reports():
    services = load_data("services")
    programs = load_data("programs")
    customers = load_data("customers")
    inquiries = load_data("inquiries")
    report = {
        "service_categories": {}, "program_types": {}, "customer_segments": {}, "inquiry_status": {}
    }
    for item in services:
        key = item.get("category", "Other"); report["service_categories"][key] = report["service_categories"].get(key, 0) + 1
    for item in programs:
        key = item.get("type", "Other"); report["program_types"][key] = report["program_types"].get(key, 0) + 1
    for item in customers:
        key = item.get("segment", "Other"); report["customer_segments"][key] = report["customer_segments"].get(key, 0) + 1
    for item in inquiries:
        key = item.get("status", "Other"); report["inquiry_status"][key] = report["inquiry_status"].get(key, 0) + 1
    return render_template("reports.html", report=report, totals={"services": len(services), "programs": len(programs), "customers": len(customers), "inquiries": len(inquiries)})


@app.route("/export/<key>.csv")
def export_csv(key):
    if key not in DATA_FILES:
        return "Unknown dataset", 404
    records = load_data(key)
    output = io.StringIO()
    if records:
        writer = csv.DictWriter(output, fieldnames=records[0].keys())
        writer.writeheader(); writer.writerows(records)
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": f"attachment; filename={key}.csv"})


@app.route("/api/summary")
def api_summary():
    return jsonify({
        "services": len(load_data("services")),
        "programs": len(load_data("programs")),
        "customers": len(load_data("customers")),
        "inquiries": len(load_data("inquiries")),
    })


@app.errorhandler(404)
def not_found(_):
    return render_template("error.html", code=404, message="The requested workspace page was not found."), 404


@app.errorhandler(500)
def server_error(_):
    return render_template("error.html", code=500, message="Something went wrong. Please try again."), 500


if __name__ == "__main__":
    ensure_data()
    app.run(debug=True, host="127.0.0.1", port=5000)
