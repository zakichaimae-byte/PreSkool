import requests

session = requests.Session()

# Get CSRF token from the register page
resp = session.get('http://127.0.0.1:8000/fr/register/')
print(f"GET register: {resp.status_code}")

# Extract CSRF token from cookies
csrf = session.cookies.get('csrftoken')
print(f"CSRF token: {csrf}")

# Submit the form
data = {
    'csrfmiddlewaretoken': csrf,
    'first_name': 'Test',
    'last_name': 'User',
    'email': 'newuser_test123@example.com',
    'password': 'TestPass123!',
    'confirm_password': 'TestPass123!',
}

resp2 = session.post(
    'http://127.0.0.1:8000/fr/register/',
    data=data,
    headers={'Referer': 'http://127.0.0.1:8000/fr/register/'},
    allow_redirects=False
)
print(f"POST register: {resp2.status_code}")
print(f"Location header: {resp2.headers.get('Location', 'None')}")

# Check for error in response
if 'Erreur' in resp2.text or 'error' in resp2.text.lower():
    import re
    errors = re.findall(r'alert[^>]*>(.*?)</div>', resp2.text, re.DOTALL)
    for e in errors[:3]:
        print(f"Error: {e.strip()[:200]}")
