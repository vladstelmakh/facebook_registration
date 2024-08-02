
# Facebook Account Registration with FastAPI and Playwright

This project demonstrates how to automate the registration of Facebook accounts using FastAPI and Playwright. The FastAPI server handles the registration requests and uses Playwright to interact with Facebook's registration page.

## Installation

To install the necessary dependencies, you can use the `requirements.txt` file. 

```sh
pip install -r requirements.txt
```

## Running the Server

To start the FastAPI server, run the following command:

```sh
uvicorn fastap:app --reload --port 8005
```

## Usage

You can use the `test.py` script to send a registration request to the FastAPI server.

```sh
python test.py
```

### Example Output

If the registration is successful, you will see output similar to this:

```
Акаунт успішно створено
Ім'я: John
Прізвище: Doe
Електронна пошта: john.doe@example.com
Пароль: randompassword123
```

## Project Structure

<ul>
    <li><code>fastap.py</code> - The FastAPI server that handles registration requests.</li>
    <li><code>test.py</code> - The script for sending a registration request to the FastAPI server.</li>
    <li><code>requirements.txt</code> - The file containing all necessary dependencies.</li>
</ul>

## fastap.py

```python
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from skimage import io, transform, util
import requests
import random
import string
import time
import names

subprocess.run(["playwright", "install"], check=True)

app = FastAPI()

class RegistrationRequest(BaseModel):
    proxy: str = None

def generate_name():
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    return first_name, last_name

def get_temp_email():
    response = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
    email = response.json()[0]
    return email

def modify_image(image_path):
    image = io.imread(image_path)
    image = util.random_noise(image)
    image = transform.rotate(image, angle=random.uniform(-30, 30))
    return image

@app.post("/register/")
def register_account(request: RegistrationRequest):
    user_agent = UserAgent().random
    proxy_server = request.proxy

    with sync_playwright() as p:
        if proxy_server:
            browser = p.chromium.launch(headless=False, proxy={'server': proxy_server})
        else:
            browser = p.chromium.launch(headless=False)

        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()

        first_name, last_name = generate_name()
        email = get_temp_email()

        page.goto("https://www.facebook.com/r.php")
        page.fill('input[name="firstname"]', first_name)
        time.sleep(1)
        page.fill('input[name="lastname"]', last_name)
        time.sleep(1)
        page.fill('input[name="reg_email__"]', email)
        page.click('body', position={'x': 0, 'y': 0})
        time.sleep(1)
        page.fill('input[name="reg_email_confirmation__"]', email)

        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        page.fill('input[name="reg_passwd__"]', password)
        page.select_option('select[name="birthday_day"]', str(random.randint(1, 28)))
        time.sleep(1)
        page.select_option('select[name="birthday_month"]', str(random.randint(1, 12)))
        time.sleep(1)
        page.select_option('select[name="birthday_year"]', str(random.randint(1980, 2000)))
        time.sleep(1)
        page.click('input[name="sex"][value="2"]')

        page.click('button[name="websubmit"]')
        time.sleep(5)

        result_TO_SAVE = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }
        
        if page.is_visible('text="There was an error with your registration. Please try registering again."'):
            browser.close()
            raise HTTPException(status_code=400, detail=f"Помилка при реєстрації. Спробуйте ще раз. {result_TO_SAVE}")
        elif "checkpoint" in page.url:
            image_path = 'path/to/sample_image.jpg'
            modified_image = modify_image(image_path)
            io.imsave('modified_image.jpg', modified_image)
            page.set_input_files('input[type="file"]', 'modified_image.jpg')
            page.click('button[type="submit"]')
        elif "facebook.com" in page.url:
            result = {
                "status": "success",
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password
            }
        else:
            browser.close()
            raise HTTPException(status_code=400, detail=f"Не вдалося створити акаунт {result_TO_SAVE}")

        browser.close()
        return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
```

## test.py

```python
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
```

## Requirements

Install the necessary dependencies with the following command:

```sh
pip install -r requirements.txt
```

```txt
fastapi
uvicorn
requests
playwright
fake-useragent
scikit-image
pydantic
names
```
