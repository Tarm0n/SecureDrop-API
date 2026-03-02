FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONUNBUFFERED = 1

# set working directory
WORKDIR /app

# copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy anything else
COPY . .

# create non-root user and switch
RUN useradd -m user
RUN chown -R user:user /app
USER user

EXPOSE 8000

#command to run
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]