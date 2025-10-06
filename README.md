# KWIP-2

A fork of KMNR's KWIP2 project for CS 4091 - Software Engineering Capstone II.

Stack:
- Angular frontend
- Flask (Python) backend
- MySQL/MariaDB database

## Quickstart commands

### Using Docker (Debian images):

`docker-compose up` to start everything, and `docker-compose down` to stop everything.

Use `docker-compose down --rmi all` to stop and **reset** everything _(not recommended unless you messed up the database or a container somehow)_.

### Not using Docker (Directly in Windows):

In `frontend/`: `npm run start`

In `backend/`: `pipenv run python3 app.py`

## First time setup

There are instruction documents for setting up KWIP for the first time in the `documentation` folder. Note that the instructions are different for Windows vs. Linux machines.

- [Windows setup](./documentation/windows-setup.md)
- [Linux setup](./documentation/linux-setup.md)
