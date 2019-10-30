import emails
from emails.template import JinjaTemplate
import logging
from pathlib import Path

from app import crud
from app.core import config
from app.db.session import db_session
from app.api.utils.io import get_predictions_csv


def send_email(email_to: str, subject_template="", html_template="", environment={}):
    assert config.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(config.EMAILS_FROM_NAME, config.EMAILS_FROM_EMAIL),
    )
    if "file" in environment:
        message.attach(data=environment["file"], filename=environment["file_name"])
    smtp_options = {"host": config.SMTP_HOST, "port": config.SMTP_PORT}
    if config.SMTP_TLS:
        smtp_options["tls"] = True
    if config.SMTP_USER:
        smtp_options["user"] = config.SMTP_USER
    if config.SMTP_PASSWORD:
        smtp_options["password"] = config.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_reset_password_email(email_to: str, email: str, token: str):
    project_name = config.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(config.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    if hasattr(token, "decode"):
        use_token = token.decode()
    else:
        use_token = token
    server_host = config.SERVER_HOST
    link = f"{server_host}/reset-password?token={use_token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": config.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": config.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email_to: str, username: str, password: str):
    project_name = config.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(config.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = config.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": config.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


def send_test_email(email_to: str):
    project_name = config.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(config.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": config.PROJECT_NAME, "email": email_to},
    )


def send_prediction_email(email_to: str, prediction_id: int):
    project_name = config.PROJECT_NAME
    subject = f"{project_name} - Predicció"

    prediction = crud.prediction.read(db_session, prediction_id=prediction_id)
    prediction_data = crud.prediction.read_data(
        db_session, prediction_id=prediction_id, limit=None, offset=None
    )
    csv_file = get_predictions_csv(
        prediction_data, undesired_attrs=["id", "prediction_id"]
    )

    with open(Path(config.EMAIL_TEMPLATES_DIR) / "prediction_result.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": config.PROJECT_NAME,
            "username": email_to,
            "file": csv_file,
            "file_name": "prediction_{}.csv".format(
                prediction.updated.strftime("%Y_%m_%d_%H_%M_%S")
            ),
        },
    )
