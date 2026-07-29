import smtplib
import requests

MY_LATITUDE = 41.462206559007626
MY_LONGITUDE = 2.0819858497493287
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_id = "4f3bca008cc6457babfbeaebc7ca366d"

parameters = {
    "lat": MY_LATITUDE,
    "lon": MY_LONGITUDE,
    "cnt": 4,
    "appid": api_id,
}

response = requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()["list"]
text = f"{response.json()["city"]["name"]}\n"

will_rain = False
for item in weather_data:
    if int(item["weather"][0]["id"]) < 700:
        will_rain = True
    text += (f"{item["dt_txt"]}: "
             f"{item["weather"][0]["description"]} "
             f"({item["weather"][0]["id"]})\n"
             )
print(text)
if will_rain:
    my_email = "carlo.gonzalez.troger@gmail.com"
    my_password = "kqza htuw ytaf ihqu"
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(my_email, my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject:Bring an Umbrella!\n\n{text}"
        )