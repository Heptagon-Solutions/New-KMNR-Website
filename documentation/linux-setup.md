# Setting up KWIP on Linux

## Cloning the project using SSH

You'll need to generate an SSH key. In the VM, run `ssh-keygen -t rsa -b 2048 -C "<A message to help you remember what this key is for>"`. Then run `cat .ssh/id_rsa.pub`. Then go to Github, go to your preferences, go to SSH keys, add new key, give it a name, and copy and paste everything that that command spit out into there and save it. Now you can run `git clone git@github.com:KMNR/KWIP-2.git`.

## Frontend

NodeJS has installation instructions [here](https://nodejs.org/en/download/package-manager/all). Debian and Ubuntu distro instructions are [here](https://github.com/nodesource/distributions?tab=readme-ov-file#using-debian-as-root-nodejs-18). Make sure you install version 18.x.

The following instructions are copied here for installing v18.x on Debian. Run them as root:

```
apt-get install -y curl
curl -fsSL https://deb.nodesource.com/setup_18.x -o nodesource_setup.sh
bash nodesource_setup.sh
apt-get install -y nodejs
```

Then verify that it is installed with `node -v`.

Then, as normal, go to the frontend folder and run `npm install`.

### Connecting to frontend from a different machine

Install Angular CLI globally (to have access to the `ng` command directly):
```
sudo npm install -g @angular/cli@16.1.0
```

Then run the app with `ng serve --host 0.0.0.0` to expose the dev server on every IP address the machine owns. If you want it exposed on a specific port, add `--port <PORT NUMBER>`.

## Backend

Make sure python is installed: `python3 --version`.

Check if pip is installed: `pip --version` or `pip3 --version`. If not installed, install it with:

```
apt-get update && apt-get install python3-pip
```

Then install pipenv with:

```
pip install pipenv --break-system-packages
```

Then restart your terminal and try the `pipenv --version`.

For the MySQL/MariaDB-Python connector to work and install properly, you have to install some dependencies manually yourself (as described [here](https://pypi.org/project/mysqlclient)):

```
apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
```

After that, run `pipenv install --dev` as usual.

Now the Backend should run fine and the same as it would on a Windows machine.

### Connecting to Backend from a different machine

You will have to change your run command to make the server open to the local network. Running this command will make the backend server accessible on ALL IP addresses your machine owns:

```
pipenv run python3 -m flask run --host=0.0.0.0
```

If you are then running frontend on a different machine as backend, on that machine in `frontend/src/constants.ts`, in the `API_URL` variable, change `localhost` to the backend machine's IP address (use `ip address` command on backend machine to find it).

## Database

There is [this guide](https://dev.mysql.com/doc/refman/8.4/en/linux-installation-apt-repo.html) to install MySQL and MySQL Workbench onto a Debian VM.

HOWEVER, it seems easiest to just use MariaDB, which is widely considered a drop in replacement. Download it [here](https://mariadb.com/downloads/community/).

_NOTE:_ All of the below commands assume you are running them as root. Either run `su -` to login as root, or prefix them all with `sudo`.

As the README says in the tar archive (the file that you downloaded from MariaDB's website), run this command to extract the archive (a little bit of a chicken and the egg problem right?):

```
tar -xf <the downloaded tar file's name> /opt
```

Then cd into that extracted folder (as root still) and run `./setup_repository`.

Once that completes successfully it'll tell you to run this to install the MariaDB server:

```
apt-get update && apt-get install mariadb-server
```

MariaDB is now installed! Now run this command to run the server and to make it start on boot:

```
systemctl enable mariadb
```

Now to test it. Run the command `mariadb`. It'll open up a new prompt. Type in `SELECT VERSION();` and make sure you get something like this back:

```
+----------------------+
| VERSION()            |
+----------------------+
| 11.7.2-MariaDB-deb12 |
+----------------------+
```

It's working! Now you need to setup the KWIP database with the `setup.sql` and `sample_data.sql` scripts. While still in the MariaDB terminal, enter these two commands:

```
source <path to setup.sql>;
source <path to sample_data.sql>;
```

_If you run into issues, check [this website](https://www.server-world.info/en/note?os=Debian_12&p=mariadb); it was very helpful while writing this._
