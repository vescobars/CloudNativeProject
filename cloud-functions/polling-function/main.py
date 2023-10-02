import os
import time
import requests
from flask import jsonify

# Environment variable
SECRET_FAAS_TOKEN = os.environ.get("SECRET_FAAS_TOKEN", "secret_faas_token")

# True native route
NATIVE_PATH = os.environ.get("NATIVE_PATH", "http://34.149.221.138/native/cards")

# Credit card route
CC_PATH = os.environ.get("CC_PATH", "http://34.149.221.138/credit-cards")


# Status polling function
def card_status_polling(request):
    """
    Receives request from the credit card microservice to get information from the true native microservice. Performs
    polling operation on true native microservice until the desired operation is ready :param request: Request from
    the credit card microservice :return: request to the credit card microservice with apropiate auth and transaction
    identifier (notifies that operation has been completed)
    """

    # Validate polling token
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer") or auth_header.split("Bearer ")[1] != SECRET_FAAS_TOKEN:
        return jsonify({"error": "Invalid token"}), 403

    # Extract request content
    data = request.get_json()
    ruv = data["RUV"]
    recipient_email = data["recipient_email"]
    transaction_identifier = data["transactionIdentifier"]
    secret_token = data["SECRET_TOKEN"]

    # Auth headers set up
    headers = {"Authorization": f'Bearer {secret_token}'}

    # Polling protocol
    while True:
        response = requests.get(f'{NATIVE_PATH}/{ruv}', headers=headers)
        if response.status_code == 200:
            break
        elif response.status_code == 202:
            time.sleep(10)  # Waits 10 seconds before re-starting polling sequence
        else:
            # Anything else other than 200 and 202 is considered an error
            return jsonify({"error": "Unexpected response from TrueNative service"}), 500

    # Extract data from TrueNative response
    true_native_data = response.json()
    status = true_native_data.get("status")
    created_at = true_native_data.get("createdAt")

    # Send data to Credit Card Micro Service
    credit_card_data = {
        "createdAt": created_at,
        "transactionIdentifier": transaction_identifier,
        "recipient_email": recipient_email,
        "status": status
    }

    headers = {"Authorization": f'Bearer {SECRET_FAAS_TOKEN}'}
    print(f"Sending data to credit card microservice at path: {CC_PATH}/{ruv}\n"
          f'"Authorization": {headers["Authorization"]}\n'
          f'"createdAt": {created_at}\n'
          f'"recipient_email": {recipient_email}\n'
          f'"transactionIdentifier": {transaction_identifier}\n',
          f'"status": {status}')

    credit_card_response = requests.post(f'{CC_PATH}/{ruv}', json=credit_card_data, headers=headers)

    # Check if post was successfully
    if credit_card_response.status_code != 200:
        return jsonify({
            "error": "Failed to send data to Credit Card microservice",
            "request_body": credit_card_data
        }), 500

    return "", 200
