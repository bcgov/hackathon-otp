# Assumptions

## Running Locally

You have recent versions of Python and pip installed (Python 3.10)

# Setup

To install required packages:

`pip install -r requirements.txt`

# Running the Uvicorn server locally

`uvicorn main:app --host 0.0.0.0 --port 80`

# Running the Uvicorn server locally in debug mode

`uvicorn main:app --reload --host 0.0.0.0 --port 80`

To confirm that the Uvicorn server is running locally, after running one of the above commands, navigate to 0.0.0.0/docs in your browser.