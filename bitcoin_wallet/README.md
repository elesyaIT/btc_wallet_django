# Bitcoin Wallet

Bitcoin Wallet - Bitcoin Wallet is a web application developed using Django, providing the functionality to manage a bitcoin wallet.

## Installation

To run the project, you'll need Python and Docker installed.

1. Clone the repository:
https://github.com/elesyaIT/btc_wallet_django
2. Create and activate a virtual environment (optional):

python3 -m venv venv

source venv/bin/activate

3. Navigate to the project directory:

cd bitcoin_wallet

4. Install project dependencies:

pip install -r requirements.txt

## Run the Docker container:
sudo docker build -t my_django_app .

sudo docker run -p 8000:8000 my_django_app

Open your web browser and go to http://localhost:8000

## Usage

### Add data to the transaction

You can add data to the transaction database either through the admin panel or via the API.

Through the admin panel:
    After launching the project, you can go to http://localhost:8000/admin/ and log in to the admin panel with the username root and the password 1234.
    In the admin panel, you can add, edit, and delete transactions, manage users, and other aspects of your application.

Through the API:
    You can also add data to the database via the API by accessing the endpoint http://localhost:8000/api/v1/walletlist/add_transaction/.
    You will need to send a POST request with the data of the new transaction in JSON format.

### Add transactions spent

You can input the amount spent in euros through the endpoint http://localhost:8000/api/v1/walletlist/spent_eur/
Transactions will be updated, and the balance will be displayed in bitcoins.

### Look total balance
You can view the total balance by accessing the endpoint http://localhost:8000/balance/
