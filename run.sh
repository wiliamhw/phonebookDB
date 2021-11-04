#container ini akan dinamai PHONEBOOK
docker rm -f PHONEBOOK
docker run -d -p 32000:32000 --name PHONEBOOK -e USERNAME=user1 my-phonebook-service:latest
