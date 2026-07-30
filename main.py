import smtplib
import requests
import os
import datetime as dt

MY_LATITUDE = 41.462206559007626
MY_LONGITUDE = 2.0819858497493287
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_id = os.environ.get("OWM_API_KEY")
my_email = os.environ.get("MY_EMAIL")
my_password = os.environ.get("MY_PASSWORD")

parameters = {
    "lat": MY_LATITUDE,
    "lon": MY_LONGITUDE,
    "cnt": 4,
    "appid": api_id,
}

response = requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()["list"]
now = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
text = f"{now} {response.json()["city"]["name"]} forecast:\n\n"

for item in weather_data:
    text += (f"{item["dt_txt"]}: "
             f"{item["weather"][0]["description"]} "
             f"({item["weather"][0]["id"]})\n"
             )

with smtplib.SMTP('smtp.gmail.com') as connection:
    connection.starttls()
    connection.login(my_email, my_password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs=my_email,
        msg=f"Subject:Today's weather forecast!\n\n{text}".encode("utf-8")
    )
