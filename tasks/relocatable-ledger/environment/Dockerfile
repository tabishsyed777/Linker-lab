FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev make cmake binutils util-linux && rm -rf /var/lib/apt/lists/* && useradd -u 1000 builder
WORKDIR /app/project
COPY project/ /app/project/
RUN chmod -R a+rX /app
CMD ["sleep", "infinity"]
