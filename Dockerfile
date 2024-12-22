# Base image
FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-devel

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install django torch torchvision

# Expose the Django port
EXPOSE 8000

# Default command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]