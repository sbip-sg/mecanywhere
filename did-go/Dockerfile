# Start from the official Go image
FROM golang:1.20-bullseye

# Set the working directory inside the container
WORKDIR /app

# Copy the Go modules manifests
COPY go.mod go.sum ./

# Download and install Go dependencies
RUN go mod download

# Copy the rest of the application source code
COPY . .

# Expose the port the application runs on
EXPOSE 2592

# Command to run the executable
CMD ["go", "run", "./server", "--config", "./server/sample_cfg.json"]
