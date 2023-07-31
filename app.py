import tweepy
import requests
import time

# Configuración de las credenciales de la API de Twitter
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''


# URL/API para obtener el valor del dólar blue
dollar_url = 'https://dolar-api-argentina.vercel.app/v1/dolares/blue'

# Configurar la autenticación de la API de Twitter
auth = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

def get_dollar_value():
    try:
        response = requests.get(dollar_url)
        if response.status_code == 200:
            data = response.json()
            blue_dollar_value = data['venta']
            return blue_dollar_value
        else:
            print("Error al obtener datos del dólar blue. Código de estado:", response.status_code)
            return None
    except Exception as e:
        print("Error:", e)
        return None

def publicar_en_twitter(tweet):
    try:
        auth.create_tweet(text=tweet)
        print("Tweet publicado exitosamente en Twitter:", tweet)
    except tweepy.errors.TweepyException as e:
        print("Error al publicar en Twitter:", e)

def main():
    last_dollar_value = None

    while True:
        try:
            dollar_value = get_dollar_value()
            if dollar_value is not None:
                if last_dollar_value is not None and dollar_value != last_dollar_value:
                    if dollar_value > last_dollar_value:
                        message = f"El dólar blue subió 📈 a ${dollar_value}  #DolarBlue"
                    else:
                        message = f"El dólar blue bajó 📉  a ${dollar_value}  #DolarBlue"

                    publicar_en_twitter(message)

                last_dollar_value = dollar_value

            time.sleep(60)  # Esperar 1 minuto antes de obtener una nueva cotización
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()