# BUILDER
FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir ./wheels -r requirements.txt

# RUNNER
FROM python:3.12-slim

WORKDIR /app

# Create unprivileged user
RUN addgroup --system app && adduser --system --group app

# Copy dependencies from builder
COPY --from=builder /app/wheels ./wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache ./wheels/*

COPY . .

# Turn \r\n to \n
RUN sed -i 's/\r$//g' ./entrypoint.sh && chmod +x ./entrypoint.sh

RUN chown -R app:app /app

USER app

ENTRYPOINT [ "./entrypoint.sh" ]