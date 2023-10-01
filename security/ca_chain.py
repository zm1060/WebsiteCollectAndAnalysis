import json
import ssl
import socket
import os


def fetch_certificates(hostname, unit_name):
    # Check if the website supports HTTPS
    os.makedirs(f'./ca/{unit_name}', exist_ok=True)

    filename = os.path.join(f'./ca/{unit_name}', f"{hostname}.json")
    if os.path.exists(filename):
        # If the file already exists, return
        return

    try:
        # Send SYN on TCP port 443
        with socket.create_connection((hostname, 443)) as s:
            s.settimeout(5)  # Set a timeout in case the connection takes too long
            context = ssl.create_default_context()
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
                    output_filename = f"./ca/{unit_name}/{hostname}.json"
                    with open(output_filename, 'w', encoding='utf-8') as json_file:
                        json.dump(certificate_info, json_file, ensure_ascii=False, indent=4)
                    print(f"Certificate information for {hostname} has been saved to {output_filename}.")
                    print(f"The TLS version used by {hostname} is: {tls_version}")

            except ssl.SSLError as e:
                # Write the hostname into a file within the unit_name directory
                error_filename = f'./ca/{unit_name}/rerror.txt'
                with open(error_filename, 'a') as error_file:
                    error_file.write(hostname + "\n")
                print(f"An error occurred while fetching the certificate: {e}. Error written to {error_filename}.")

    except (socket.timeout, socket.gaierror) as e:
        # Write the hostname into a file within the unit_name directory
        error_filename = f'./ca/{unit_name}/rerror.txt'
        with open(error_filename, 'a') as error_file:
            error_file.write(hostname + "\n")
        print(f"The website {hostname} does not support HTTPS or cannot be reached. Error written to {error_filename}.")

    except socket.error as e:
        # Handle the socket error
        print(f"Socket error occurred while connecting to {hostname}: {e}")


# fetch_certificates("www.baidu.com", "test")

