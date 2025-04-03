# Backend

Run `pipenv run py app.py` to start the backend application in debug mode. By using debug mode, you don't have to restart the app after making changes and you get more detailed error logs.

To check that it is running go to [http://localhost:5000/]().

If you are running the backend on a separate Linux machine from the frontend, run the `run_with_exposed_ports.sh` bash script. The IP addresses where the backend is reachable are displayed during it's startup.

## Maintenance

To see what dependencies are outdated run `pipenv update --dry-run`. To actually update them run `pipenv update`. **Please** start the app and test it before committing these changes.
