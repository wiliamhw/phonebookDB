#container ini akan dinamai PHONEBOOK
docker rm -f PHONEBOOK
docker run -d -p 32000:32000 --name PHONEBOOK my-phonebook-service:latest