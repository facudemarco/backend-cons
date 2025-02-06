from fastapi import FastAPI, HTTPException, Request, APIRouter
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter()

class FormData(BaseModel):
    nombre: str
    email: str
    telefono: str
    m2: str
    mensaje: str

def enviar_email(form_data: FormData):
    sender_email = "fac.demarco37@gmail.com"
    sender_password = "ifoc prlz usgx mvno"
    receiver_email = "fac.demarco37@gmail.com"
    subject = f"Nuevo mensaje de contacto desde la Web de {form_data.nombre}"
    body = f"Nombre: {form_data.nombre}\nEmail: {form_data.email}\nTeléfono: {form_data.telefono}\nMetros cuadrados: {form_data.m2}\nMensaje: {form_data.mensaje}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        raise HTTPException(status_code=500, detail="Error al enviar el correo")

@router.post("/send-email")
async def send_email(form_data: FormData):
    enviar_email(form_data)
    return {"message": "Formulario enviado exitosamente"}
