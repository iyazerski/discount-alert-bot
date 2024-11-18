# base image
FROM python:3.12-slim AS builder-image

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# configure build args
ARG PROJECT_USER=admin
ARG PROJECT_PATH=/home/$PROJECT_USER/discount-alert-bot

# Install Poetry
RUN pip install --no-cache-dir poetry

# Create project directory and set ownership
RUN useradd --create-home $PROJECT_USER
WORKDIR $PROJECT_PATH
RUN chown $PROJECT_USER:$PROJECT_USER $PROJECT_PATH

# Switch to non-root user
USER $PROJECT_USER

# install requirements
COPY --chown=$PROJECT_USER:$PROJECT_USER pyproject.toml ./
RUN poetry install --with bot_interface --without bot_engine,dev --no-interaction

# main image
FROM python:3.12-slim AS main-image

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# configure build args
ARG PROJECT_USER=admin
ARG PROJECT_PATH=/home/$PROJECT_USER/discount-alert-bot

# Create project directory and set ownership
RUN useradd --create-home $PROJECT_USER
WORKDIR $PROJECT_PATH
RUN chown $PROJECT_USER:$PROJECT_USER $PROJECT_PATH

# Copy project files and virtual environment from builder-image
COPY --from=builder-image --chown=$PROJECT_USER:$PROJECT_USER $PROJECT_PATH $PROJECT_PATH

# Switch to non-root user
USER $PROJECT_USER

# copy project files
COPY --chown=$PROJECT_USER:$PROJECT_USER LICENSE pyproject.toml ./
COPY --chown=$PROJECT_USER:$PROJECT_USER bot_common bot_common
COPY --chown=$PROJECT_USER:$PROJECT_USER bot_interface bot_interface

# Set the PATH to use the virtual environment
ENV PATH="$PROJECT_PATH/.venv/bin:$PATH"

# Start the application
CMD ["uvicorn", "bot_interface.app:app", "--host", "0.0.0.0", "--port", "8000"]
