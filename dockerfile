FROM ubuntu:20.04
ENV DEBIAN_FRONTEND noninteractive

# Update the package manager and install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-tk

# Install the required libraries
RUN pip3 install pandas pandastable matplotlib numpy xlsxwriter

# Set the working directory
WORKDIR /app

# Copy the current directory into the container
COPY . .


