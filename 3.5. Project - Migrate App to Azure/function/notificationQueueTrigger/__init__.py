import os
import logging
from datetime import datetime

import azure.functions as func

import psycopg2
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


POSTGRES_URL = 'techconfdbserver.postgres.database.azure.com'
POSTGRES_DB = 'techconfdb'
POSTGRES_USER = 'dbadmin@techconfdbserver'
POSTGRES_PW = 'Postgres65432!'

ADMIN_EMAIL_ADDRESS: 'info@techconf.com'
SENDGRID_API_KEY = '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'


def main(msg: func.ServiceBusMessage):
    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info(
        '>>> Python ServiceBus queue trigger processed message: %s', notification_id)

    # TODO: Get connection to database
    connection = psycopg2.connect(
        host=POSTGRES_URL, database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PW)
    cursor = connection.cursor()
    logging.info('>>> Connected to Postgres Database on Azure')

    try:
        # TODO: Get notification message and subject from database using the notification_id
        cursor.execute(
            f'SELECT subject, message FROM notification where id = {notification_id};')
        notification = cursor.fetchone()
        logging.info(
            '>>> Got notification record from Postgres Database on Azure')

        # TODO: Get attendees email and name
        cursor.execute('SELECT first_name, last_name, email FROM attendee;')
        attendees = cursor.fetchall()
        logging.info(
            '>>> Got all attendee records from Postgres Database on Azure')

        # TODO: Loop through each attendee and send an email with a personalized subject
        notification_subject, notification_message = notification

        for attendee in attendees:
            first_name, last_name, email = attendee

            subject = f'{first_name} {last_name}: {notification_subject}'
            message = Mail(from_email=ADMIN_EMAIL_ADDRESS, to_emails=email,
                           subject=subject, html_content=f'<p>{notification_message}</p>')

            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)

            logging.info(
                f'>>> Message sent with subject: {subject} [code: {response.status_code}, header: {response.headers}, body: {response.body}]')

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        cursor.execute(
            f"UPDATE notification SET status = 'Notified {len(attendees)} attendees', completed_date = '{datetime.now}' WHERE id = {notification_id};")
        connection.commit()
        logging.info(
            '>>> Updated notification status to Postgres Database on Azure')
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        # TODO: Close connection
        cursor.close()
        connection.close()
