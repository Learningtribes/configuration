#!/bin/bash
##
## Installs the pre-requisites for running Open edX on a single Ubuntu 16.04
## instance.  This script is provided as a convenience and any of these
## steps could be executed manually.
##
## Note that this script requires that you have the ability to run
## commands as root via sudo.  Caveat Emptor!
##

##
## Sanity checks
##

if [[ ! $OPENEDX_RELEASE ]]; then
    echo "You must define OPENEDX_RELEASE"
    exit
fi

if [[ ! $LT_VERSION ]]; then
    echo "You must define LT_VERSION"
    exit
fi


if [[ `lsb_release -rs` != "16.04" ]]; then
    echo "This script is only known to work on Ubuntu 16.04, exiting..."
    exit
fi

##
## Log what's happening
##

mkdir -p logs
log_file=logs/install-$(date +%Y%m%d-%H%M%S).log
exec > >(tee $log_file) 2>&1
echo "Capturing output to $log_file"
echo "Installation started at $(date '+%Y-%m-%d %H:%M:%S')"

function finish {
    echo "Installation finished at $(date '+%Y-%m-%d %H:%M:%S')"
}
trap finish EXIT

echo "Installing release '$OPENEDX_RELEASE'"

##
## Set ppa repository source for gcc/g++ 4.8 in order to install insights properly
##
sudo apt-get install -y python-software-properties
sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test

##
## Update and Upgrade apt packages
##
sudo apt-get update -y
sudo apt-get upgrade -y

##
## Install system pre-requisites
##
sudo apt-get install -y build-essential software-properties-common curl git-core libxml2-dev libxslt1-dev python-pip libmysqlclient-dev python-apt python-dev libxmlsec1-dev libfreetype6-dev swig gcc g++
sudo pip install --upgrade pip==9.0.3
sudo pip install --upgrade setuptools==39.0.1
sudo -H pip install --upgrade virtualenv==15.2.0

##
## Overridable version variables in the playbooks. Each can be overridden
## individually, or with $OPENEDX_RELEASE.
##
EDX_VERSION_VARS=(
    certs_version
    forum_version
    xqueue_version
    demo_version
    NOTIFIER_VERSION
    INSIGHTS_VERSION
    ANALYTICS_API_VERSION
    ECOMMERCE_VERSION
    ECOMMERCE_WORKER_VERSION
    DISCOVERY_VERSION
    THEMES_VERSION
)

LT_VERSION_VARS=(
    edx_platform_version
    configuration_version
)

for var in ${EDX_VERSION_VARS[@]}; do
    # Each variable can be overridden by a similarly-named environment variable,
    # or OPENEDX_RELEASE, if provided.
    ENV_VAR=$(echo $var | tr '[:lower:]' '[:upper:]')
    eval override=\${$ENV_VAR-\$OPENEDX_RELEASE}
    if [ -n "$override" ]; then
        EXTRA_VARS="-e $var=$override $EXTRA_VARS"
    fi
done

for var in ${LT_VERSION_VARS[@]}; do
    # Each variable can be overridden by a similarly-named environment variable,
    # or OPENEDX_RELEASE, if provided.
    ENV_VAR=$(echo $var | tr '[:lower:]' '[:upper:]')
    eval override=\${$ENV_VAR-\$LT_VERSION}
    if [ -n "$override" ]; then
        EXTRA_VARS="-e $var=$override $EXTRA_VARS"
    fi
done


# my-admin-passwords.yml is the file made by generate-passwords.sh.
if [[ -f my-passwords.yml ]]; then
    EXTRA_VARS="-e@$(pwd)/my-passwords.yml $EXTRA_VARS"
fi

##
## Clone the configuration repository and run Ansible
##
cd /var/tmp
git clone https://github.com/Learningtribes/configuration
cd configuration
git checkout $LT_VERSION
git pull

##
## Install the ansible requirements
##
cd /var/tmp/configuration
sudo -H pip install -r requirements.txt

##
## Run the edx_sandbox.yml playbook in the configuration/playbooks directory
##
cd /var/tmp/configuration/playbooks && sudo -E ansible-playbook -c local ./edx_sandbox.yml -i "localhost," $EXTRA_VARS "$@"
ansible_status=$?

if [[ $ansible_status -ne 0 ]]; then
    echo " "
    echo "========================================"
    echo "Ansible failed!"
    echo "----------------------------------------"
    echo "If you need help, see https://open.edx.org/getting-help ."
    echo "When asking for help, please provide as much information as you can."
    echo "These might be helpful:"
    echo "    Your log file is at $log_file"
    echo "    Your environment:"
    env | egrep -i 'version|release' | sed -e 's/^/        /'
    echo "========================================"
fi
