import random
import string


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(length))


def get_local_ip():
    """Returns the IP of the local host as seen by a remote host."""
    for name in ni.interfaces():
        # Find the first non-loopback IPv4 address
        addresses = ni.ifaddresses(name)
        if ni.AF_INET in addresses:
            address = addresses[ni.AF_INET][0]
            if 'broadcast' in address:
                return address['addr']
    return 'localhost'  # Cannot get local IP.
