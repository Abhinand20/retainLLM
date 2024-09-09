# Use a base image with Miniconda installed
FROM continuumio/miniconda3

# Set the working directory inside the container
WORKDIR /app

# Copy the environment.yml file to the container
COPY environment.yml .

# Create the Conda environment from the environment.yml file
RUN conda env create -f environment.yml

# Activate the Conda environment
SHELL ["conda", "run", "-n", "booksum", "/bin/bash", "-c"]

# Copy the rest of the application
COPY . .

# Expose the port for FastAPI
EXPOSE 8000

# Command to run FastAPI using the Conda environment
CMD ["conda", "run", "-n", "booksum", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
