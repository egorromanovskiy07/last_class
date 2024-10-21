docker build -t test_image .
docker run --rm test_image bash -c "python3 -m pytest ."