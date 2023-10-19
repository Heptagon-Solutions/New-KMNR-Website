# KWIP-2

This is a copy of the original [KWIP](https://github.com/KMNR/KWIP) with a change of tech stack.

- Frontend is now in Angular
- Backend is in Python's Flask

# First time setup

## Frontend

If you don't alread have _NodeJS_ installed, do so [here](https://nodejs.org/en) (we use 18.18.1 LTS, but anything with version 18 should work). During the installation make sure you check this box:

![image](https://github.com/KMNR/KWIP-2/assets/69428664/6e0dd2b5-0d8c-4416-a180-56b3e985394a)

Once _NodeJS_ is installed, in your terminal in the frontend folder run `npm install`.

Now the frontend should be good to go, read the README.md there for further info.

## Backend

### Flask Backend

As the backend uses Python, it must first be installed. Download the latest version from [here](https://www.python.org/downloads/).

`pip` should automatically be installed with Python, but you can make sure with the command `pip --version`.

This project uses `pipenv` to manage dependencies. In the backend folder, run the following commands to install pipenv and the necessary dependencies:

```
pip install --user pip
pip install --user pipenv
pipenv install
```

### MySQL Database

Your database username and password are _secrets_ that will be stored in a `.env` file. In the backend directory, create a copy of `example.env` and rename it `.env`. Fill in your chosen username and password as indicated in the file.

More Coming soon...
