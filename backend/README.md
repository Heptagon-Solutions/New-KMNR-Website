# Backend

Run `pipenv run py app.py` to start the backend application in debug mode. By using debug mode, you don't have to restart the app after making changes and you get more detailed error logs.

To check that it is running go to [http://localhost:5000/]() (note that this port number only works if you are not using the docker compose file, if you are the port number is 8971).

If you are running the backend on a separate Linux machine from the frontend, run the `run_with_exposed_ports.sh` bash script. The IP addresses where the backend is reachable are displayed during it's startup.

## Maintenance

To see what dependencies are outdated run `pipenv update --dry-run`. To actually update them run `pipenv update`. **Please** start the app and test it before committing these changes.

### Adding Database Migrations

Add all database migrations to the `db-migrations` directory. Give the migrations script an understandable name, and prefix it with `XX_` where XX is the next number not taken (this is done to keep execution order alphabetical).

Note that if you are running docker, you will need to reset your container and image to apply the new migrations.

TODO: there is probably a better way to apply those migrations that we can implement, but this is how it works as of now.

## Dev Resources

[Documentation](https://mysqlclient.readthedocs.io/user_guide.html) for the MySql/MariaDB connector. _This is documentation for the underlying package that `flask_mysqldb` uses (the connector we use)_.
