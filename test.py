import requests

url = "http://127.0.0.1:8005/register/"


payload = {
    "proxy": ""
}

response = requests.post(url, json=payload)
print(response.json())
if response.status_code == 200:
    data = response.json()
    print("Акаунт успішно створено")
    print(f"Ім'я: {data['first_name']}")
    print(f"Прізвище: {data['last_name']}")
    print(f"Електронна пошта: {data['email']}")
    print(f"Пароль: {data['password']}")
else:
    print(f"Помилка: {response.json()['detail']}")
