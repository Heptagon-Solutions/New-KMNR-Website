## Frontend

If you don't already have _NodeJS_ installed, do so [here](https://nodejs.org/en) (we use 18.18.0 LTS, but anything with version 18 should work). During the installation make sure you check this box:

![image](https://github.com/KMNR/KWIP-2/assets/69428664/6e0dd2b5-0d8c-4416-a180-56b3e985394a)

Once _NodeJS_ is installed, in your terminal in the frontend folder run `npm install`.

Now the frontend should be good to go, read the [README.md](../frontend/README.md) there for further info.

## Backend

As the backend uses Python, it must first be installed. Download the latest version from [here](https://www.python.org/downloads/).

`pip` should automatically be installed with Python, but you can make sure with the command `pip --version`.

This project uses `pipenv` to manage dependencies. In the backend folder, run the following commands to install pipenv and the necessary dependencies:

```
pip install --user pip
pip install --user pipenv
pipenv install --dev
```

## Database

You will need to install MySQL on your device to use the database. Read [`Installing_MySQL_on_Windows.md`](./Installing_MySQL_on_Windows.md) for instructions.

Connect to your MySQL Server and run `backend/setup.sql`. There are several commands/applications you can use to do this, but here are instructions for using _MySQL Command Line Client_ to do it:

1. Find and copy the absolute path to your [`backend/setup.sql`](../backend/setup.sql) file
2. Open _MySQL Command Line Client_
3. Run the command `source <setup.sql's absolute path>;` (don't forget the semicolon!)

If you would like to populate your database with some prepared sample data, repeat these steps with [`backend/sample_data.sql`](../backend/sample_data.sql).

After that your database should be running and prepared for use.

Make sure to read [`backend/README.md`](../backend/README.md) for information about how to use the backend.
