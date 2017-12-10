#!/bin/bash

# variable
PROJECT_FOLDER="{project_name}"
PROJECT_NAME="{GitHubProjectName}"

# Version file to know if this script is running for the first time or not
version_file_path="/var/log/version.txt"

# Get environment
instance_id=$(ec2metadata --instance-id)
region=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document | grep region | awk -F\" '{print $4}')
environment=$(aws ec2 describe-tags --filters "Name=resource-id,Values=${instance_id}" "Name=key,Values=Environment" --region=${region} --output=text | cut -f5)
echo "[DEBUG]: 1 Instance id is ${instance_id}"
echo "[DEBUG]: 2 Region is ${region}"
echo "[DEBUG]: 3 Environment is ${environment}"

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

cd /var/python/${PROJECT_NAME}/


 echo "[INFO]: 4 Creating the virtual envoirnment..."
 # Create virtual env inside the prject folder
virtualenv venv
echo "export DJANGO_SETTINGS_MODULE=${PROJECT_FOLDER}.settings.${environment}" >> /var/python/${PROJECT_NAME}/venv/bin/activate

if [ -f "$version_file_path" ]
then
        # not the first time, increase version by 1
        version_number=$(cat $version_file_path)
        version_number=$((version_number+1))
        echo $version_number > $version_file_path

        echo "[INFO]: 5 not first time"
else
        echo "[INFO]: 6 Starting first time actions..."

        echo "[INFO]: 7 Creating logging directory..."
        #  For logging
        mkdir -p /var/python/${PROJECT_NAME}/logging/

        echo "[INFO]: 8 First time actions finished"
fi


echo "[INFO]: 9 Activating the virtual envoirnment..."
# Activate venv
source venv/bin/activate
sudo chown -R backend:backend /var/python/${PROJECT_NAME}/venv

echo "[INFO]: 10 Installing the requirements..."
# Install project requirments
pip install -r /var/python/${PROJECT_NAME}/requirements.txt

if ! [ -f "$version_file_path" ];
then
    echo "[INFO]: 11 Starting first time actions..."

    echo "[INFO]: 12 Configuring the symlinks..."
    # Symlink uwsgi.ini file to /etc/uwsgi/vassles
    sudo ln -s /var/python/${PROJECT_NAME}/${PROJECT_FOLDER}/configs/${environment}/harri_uwsgi.ini /etc/uwsgi/vassals/

    # Symlink nginx.conf file to /etc/nginx/sites-enabled/
    sudo ln -s /var/python/${PROJECT_NAME}/${PROJECT_FOLDER}/configs/${environment}/harri_nginx.conf /etc/nginx/sites-enabled/

    echo "[INFO]: 13 Configuring the .bash_aliases..."
    # Setup .bash_aliases file for start/restart/stop uwsgi server
    touch ~/.bash_aliases
    sudo touch /tmp/master_process.pid
    sudo chown backend:backend /tmp/master_process.pid
    echo "alias go_harri='cd /var/python/${PROJECT_NAME}'" >> ~/.bash_aliases
    echo "alias start_uwsgi='/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid backend --gid backend --daemonize /var/log/uwsgi-emperor.log --pidfile /tmp/master_process.pid'" >> ~/.bash_aliases
    echo "alias stop_uwsgi='/usr/local/bin/uwsgi --stop /tmp/master_process.pid'" >> ~/.bash_aliases
    echo "alias restart_uwsgi='/usr/local/bin/uwsgi --reload /tmp/master_process.pid'" >> ~/.bash_aliases

    echo "[INFO]: 14 First time actions finished"

     echo "[INFO]: 15 Creating version.txt file..."

     # First time, create versions file
     echo 1 > $version_file_path
fi

# Backend privilege to python folder
sudo chown -R backend:backend /etc/uwsgi/vassals
sudo chown -R backend:backend /var/python

echo "[INFO]: 16 Starting the nginx server..."
# Restart nginx
sudo /etc/init.d/nginx restart

echo "[INFO]: 17 Starting the uwsgi server..."
# Stop uwsgi
PID=`ps -ef | grep 'uwsgi' | grep -v grep | awk '{print $2}'`
if [ -n "$PID" ]
then
echo $PID
/usr/local/bin/uwsgi --stop /tmp/master_process.pid
fi

# Start uwsgi
/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid backend --gid backend --daemonize /var/log/uwsgi-emperor.log --pidfile /tmp/master_process.pid

echo "[INFO]: 18 uwsgi server started ..."
