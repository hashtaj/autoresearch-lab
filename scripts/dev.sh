#!/usr/bin/env bash
# Dev script to run backend and frontend concurrently
# Claude will likely update this to use concurrently, tmux, or just background jobs.

echo "Starting VisualResearcher Dev Environment..."

# Trap ctrl-c and kill all processes
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

# TODO: Start backend
# cd app/backend && uvicorn main:app --reload --port 8000 &
echo "Backend not yet implemented. Placeholder start..."

# Start frontend
cd app/frontend || exit
npm run dev
