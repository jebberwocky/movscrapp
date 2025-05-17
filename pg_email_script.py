import configparser
import pathlib
from pathlib import Path
import smtplib, ssl
from email.message import EmailMessage
import psycopg2
import pandas as pd
from datetime import datetime
import sys

# Path setup for configuration
path: Path = pathlib.Path(__file__).parent.resolve()
config = configparser.ConfigParser()
config.read(str(path) + '/default.ini')

# Environment settings
stage = config['env']['stage']
debug = config['env']['debug']

# Email settings
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = config['email']['sender']
receiver_email = config['email']['to']
password = config['email']['apppwd']

# PostgreSQL connection parameters
host = "db-postgresql-nyc3-11607-do-user-2845759-0.j.db.ondigitalocean.com"
pgport = 25060
dbname = "pokkoa"

# You'll need to add these to your config file or set them here
username = config['database']['username'] if 'database' in config and 'username' in config[
    'database'] else "YOUR_USERNAME"
password_db = config['database']['password'] if 'database' in config and 'password' in config[
    'database'] else "YOUR_PASSWORD"


def query_postgresql():
    """Query PostgreSQL and return results as a DataFrame"""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=host,
            port=pgport,
            dbname=dbname,
            user=username,
            password=password_db
        )

        # Execute query
        query = """
        SELECT *, ctid, to_timestamp(event_timestamp)
        FROM input
        ORDER BY event_timestamp DESC
        LIMIT 100;
        """

        print(f"Executing query: {query}")

        # Create a cursor and execute the query directly
        cursor = conn.cursor()
        cursor.execute(query)

        # Get column names from cursor description
        column_names = [desc[0] for desc in cursor.description]
        print(f"Column names: {column_names}")

        # Fetch all results
        results = cursor.fetchall()
        print(f"Number of rows retrieved: {len(results)}")

        # Create DataFrame manually
        df = pd.DataFrame(results, columns=column_names)

        # Close cursor and connection
        cursor.close()
        conn.close()

        return df
    except Exception as e:
        return f"Database error: {str(e)}"


def send_email(content, subject="PostgreSQL Query Results"):
    """Send email with the provided content"""
    msg = EmailMessage()

    # Add HTML formatting to make the table display nicely
    if isinstance(content, pd.DataFrame):
        html_content = f"""
        <html>
        <head>
            <style>
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
            </style>
        </head>
        <body>
            <h2>PostgreSQL Query Results</h2>
            <p>Query executed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            {content.to_html(index=False)}
        </body>
        </html>
        """
        msg.set_content(f"PostgreSQL Query Results\n\n{content.to_string(index=False)}")
        msg.add_alternative(html_content, subtype='html')
    else:
        # If content is an error message or something else
        msg.set_content(content)

    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Only sending email in production
    if stage == 'production' and config['email']['email']:
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email.split(","))
            return "Email sent successfully!"
        except Exception as e:
            return f"Failed to send email: {str(e)}"
    else:
        return "Email not sent (not in production or email disabled in config)"


if __name__ == '__main__':
    # Get PostgreSQL query results
    results = query_postgresql()

    # Debug: Print query results
    print("Query Results (Debug):")
    print(results)

    # Send results via email
    email_status = send_email(results, "PostgreSQL Query Results")

    print(email_status)