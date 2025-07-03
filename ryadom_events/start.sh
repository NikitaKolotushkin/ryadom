#!/bin/sh

uvicorn app.main:app --host 0.0.0.0 --port ${EVENTS_SERVICE_PORT} --reload
