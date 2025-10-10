# KWIP-2

A fork of KMNR's KWIP2 project for CS 4091 - Software Engineering Capstone II.

Stack:
- Angular frontend
- Flask (Python) backend
- MySQL/MariaDB database

## Quickstart commands

### Using Docker (Debian images):

`docker compose up --watch` to start everything with hot reloading enabled (changes to files are reflected immediately).

`docker compose down` to stop everything.

Use `docker-compose down --rmi all` to stop and **reset** everything _(not recommended unless you messed up the database or a container somehow)_. Note that if you change/update dependencies anywhere, you will need to do this or delete your existing images, then rebuild.

Once it is up and running, access the services as so:

|          |                    |
| -------- | ------------------ |
| Frontend | [localhost:8970]() |
| Backend  | [localhost:8971]() |
| Database | [localhost:8972]()  |

If using Docker, use the following command to access the database directly: `mysql -u root -h localhost -P 8972 --protocol=tcp`

### Not using Docker (Directly in Windows):

In `frontend/`: `npm run start`

In `backend/`: `pipenv run python3 app.py`

Once everything is running, access the services as so:

|          |                    |
| -------- | ------------------ |
| Frontend | [localhost:4200]() |
| Backend  | [localhost:5000]() |
| Database | [localhost:3306]() |

The above commands enable hot reloading, so changes to the code are reflected immediately.

## First time setup

There are instruction documents for setting up KWIP for the first time in the `documentation` folder. Note that the instructions are different for Windows vs. Linux machines.

- [Windows setup](./documentation/windows-setup.md)
- [Linux setup](./documentation/linux-setup.md)
