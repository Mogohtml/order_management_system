import requests
from requests.auth import HTTPBasicAuth

url = 'http://127.0.0.1:5000/get_form'
auth = HTTPBasicAuth('Magomed', 'Chuvac_ov')
data = {
    'order_id': '12345',
    'order_date': '2023-10-01',
    'lead_email': 'john.doe@example.com',
    'customer_phone': '+7 123 456 78 90'
}

response = requests.post(url, json=data, auth=auth)
print(response.json())
