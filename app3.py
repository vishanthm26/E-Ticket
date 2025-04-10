import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image
from fpdf import FPDF
import random
import datetime
import base64

# ---------- Page Config ----------
st.set_page_config(page_title="Stylish Transit E-Ticket", page_icon="🚌", layout="centered")

# ---------- Styles ----------
st.markdown("""
    <style>
        body {
            background-color: #f5f5f5;
        }
        .ticket-box {
            background: linear-gradient(135deg, #b2fefa, #edb4f3, #ccf3c0);
            background-image: url('https://cdn.pixabay.com/photo/2018/03/11/18/05/traffic-3219239_1280.jpg');
            background-size: cover;
            background-position: center;
            padding: 2rem;
            width: 520px;
            margin: auto;
            border-radius: 25px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
            position: relative;
            color: #000;
            font-family: 'Segoe UI', sans-serif;
        }
        .ticket-box h1 {
            text-align: center;
            font-size: 30px;
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .ticket-box h2 {
            text-align: center;
            font-size: 24px;
            color: #000;
            font-weight: bold;
        }
        .ticket-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }
        .fare-box {
            font-size: 20px;
            font-weight: bold;
            color: green;
            text-align: center;
            margin-top: 1rem;
        }
        .route-button {
            position: absolute;
            bottom: 1rem;
            left: 1rem;
            background-color: #1d3557;
            color: white;
            padding: 0.4rem 0.8rem;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            font-size: 14px;
        }
        .qr-box {
            position: absolute;
            top: 1.5rem;
            right: 1rem;
            text-align: center;
        }
        .fare-button {
            background-color: #e76f51;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 8px;
            margin-top: 10px;
            cursor: pointer;
            font-weight: bold;
        }
        .bus-icon {
            position: absolute;
            top: 1rem;
            left: 1rem;
            width: 40px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Helper Functions ----------
def generate_qr(data):
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return Image.open(buffer), buffer.getvalue()

def create_pdf(ticket_details, qr_bytes, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in ticket_details.split("\n"):
        line = line.replace("₹", "Rs.")
        pdf.cell(200, 10, txt=line.encode("latin-1", "replace").decode("latin-1"), ln=True)
    qr_file = "temp_qr.png"
    with open(qr_file, "wb") as f:
        f.write(qr_bytes)
    pdf.image(qr_file, x=150, y=10, w=40)
    pdf.output(filename)

# ---------- Input Form ----------
st.title("🎟️ Stylish Smart Transit E-Ticket")

with st.form("ticket_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        booking_date = st.date_input("📅 Date", datetime.date.today())
    with col2:
        num_passengers = st.number_input("👥 No. of Passengers", min_value=1, max_value=10, value=1)
    with col3:
        name = st.text_input("👤 Passenger Name")

    source = st.text_input("🚌 Source")
    destination = st.text_input("📍 Destination")

    submit = st.form_submit_button("Generate Ticket")

# ---------- Ticket Logic ----------
if submit:
    if all([name.strip(), source.strip(), destination.strip()]):
        fare = random.randint(15, 30) * num_passengers
        bus_number = f"BUS-{random.randint(100,999)}"
        seat_number = f"S{random.randint(1,50)}"
        expiration = datetime.datetime.now() + datetime.timedelta(minutes=15)
        expiration_str = expiration.strftime("%H:%M:%S")

        qr_data_payment = f"Payment for Rs.{fare} - {name}"
        qr_img_payment, qr_bytes_payment = generate_qr(qr_data_payment)

        qr_data_ticket = f"Download Ticket for {name}"
        qr_img_ticket, qr_bytes_ticket = generate_qr(qr_data_ticket)

        st.markdown(f"""
            <div class='ticket-box'>
                <img class='bus-icon' src='https://cdn-icons-png.flaticon.com/512/1670/1670865.png' />
                <a class='route-button' href='https://your-route-optimizer-link.com' target='_blank'>View Routes</a>
                <div class='qr-box'>
                    <img src='data:image/png;base64,{base64.b64encode(qr_bytes_payment).decode()}' width='100' /><br/>
                    <button class='fare-button'>Rs.{fare} - Click to Pay</button>
                    <p style='color:green; font-weight:bold;'>✔️ Payment Done</p>
                    <img src='data:image/png;base64,{base64.b64encode(qr_bytes_ticket).decode()}' width='100' /><br/>
                    <small>Scan to Download</small>
                </div>
                <h1>🎉 Happy Journey!</h1>
                <h2>🚌 E-Ticket</h2>
                <div class='ticket-row'><b>Date:</b> {booking_date}</div>
                <div class='ticket-row'><b>Passenger:</b> {name}</div>
                <div class='ticket-row'><b>Bus No:</b> {bus_number}</div>
                <div class='ticket-row'><b>Seat No:</b> {seat_number}</div>
                <div class='ticket-row'><b>Passengers:</b> {num_passengers}</div>
                <div class='ticket-row'><b>From:</b> {source}</div>
                <div class='ticket-row'><b>To:</b> {destination}</div>
                <div class='fare-box'>Ticket Valid Until: {expiration_str}</div>
            </div>
        """, unsafe_allow_html=True)

        # PDF generation
        ticket_text = f"""
E-Ticket Receipt
------------------
Date: {booking_date}
Passenger Name: {name}
Bus Number: {bus_number}
Seat Number: {seat_number}
Number of Passengers: {num_passengers}
From: {source}
To: {destination}
Fare: Rs.{fare}
Status: Paid
Valid Until: {expiration_str}
        """
        pdf_filename = f"ticket_{name}.pdf"
        create_pdf(ticket_text, qr_bytes_ticket, pdf_filename)

        with open(pdf_filename, "rb") as f:
            st.download_button("📄 Download PDF Ticket", f, file_name=pdf_filename, mime="application/pdf")
    else:
        st.error("⚠️ Please fill in all fields before generating your ticket.")
