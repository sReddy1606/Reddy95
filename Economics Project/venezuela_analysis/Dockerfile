# 1. Use an official lightweight Python image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your requirements file first (for faster building)
COPY requirements.txt .

# 4. Install the specific libraries your research needs
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your project (Home.py, pages/, data/, etc.)
COPY . .

# 6. Expose the port Streamlit uses
EXPOSE 8501

# 7. The command to run your app
CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]