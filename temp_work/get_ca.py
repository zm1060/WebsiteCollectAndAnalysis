import csv
import json
import ssl
import socket
import os
import threading


def is_ip_address(hostname):
    try:
        socket.inet_aton(hostname)
        return True
    except socket.error:
        return False


def is_port_open(hostname, port):
    try:
        with socket.create_connection((hostname, port), timeout=5):
            return True
    except (socket.timeout, socket.gaierror, socket.error):
        return False


def log_ip_address_if_port_open(hostname):
    if is_port_open(hostname, 443):
        with open('443.txt', 'a') as file:
            file.write(hostname + "\n")


def fetch_certificates(hostname):
    # Check if the website supports HTTPS
    os.makedirs(f'./ca', exist_ok=True)

    filename = f'./ca/{hostname}.json'

    if os.path.exists(filename):
        # If the file already exists, return
        return
    log_ip_address_if_port_open(hostname)

    try:
        # Send SYN on TCP port 443
        with socket.create_connection((hostname, 443), timeout=5) as s:
            context = ssl.create_default_context()

            # Skip SSL verification for IP addresses
            if is_ip_address(hostname):
                context.check_hostname = False  # Disable hostname checking
                context.verify_mode = ssl.CERT_NONE

            # Initiate an HTTPS connection and fetch SSL certificates
            try:

                with context.wrap_socket(s, server_hostname=hostname) as ssock:
                    # Get the certificate
                    cert = ssock.getpeercert()
                    # Get the certificate chain
                    cert_chain = context.get_ca_certs()

                    # Create a dictionary with certificate details
                    certificate_info = {
                        'hostname': hostname,
                        'issuer': cert['issuer'],
                        'subject': cert['subject'],
                        'valid_from': cert['notBefore'],
                        'valid_until': cert['notAfter'],
                        'cert_chain': cert_chain,
                    }
                    # Get the negotiated TLS version
                    tls_version = ssock.version()
                    certificate_info['tls_version'] = tls_version

                    # Write the certificate information to a JSON file
                    output_filename = f"./ca/{hostname}.json"
                    with open(output_filename, 'w', encoding='utf-8') as json_file:
                        json.dump(certificate_info, json_file, ensure_ascii=False, indent=4)
                    print(f"Certificate information for {hostname} has been saved to {output_filename}.")
                    print(f"The TLS version used by {hostname} is: {tls_version}")

            except ssl.CertificateError as ce:
                # Handle certificate verification errors
                error_filename = f'./ca/certificate_errors.txt'
                with open(error_filename, 'a') as error_file:
                    error_file.write(f"{hostname}: Certificate error - {str(ce)}\n")
                print(f"Certificate verification failed for {hostname}: {ce}. Error written to {error_filename}.")

            except ssl.SSLError as e:
                # Handle other SSL errors
                error_filename = f'./ca/ssl_errors.txt'
                with open(error_filename, 'a') as error_file:
                    error_file.write(f"{hostname}: SSL error - {str(e)}\n")
                print(f"An SSL error occurred for {hostname}: {e}. Error written to {error_filename}.")


    except (socket.timeout, socket.gaierror) as e:
        # Write the hostname into a file within the unit_name directory
        error_filename = f'./ca/rerror.txt'
        with open(error_filename, 'a') as error_file:
            error_file.write(hostname + "\n")
        print(f"The website {hostname} does not support HTTPS or cannot be reached. Error written to {error_filename}.")

    except socket.error as e:
        # Handle the socket error
        print(f"Socket error occurred while connecting to {hostname}: {e}")


def process_ip_address(ip_address):
    fetch_certificates(ip_address)


def process_ip_addresses_from_csv(csv_file_path, max_threads=10):
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row

        threads = []
        for row in csv_reader:
            ip_address = row[0]

            while len(threads) >= max_threads:
                for t in threads:
                    if not t.is_alive():
                        threads.remove(t)

            thread = threading.Thread(target=process_ip_address, args=(ip_address,))
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for t in threads:
            t.join()


# Example usage
# csv_file_path = 'dns_new_11_10.csv'
# process_ip_addresses_from_csv(csv_file_path)
