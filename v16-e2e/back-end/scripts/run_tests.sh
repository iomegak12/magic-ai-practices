#!/bin/bash
# Test Runner Script for Linux/Mac
# Usage: ./run_tests.sh [options]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   V16 E2E Back-End Test Runner       ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}Error: pytest is not installed${NC}"
    echo "Please install: pip install -r requirements.txt"
    exit 1
fi

# Parse command line arguments
TEST_TYPE="${1:-all}"

case "$TEST_TYPE" in
    "all")
        echo -e "${YELLOW}Running all tests...${NC}"
        pytest tests/ -v --tb=short
        ;;
    "unit")
        echo -e "${YELLOW}Running unit tests only...${NC}"
        pytest tests/unit/ -v --tb=short -m unit
        ;;
    "integration")
        echo -e "${YELLOW}Running integration tests only...${NC}"
        pytest tests/integration/ -v --tb=short -m integration
        ;;
    "fast")
        echo -e "${YELLOW}Running fast tests (excluding slow tests)...${NC}"
        pytest tests/ -v --tb=short -m "not slow"
        ;;
    "coverage")
        echo -e "${YELLOW}Running tests with coverage report...${NC}"
        pytest tests/ -v --cov=app --cov-report=html --cov-report=term
        echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"
        ;;
    "watch")
        echo -e "${YELLOW}Running tests in watch mode...${NC}"
        pytest tests/ -v --tb=short -f
        ;;
    "failed")
        echo -e "${YELLOW}Re-running only failed tests...${NC}"
        pytest tests/ -v --tb=short --lf
        ;;
    "verbose")
        echo -e "${YELLOW}Running tests with verbose output...${NC}"
        pytest tests/ -vv --tb=long
        ;;
    "quick")
        echo -e "${YELLOW}Running quick smoke tests...${NC}"
        pytest tests/ -v --tb=short -k "test_health or test_info" --maxfail=3
        ;;
    "help")
        echo "Usage: ./run_tests.sh [option]"
        echo ""
        echo "Options:"
        echo "  all         - Run all tests (default)"
        echo "  unit        - Run unit tests only"
        echo "  integration - Run integration tests only"
        echo "  fast        - Run fast tests (exclude slow)"
        echo "  coverage    - Run tests with coverage report"
        echo "  watch       - Run tests in watch mode (re-run on file changes)"
        echo "  failed      - Re-run only failed tests"
        echo "  verbose     - Run tests with detailed output"
        echo "  quick       - Run quick smoke tests"
        echo "  help        - Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./run_tests.sh unit"
        echo "  ./run_tests.sh coverage"
        echo "  pytest tests/unit/test_helpers.py -v"
        echo "  pytest tests -k test_health -v"
        ;;
    *)
        echo -e "${RED}Error: Unknown option '${TEST_TYPE}'${NC}"
        echo "Use './run_tests.sh help' for usage information"
        exit 1
        ;;
esac

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ Tests completed successfully${NC}"
else
    echo -e "${RED}✗ Tests failed${NC}"
fi

exit $EXIT_CODE
