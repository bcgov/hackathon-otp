# Assumptions

## Running Locally

You have recent versions of Python and pip installed (Python 3.10)

# Setup

To install required packages:

`pip install -r requirements.txt`

Assuming you have homebrew, run

```bash
brew tap sqitchers/sqitch
brew install sqitch --with-postgres-support
```

If you're on a Windows machine, you can install sqitch following these instructions: https://sqitch.org/download/windows/ 

# Running the Uvicorn server locally

`uvicorn main:app --host 0.0.0.0 --port 80`

# Running the Uvicorn server locally in debug mode

`uvicorn main:app --reload --host 0.0.0.0 --port 80`

To confirm that the Uvicorn server is running locally, after running one of the above commands, navigate to 0.0.0.0/docs in your browser.

# To set up a Postgres database for the app locally

From your Terminal or console window (shell), create a new database with the name 'email_verification' (or whatever database name desired) by running:

`createdb email_verification`

(If the database has been created successfully, there will be no output in the console. That's ok. But it would be a good idea to confirm it's been created either using the psql command line tool or using a database explorer application such as pgAdmin).

Then run the following command from your command line:

`sqitch deploy db:pg://<username>@localhost<:port>/email_verification` (replacing 'email_verification' if you've chosen a different database name).

If successful, there will be an output confirming that registry tables have been added to the database and that changes have been deployed.

You can view the newly created schema using the command

`psql -d email_verification -c '\dn everify'`