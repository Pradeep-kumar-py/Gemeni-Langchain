command to build docker image for specific platform

1. docker buildx create --use
2. docker buildx build --platform linux/amd64 -t pradeep050/gemeni-langchain --push .


some other command
* docker build -t pradeep050/gemeni-langchain:latest .
* docker run -d -p 80:80 gemeni-langchain 


* docker build -t pradeep050/gemeni-langchain:latest .
* docker push pradeep050/gemeni-langchain:latest