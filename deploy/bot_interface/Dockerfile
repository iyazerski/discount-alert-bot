FROM python:3.12-slim

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
USER $PROJECT_USER

# install requirements
COPY --chown=$PROJECT_USER:$PROJECT_USER pyproject.toml ./
RUN poetry install --with bot_interface --without bot_engine,dev --no-interaction
ENV PATH="$PROJECT_PATH/.venv/bin:$PATH"

# copy project files
COPY --chown=$PROJECT_USER:$PROJECT_USER LICENSE ./
COPY --chown=$PROJECT_USER:$PROJECT_USER bot_common bot_common
COPY --chown=$PROJECT_USER:$PROJECT_USER bot_interface bot_interface

# Start the application
CMD ["python3", "-m", "bot_interface"]
