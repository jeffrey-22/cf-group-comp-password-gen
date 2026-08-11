# Generate random token for contest random seeding

import secrets
import string

token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
print(token)