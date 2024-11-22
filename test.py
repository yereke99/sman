import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, recipient_email, subject, code):
    try:
        # Настройка сервера
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # Создание сообщения
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        body = f"Ваш код: {code}"
        message.attach(MIMEText(body, "plain"))
        
        # Подключение к серверу
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Отправка сообщения
        server.sendmail(sender_email, recipient_email, message.as_string())
        print("Email успешно отправлен!")
        
        # Закрытие соединения
        server.quit()
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")

# Пример использования
send_email(
    sender_email="hello@worldbonussystem.com",
    sender_password="m7427172M/",
    recipient_email="erkinbekly@gmail.com",
    subject="Ваш код подтверждения",
    code="123456"
)
