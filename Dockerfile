# Use the official image as a parent image
FROM ubuntu:18.04

# Set the working directory
WORKDIR /usr/src/app

COPY requirements.txt .

# Inform Docker of the port being exposed.
EXPOSE 5000

# Run the command inside your image filesystem
RUN apt-get update
RUN apt-get install -y python3 python3-venv python3-pip
RUN python3 -m venv venv
RUN . venv/bin/activate
RUN pip3 install -r requirements.txt

# Run the specified command within the container.
CMD [ "python3", "api.py" ]

# Copy the rest of your app's source code frmo your host to your image filesystem.
COPY . .
