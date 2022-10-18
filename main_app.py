import psycopg2
from flask import Flask
from flask import request
from psycopg2 import Error
import requests


def solana(connection,cursor, address):


    url = f'https://solana-gateway.moralis.io/nft/mainnet/' + address + '/metadata'
    headers = {"accept": "application/json",
               "X-API-Key": "u8emWI08OHGRqpKRzmO3Y3gW4OhbTdOdVRuJobooGeSvYRGjep6bmjuIDVu8RqEI"}
    response = requests.get(url, headers=headers)


    cursor.execute(
        "INSERT INTO nft (address, info) values (" + "'" + address + "'" + "," + "'" + response.text + "'" + ")");
    connection.commit()

    return f''' 
                    <h1>infp: {response.text} </h1>

                                    '''






app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def form_example():
    if request.method == 'POST':
        connection = psycopg2.connect(user="postgres",
                                      password="123",
                                      host="127.0.0.1",
                                      port="5433",
                                      database="nft_db")
        cursor = connection.cursor()
        address = request.form.get('nftaddress')

        try:
            postgreSQL_select_Query = "SELECT info FROM nft WHERE address=" + "'" + address + "'" + ";"
            cursor.execute(postgreSQL_select_Query)
            mobile_records = cursor.fetchall()

            if mobile_records == []:
                solana(address)
            else:
                for row in mobile_records:
                    return f''' 
                                  <h1>infp: {row[0]} </h1>

                                                 '''


        except (Exception, Error) as error:
            return solana(connection, cursor, address)




        cursor.close()
        connection.close()


    return '''
                      <form method="POST">
                          <div><label>Get address: <input type="text" name="nftaddress"></label></div>
                          <input type="submit" value="Submit">
                      </form>'''


if __name__ == '__main__':
    app.run(debug=True)