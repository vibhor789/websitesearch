#!/bin/bash
# Convenience script to run the application

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Website Search & Chatbox Finder${NC}"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source venv/bin/activate
fi

# Check if query provided
if [ -z "$1" ]; then
    echo -e "${YELLOW}Usage: ./run.sh \"your search query\"${NC}"
    echo ""
    echo "Examples:"
    echo "  ./run.sh \"restaurants in New York\""
    echo "  ./run.sh \"law firms in California\""
    echo ""
    python main.py
else
    python main.py "$@"
fi
