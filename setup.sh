#!/usr/bin/env bash
# ================================================================
# setup.sh — ChatBot project setup script (no API key required)
# Usage: bash setup.sh
# ================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

info()    { echo -e "${CYAN}[INFO]${RESET}  $*"; }
success() { echo -e "${GREEN}[OK]${RESET}    $*"; }
error()   { echo -e "${RED}[ERROR]${RESET} $*"; exit 1; }

echo ""
echo -e "${BOLD}╔══════════════════════════════════════════╗${RESET}"
echo -e "${BOLD}║       ChatBot — Project Setup            ║${RESET}"
echo -e "${BOLD}╚══════════════════════════════════════════╝${RESET}"
echo ""

# ── Step 1: Check prerequisites ───────────────────────────────────
info "Checking prerequisites..."
command -v python3 &>/dev/null || error "python3 not found. Install from https://python.org"
success "python3 found: $(python3 --version)"

# ── Step 2: Virtual environment ───────────────────────────────────
echo ""
info "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    success "Virtual environment created at ./venv"
else
    success "Virtual environment already exists."
fi
source venv/bin/activate
success "Virtual environment activated."

# ── Step 3: Install dependencies ──────────────────────────────────
echo ""
info "Installing dependencies from requirements.txt..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
success "Dependencies installed."

# ── Step 4: Start server ──────────────────────────────────────────
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════╗${RESET}"
echo -e "${BOLD}║         Starting Local Dev Server        ║${RESET}"
echo -e "${BOLD}╚══════════════════════════════════════════╝${RESET}"
echo ""
echo -e "  ${GREEN}➜  Open:${RESET}  http://localhost:8000"
echo -e "  ${GREEN}➜  Docs:${RESET}  http://localhost:8000/docs"
echo -e "  Press Ctrl+C to stop."
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000
