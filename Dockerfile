FROM python:3.10

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 

RUN apt-get update && apt-get install -y nano

WORKDIR /app

RUN pip install ipython==8.29.0
RUN ipython profile create && echo "c.TerminalInteractiveShell.display_completions = 'readlinelike'" >> /root/.ipython/profile_default/ipython_config.py

COPY req.txt .
RUN pip install -r req.txt

COPY . /app/
