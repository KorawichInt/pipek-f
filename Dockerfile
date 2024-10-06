FROM debian:sid
RUN echo 'deb http://mirror.psu.ac.th/debian/ sid main contrib non-free non-free-firmware' > /etc/apt/sources.list
RUN echo 'deb http://mirror.kku.ac.th/debian/ sid main contrib non-free non-free-firmware' >> /etc/apt/sources.list

RUN apt-get update && apt-get upgrade -y

RUN apt install -y python3 python3-dev python3-pip python3-venv npm git locales cmake
RUN sed -i '/th_TH.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8 
# ENV LC_ALL en_US.UTF-8



RUN python3 -m venv /venv
ENV PYTHON=/venv/bin/python3
RUN $PYTHON -m pip install wheel poetry gunicorn

WORKDIR /app

ENV PIPEK_SETTINGS=/app/pipek-production.cfg

COPY pipek/cmd /app/pipek/cmd
COPY poetry.lock pyproject.toml /app/

# RUN . /venv/bin/activate \
# 	&& poetry config virtualenvs.create false \
#     && peotry add torch torchvision \
#     # && poetry update \
# 	&& poetry install --no-interaction --only main

RUN . /venv/bin/activate && poetry config virtualenvs.create false
RUN . /venv/bin/activate && poetry install --no-interaction --only main
RUN . /venv/bin/activate && poetry add torch torchvision
# RUN poetry update

COPY pipek/web/static/package.json pipek/web/static/package-lock.json pipek/web/static/
RUN npm install --prefix pipek/web/static

COPY . /app



# # Use a base image that supports CUDA (assuming you want CUDA support)
# FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

# # Install necessary packages and Python dependencies
# RUN apt-get update && apt-get install -y \
#     python3 python3-dev python3-pip python3-venv npm git locales cmake \
#     && rm -rf /var/lib/apt/lists/*

# # Set up locale
# RUN sed -i '/th_TH.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
# ENV LANG en_US.UTF-8

# # Create a virtual environment
# RUN python3 -m venv /venv
# ENV PYTHON=/venv/bin/python3
# RUN $PYTHON -m pip install --upgrade pip
# RUN $PYTHON -m pip install wheel poetry gunicorn

# # Set up working directory
# WORKDIR /app

# # Set the environment variable for your application settings
# ENV PIPEK_SETTINGS=/app/pipek-production.cfg

# # Copy the application code
# COPY pipek/cmd /app/pipek/cmd
# COPY poetry.lock pyproject.toml /app/

# # Install Python dependencies using poetry (including torch with CUDA)
# RUN . /venv/bin/activate \
#     && poetry config virtualenvs.create false \
#     && poetry install --no-interaction --only main

# # Manually install PyTorch with CUDA
# RUN $PYTHON -m pip install torch==2.4.0+cu118 torchvision==0.15.0+cu118 torchaudio==2.4.0 --index-url https://download.pytorch.org/whl/cu118

# # Copy static files and install npm packages
# COPY pipek/web/static/package.json pipek/web/static/package-lock.json pipek/web/static/
# RUN npm install --prefix pipek/web/static

# # Copy the rest of the application
# COPY . /app
