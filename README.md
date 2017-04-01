#PlanetSync
The SSH Directory Mounter

##How does it work?
* Using sshfs, PlanetSync mount your remote folder on your local computer. [read more](https://en.wikipedia.org/wiki/SSHFS)

##What does it do?
* Create an ssh file share with your home's dynamic IP server
* Add an ssh key to you server
* Add an fstab entry to automaticaly mount your remote folder
* Mount your remote folder through the web or on your local network automaticaly


##Setup the project
###Debian
* Install pip's build dependency
    ```bash
    sudo apt-get install build-essential libssl-dev libffi-dev python-dev
    ```
* Update pip
	```bash
	sudo pip install pip -U
	```
* Install a system wide pip package
    ```bash
	sudo pip install virtualenv
	```
* Create a virtual environment
	```bash
	virtualenv -p python3 /home/user/choose/a/path/for/your/virtualenv
    ```
* Activate the virtualEnv
    ```bash
    source /home/user/choose/a/path/for/your/virtualenv/bin/activate
    ```
* Install project dependency
    ```bash
	pip install -r python.req
	```