@echo off
REM Test Runner Script for Windows
REM Usage: run_tests.bat [options]

setlocal enabledelayedexpansion

echo ╔══════════════════════════════════════╗
echo ║   V16 E2E Back-End Test Runner       ║
echo ╚══════════════════════════════════════╝
echo.

REM Check if pytest is installed
where pytest >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: pytest is not installed
    echo Please install: pip install -r requirements.txt
    exit /b 1
)

REM Parse command line argument
set TEST_TYPE=%1
if "%TEST_TYPE%"=="" set TEST_TYPE=all

if "%TEST_TYPE%"=="all" (
    echo Running all tests...
    pytest tests/ -v --tb=short
    goto :end
)

if "%TEST_TYPE%"=="unit" (
    echo Running unit tests only...
    pytest tests/unit/ -v --tb=short -m unit
    goto :end
)

if "%TEST_TYPE%"=="integration" (
    echo Running integration tests only...
    pytest tests/integration/ -v --tb=short -m integration
    goto :end
)

if "%TEST_TYPE%"=="fast" (
    echo Running fast tests (excluding slow tests)...
    pytest tests/ -v --tb=short -m "not slow"
    goto :end
)

if "%TEST_TYPE%"=="coverage" (
    echo Running tests with coverage report...
    pytest tests/ -v --cov=app --cov-report=html --cov-report=term
    echo Coverage report generated in htmlcov/index.html
    goto :end
)

if "%TEST_TYPE%"=="watch" (
    echo Running tests in watch mode...
    pytest tests/ -v --tb=short -f
    goto :end
)

if "%TEST_TYPE%"=="failed" (
    echo Re-running only failed tests...
    pytest tests/ -v --tb=short --lf
    goto :end
)

if "%TEST_TYPE%"=="verbose" (
    echo Running tests with verbose output...
    pytest tests/ -vv --tb=long
    goto :end
)

if "%TEST_TYPE%"=="quick" (
    echo Running quick smoke tests...
    pytest tests/ -v --tb=short -k "test_health or test_info" --maxfail=3
    goto :end
)

if "%TEST_TYPE%"=="help" (
    echo Usage: run_tests.bat [option]
    echo.
    echo Options:
    echo   all         - Run all tests (default)
    echo   unit        - Run unit tests only
    echo   integration - Run integration tests only
    echo   fast        - Run fast tests (exclude slow)
    echo   coverage    - Run tests with coverage report
    echo   watch       - Run tests in watch mode (re-run on file changes)
    echo   failed      - Re-run only failed tests
    echo   verbose     - Run tests with detailed output
    echo   quick       - Run quick smoke tests
    echo   help        - Show this help message
    echo.
    echo Examples:
    echo   run_tests.bat unit
    echo   run_tests.bat coverage
    echo   pytest tests/unit/test_helpers.py -v
    echo   pytest tests -k test_health -v
    goto :end
)

echo Error: Unknown option '%TEST_TYPE%'
echo Use 'run_tests.bat help' for usage information
exit /b 1

:end
set EXIT_CODE=%ERRORLEVEL%

echo.
if %EXIT_CODE% EQU 0 (
    echo ✓ Tests completed successfully
) else (
    echo ✗ Tests failed
)

exit /b %EXIT_CODE%
