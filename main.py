import requests
import datetime
import smtplib
import time

# CONSTANTS
MY_LAT = -14.8619237
MY_LNG = -40.8445346

TIME_NOW = datetime.datetime.now()
TIME_NOW_HOUR = TIME_NOW.hour

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
}


def is_night():
    response_sun = requests.get(url="https://api.sunrise-sunset.org/json?formatted=0", params=parameters)
    response_sun.raise_for_status()
    data_sun = response_sun.json()
    sunrise = int(data_sun['results']['sunrise'].split("T")[1].split(":")[0])
    sunset = int(data_sun['results']['sunset'].split("T")[1].split(":")[0])
    if TIME_NOW_HOUR >= sunset or TIME_NOW_HOUR <= sunrise:
        return True


def is_close():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data_iss = response.json()
    longitude = float(data_iss['iss_position']['longitude'])
    latitude = float(data_iss['iss_position']['latitude'])
    iss_position = (latitude, longitude)
    if MY_LAT-5 <= latitude <= MY_LAT+5 and MY_LNG-5 <= longitude <= MY_LNG+5:
        return True

while True:
    time.sleep(60)
    if is_close() and is_night():
        email = "xxxxxxxx"
        password = "xxxxxxxxx"
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(from_addr=email,
                                to_addrs=f"{birthday_person['email']}",
                                msg="Subject: LOOK UP!!!\n\nThe ISS is above you}"
                                )

