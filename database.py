import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "ai_serviceconnect"),
        port=int(os.getenv("DB_PORT", "3306"))
    )


def get_services():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()

    cursor.close()
    connection.close()

    return services


def get_providers():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            p.provider_id,
            u.name,
            p.service_type,
            p.experience_years,
            p.rating,
            p.location,
            p.availability,
            p.price_per_hour,
            p.verified
        FROM providers p
        JOIN users u
            ON p.user_id = u.user_id
    """

    cursor.execute(query)
    providers = cursor.fetchall()

    cursor.close()
    connection.close()

    return providers


def create_service_request(
    user_id,
    service_id,
    request_text,
    problem_description,
    location,
    urgency
):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO service_requests
        (
            user_id,
            service_id,
            request_text,
            problem_description,
            location,
            urgency
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        user_id,
        service_id,
        request_text,
        problem_description,
        location,
        urgency
    )

    cursor.execute(query, values)
    connection.commit()

    request_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return request_id
