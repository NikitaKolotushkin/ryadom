#!/bin/sh

uvicorn app.main:app --host 0.0.0.0 --port ${EDGE_ROUTER_SERVICE_PORT} --reload
