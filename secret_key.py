import secrets

# Generate a random hexadecimal string with 50 characters
generated_secret_key = secrets.token_hex(25)

print("Generated SECRET_KEY:", generated_secret_key)
