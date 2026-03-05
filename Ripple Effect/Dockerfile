# STEP 1: Use a lightweight Python base image
FROM python:3.11-slim

# STEP 2: Set the directory where code will live inside the container
WORKDIR /app

# STEP 3: Install system-level tools (needed for some math libraries)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# STEP 4: Copy the 'shopping list' of libraries first
# (This makes rebuilding faster if you only change code, not libraries)
COPY requirements.txt .

# STEP 5: Install the Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# STEP 6: Copy your actual project files (filtered by .dockerignore)
COPY . .

# STEP 7: Tell Docker that Streamlit runs on port 8501
EXPOSE 8501

# STEP 8: The command to launch the dashboard
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]