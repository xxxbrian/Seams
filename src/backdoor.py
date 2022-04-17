# This backdoor is only for testing(reset password).
# Do not use it in production.

from src.config import SECRET
rcode = []

def add_code(code_str):
    rcode.append(code_str)

def get_code(secret):
    if secret != SECRET:
        return {'rcode': []}
    return {'rcode': rcode}
