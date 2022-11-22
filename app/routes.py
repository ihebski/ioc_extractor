from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import ReportForm
from app.models import Track, Ioc_Report
from werkzeug.utils import secure_filename
import PyPDF2
import hashlib
from ioc_finder import find_iocs
import os

# Accept only PDF files
ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    form = ReportForm()
    if form.validate_on_submit():
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = form.file.data
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            hash = sha256sum(f"{os.path.join(app.config['UPLOAD_FOLDER'])}/{filename}")
            if not Track.report_exists(hash=hash):
                Track.add_analyzed_file(filename, hash)
                return redirect(url_for("extract_ioc", hash=hash))
            else:
                flash(
                    message="The uploaded file has been already analyzed !",
                    category="danger",
                )
    context = {
        "files": Track.query.all(),
        "form": form,
    }
    return render_template("index.html", **context)


# Analyze uploaded file and extract IOC's
@app.route("/analyse_report/<hash>", methods=["GET", "POST"])
def extract_ioc(hash):
    empty = find_iocs("")
    iocs_list = []
    pages_list = []
    if Track.report_exists(hash):
        filename = Track.get_report_name(hash)
        # Read all pages in PDF file and extract IOC's one by one
        with open(
            f"{os.path.join(app.config['UPLOAD_FOLDER'])}/{filename}", "rb"
        ) as pdf_file:
            read_pdf = PyPDF2.PdfFileReader(pdf_file, strict=False)
            metadata = read_pdf.metadata
            number_of_pages = read_pdf.getNumPages()
            for page_number in range(number_of_pages):
                page = read_pdf.getPage(page_number)
                iocs = find_iocs(page.extractText())
                print(iocs)
                if not bool(iocs == empty):
                    iocs_list.append(iocs)
                    pages_list.append(page_number)
        # Save results to DB
        Ioc_Report.save_iocs(
            iocs_list, pages_list, metadata, Track.get_report_id_by_hash(hash)
        )
        # Render results
        context = {
            "iocs": iocs_list,
            "pages": pages_list,
            "report_name": filename,
            "metadata": metadata,
        }
        return render_template("details.html", **context)
    else:
        return render_template(
            "errors/404.html", title="Error occurred while processing your request!"
        )


# Get IOC details of previous analyzed file by file hash
@app.route("/details/<hash>", methods=["GET", "POST"])
def details(hash):
    if Track.report_exists(hash):
        iocs, pages, metadata = Ioc_Report.get_iocs_by_id(
            Track.get_report_id_by_hash(hash)
        )
        context = {
            "iocs": iocs,
            "pages": pages,
            "metadata": metadata,
            "report_name": Track.get_report_name(hash),
        }
        return render_template("details.html", **context)
    else:
        return render_template(
            "errors/404.html", title="Error occurred while processing your request!"
        )


# Delete file from DB
@app.route("/delete_file/<id>", methods=["GET", "POST"])
def delete(id):
    Track.delete_file(id)
    return redirect(url_for("index"))


# return sha256 hash of a specific file
def sha256sum(filename):
    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()
