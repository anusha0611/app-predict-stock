# Use a base Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Ensure the models directory exists
RUN mkdir -p models

# Train the model during build
RUN python models/train_model.py
# RUN echo "0 2 * * * python /app/models/train_model.py" >> /etc/crontabs/root


# Expose the Flask port
EXPOSE 5003

# Start the Flask application
CMD ["python", "app.py"]
# CMD ["sh", "-c", "crond -f & python app.py"]
