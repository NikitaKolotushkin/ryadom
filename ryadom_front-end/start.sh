#!/bin/sh

uvicorn app.main:app --host 0.0.0.0 --port ${FRONT_END_SERVICE_PORT} --reload
