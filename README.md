# Fetch-Receipt-Processor-Challenge

## Pre-requisites
Please ensure you have Docker configured and correctly set up before running this application. If you use WSL, please make sure localhostForwarding is set to True in the .wslconfig file.
Clone this repository and navigate to the folder titled "fetch-receipt-processor-challenge".

## Running the application
1. Run `./start.sh`. This should build and run the container. You can verify this by running `docker ps` and checking for the container name "receipt-processor-backend".
2. Verify that the server is up by going to `http://localhost:8000` in your browser. You should see a message saying "Hello"
3. Using Postman (or any other client), make POST or GET requests as required.
4. To terminate the application, run `./start.sh`. Run `docker ps` to confirm the container "receipt-processor-backend" isn't running anymore.

*If you run into details, please reach out to gauravramnani007@gmail.com.*