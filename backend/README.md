# Backend

Run `pipenv run py app.py` to start the backend application in debug mode. By using debug mode, you don't have to restart the app after making changes and you get more detailed error logs.

To check that it is running go to [http://localhost:5000/]().

# Installing MySQL for Windows

Go to https://dev.mysql.com/downloads/installer/. Select Version 8.0.34. Click Download on the top Installer (the one that says _mysql-installer-web-community-8.0.34.0.msi_ under the title) to be redirected to the download page. Scroll to the bottom and click _No thanks, just start my download_ to download the installer.

Start the Installer. Once booted it'll look like this:
![image](https://github.com/KMNR/KWIP-2/assets/69428664/8dbbe5a2-ca68-41a4-93e0-9786c0935203)

## Choosing A Setup Type

_Full_ is the recommended setup type, as it installs the MySQL Server and several development tools with it that you might find useful.

However, _Full_ likely includes a lot of software you won't use, so if you know what you're doing and you don't want the extra stuff, you can pick and choose what to install with _Custom_.

The rest of the guide assumes you selected _Full_.

## Download

In this section, you'll see a list of the softwares you are about to download. Click Execute to start the download process.

Some of the downloads might fail, and this is shown with "Error" displayed in the _Status_ column:
![image](https://github.com/KMNR/KWIP-2/assets/69428664/a5d58df2-e28e-4dea-af74-b0282559bc45)
Don't fret, you'll just have to download them again. Click Back and then click Next and you should return to the download list with only the bad downloads listed. Click Execute again. Repeat this process until all are successfully downloaded.

Once all softwares are downloaded, click Next.

## Installation

Now you'll the same list of softwares ready for installation. Click Execute.

Once all are Complete, click Next. 

## Product Configuration

Some of these softwares require configuration. Don't worry, it won't be too scary. Click Next.

### MySQL Router Configuration

Leave the default settings:
![image](https://github.com/KMNR/KWIP-2/assets/69428664/7008a3a8-a100-4d19-a40d-c5023d187fa1)

Click Finish.

### Samples and Examples: Connect To Server

The _Full_ setup option automatically sets up some example databases for your sandbox-development-pleasure. Select the MySQL Server you just installed:
![image](https://github.com/KMNR/KWIP-2/assets/69428664/b05894c6-8489-41bf-a23d-a5fb00781072)

To actually add these to databases to the server, you must log into it as `root`. Enter the password you set for `root` during the MySQL Server configuration and click Check.


