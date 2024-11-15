docker build -t receipt-processor .
docker run -p 8888:8000 --name receipt-processor-backend -d receipt-processor