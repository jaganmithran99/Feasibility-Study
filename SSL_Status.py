import ssl
import socket
from datetime import datetime
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend


def check_ssl_certificate_status(hostname, port):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
            cert_der = sslsock.getpeercert(binary_form=True)

            # Convert the binary certificate (DER) to PEM format
            cert_pem = ssl.DER_cert_to_PEM_cert(cert_der)

            # Load the certificate using cryptography
            cert = load_pem_x509_certificate(cert_pem.encode(), default_backend())

            # Extract details using cryptography methods
            cert_subject = cert.subject
            cert_issuer = cert.issuer
            cert_not_after = cert.not_valid_after
            cert_version = cert.version
            cert_serial_number = cert.serial_number

            # Get the public key
            cert_public_key = cert.public_key()

            if not cert_not_after:
                return "Certificate expiry info not available."

            # Get the current time to compare expiry
            current_time = datetime.utcnow()
            time_to_expiry = cert_not_after - current_time

            # Prepare the certificate status
            certificate_status = {
                "Subject": str(cert_subject),
                "Issuer": str(cert_issuer),
                "Serial Number": cert_serial_number,
                "Version": cert_version,
                "Public Key": str(cert_public_key),
                "Expiry Date": cert_not_after,
                "Days Until Expiry": time_to_expiry.days,
                "SSL/TLS Version": sslsock.version(),
            }

            return certificate_status


def print_ssl_status(status):
    print("\nSSL Certificate Status:")
    print(f"Subject: {status['Subject']}")
    print(f"Issuer: {status['Issuer']}")
    print(f"Version: {status['Version']}")
    print(f"Serial Number: {status['Serial Number']}")
    print(f"Public Key: {status['Public Key']}")
    print(f"Expiry Date: {status['Expiry Date']}")
    print(f"Days Until Expiry: {status['Days Until Expiry']} days")
    print(f"SSL/TLS Version: {status['SSL/TLS Version']}")


hostname = 'smartops-di05.ustdev.com'
port = 8443
status = check_ssl_certificate_status(hostname, port)
if isinstance(status, dict):
    print_ssl_status(status)
else:
    print(status)
