import ssl
import socket
from datetime import datetime
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend


def check_ssl_certificate_status(hostname, port=8443):
    """
    Check SSL certificate details and return certificate expiration info.
    """
    # Establish an SSL connection
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
            # Retrieve the raw certificate in binary (DER) format
            cert_der = sslsock.getpeercert(binary_form=True)

            # Convert the binary certificate (DER) to PEM format
            cert_pem = ssl.DER_cert_to_PEM_cert(cert_der)

            # Load the certificate using cryptography
            cert = load_pem_x509_certificate(cert_pem.encode(), default_backend())

            # Extract the expiration date of the certificate
            cert_not_after = cert.not_valid_after

            # Get the current time
            current_time = datetime.utcnow()

            # Calculate the time remaining until the certificate expires
            time_to_expiry = cert_not_after - current_time
            days_until_expiry = time_to_expiry.days

            return {
                "hostname": hostname,
                "expiry_date": cert_not_after,
                "days_until_expiry": days_until_expiry
            }


def print_certificates_expiring_soon(hostname, days_threshold):
    print(f"Checking certificate for {hostname} expiring in the next {days_threshold} days...\n")

    status = check_ssl_certificate_status(hostname)

    if status['days_until_expiry'] <= days_threshold:
        print(f"Host: {status['hostname']}")
        print(f"  Expiry Date: {status['expiry_date']}")
        print(f"  Days Until Expiry: {status['days_until_expiry']} days\n")
    else:
        print(f"The certificate for {hostname} is not expiring within the next {days_threshold} days.\n")


if __name__ == "__main__":
    hostname = 'smartops-di05.ustdev.com'
    days_threshold = 300
    print_certificates_expiring_soon(hostname, days_threshold)
