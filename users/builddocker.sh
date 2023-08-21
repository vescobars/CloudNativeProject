# Just as an example, dont actually run this script naively
docker build -t users-backend .
docker run --env-file ./.env -p 127.0.0.1:8000:8000 --name users_backend --net packages-network users-backend