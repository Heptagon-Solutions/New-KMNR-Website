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

Some of these softwares require configuration. Don't worry, it won't be too scary. There's a guide for each one below, follow there instructions until you are brought back to this menu, and keep clicking Next until they are all done.

### MySQL Server Configuration

#### Type and Network

Keep the defaults to configure your MySQL Server as a development server:

![image](https://github.com/KMNR/KWIP-2/assets/69428664/3595d55a-0518-4244-9002-9e9a949880c9)

Click Next.

#### Authentication Method

Select _Use Strong Password Encryption for Authentication (RECOMMENDED)_.

#### Accounts and Roles

MySQL Server has build security practices to prevent random people/programs from accessing your databases. As such, an account with a password is required for access. On this page you will be asked to set a password for this `root` account. This password is very important, and is used later in KWIP's setup, so you should **probably** write it down somewhere.

Once you set the password, click Next.

#### Windows Service

This is extra information you don't necessarily have to read, feel free to skip it:

> As this is a server, it will constantly run in the background of your computer to server any and all requests that are sent to it (in our case, requests from KWIP's backend to access it's database). To do this, MySQL Server configures itself as a Windows Service that starts up during System Startup and stays running while your computer is running.
>
> For some people, this may be undesirable, and for them there are ways to start and stop the MySQL Server Windows Service on command. These ways will not be described here, so if you're interested in that, figure out how to do it elsewhere.

If you could care less to do all that extra work, stick with the defaults:

![image](https://github.com/KMNR/KWIP-2/assets/69428664/4e06ca50-00d8-4851-bef3-82541ad95f2d)

Click Next.

#### Server File Permissions

This guide recommends selecting the first option:
_Yes, grant full access to the user running the Windows Service (if applicable)..._

#### Apply Configuration

Click Execute. Once done click Finish.

### MySQL Router Configuration

Leave the default settings:

![image](https://github.com/KMNR/KWIP-2/assets/69428664/7008a3a8-a100-4d19-a40d-c5023d187fa1)

Click Finish.

### Samples and Examples: Connect To Server

The _Full_ setup option automatically sets up some example databases for your sandbox-development-pleasure. Select the MySQL Server you just installed:

![image](https://github.com/KMNR/KWIP-2/assets/69428664/b05894c6-8489-41bf-a23d-a5fb00781072)

To actually add these to databases to the server, you must log into it as `root`. Enter the password you set for `root` earlier during the MySQL Server configuration and click Check. If you got green success symbols go ahead and click Next.

Click Execute then Finish.

## Installation Complete

That's it! Your done! The Installer can't hurt you anymore.

You can click those nice little checkboxes to start whatever software you want to play with first (I recommend the MySQL Workbench) and click Finish.
