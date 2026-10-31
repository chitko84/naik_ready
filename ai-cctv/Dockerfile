FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 NAIKREADY_RUNTIME_DIR=/tmp/naikready-vision YOLO_CONFIG_DIR=/tmp/ultralytics
WORKDIR /app/ai-cctv
RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*
COPY requirements-service.txt ./
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu && pip install --no-cache-dir -r requirements-service.txt
COPY . ./
EXPOSE 80
CMD ["python", "serve.py"]
