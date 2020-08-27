# fly_wrapper

A wrapper for the Concourse Fly CLI to automate sync and authentication.

Concourse is brilliant.

It's such a useful tool that you inevitably find yourself wanting to use it in more and more places, but as the number of Concourse clusters you interact with increases, the complexity of having to `fly sync` the correct binary and re-authenticate with the browser every 24 hours for each Concourse cluster can become cumbersome.

This repo contains a python-based wrapper script for `fly` which automates the `fly sync` and authentication steps. The wrapper scripts works in a similar way to `pyenv` or `rbenv`, storing different fly binary versions in a `~/.flyenv/bin/` directory, and automatically using the correct version for whichever Concourse you're interacting with.

This wrapper script will only work for LDAP authentication with Concourse. If you're not using an LDAP backend for auth, this script won't work for you.

## Pre-requisites

In order to automatically authenticate, this script requires access to your user credentials. Rather than storing them in environment variables or hidden files, it uses the [pass](https://passwordstore.org) command. To prevent conflicts for users with existing `pass` instances, the credentials are stored in a dedicated password store in `~/.my_secrets/`

The script will retrieve two values from the `pass` password store: `ad-username` and `ad-password`.

Full documentation for `pass` is available at the [passwordstore.org](https://passwordstore.org) website

The brief instructions for those already familiar with `gpg` and `pass` are as follows:

```sh
gpg --gen-key # Generate yourself a set of gpg-keys if you don't already have them
alias mysecrets='PASSWORD_STORE_DIR=~/.my_secrets pass' # You probably want this in your ~/.bash_profile too
mysecrets init <your_gpg_id>
mysecrets add ad-username # You will be prompted to enter your username
mysecrets add ad-password # You will be prompted to enter your password
```

You may also wish to extend the default gpg-agent timeout to a longer duration to prevent having to unlock your GPG keychain multiple times throughout the day. For example, to set an 8-hour timeout create/edit your `~/.gnupg/gpg-agent.conf` file with the following contents. (An 8-hour timeout means you only need to unlock your GPG keychain once per working day)

```sh
default-cache-ttl 43200
max-cache-ttl 43200
```

## Python pre-requisites

* Requires python 3+ version - Not compatible with 2.x

Being a python-based wrapper script, you will need to have the correct packages `pip install`ed in order for it to function. The required packages are listed in the `requirements.txt` file and can be installed as follows:

```sh
pip install -r requirements.txt
```

## How this wrapper script works

1. This wrapper script is intended to be called `fly` and to be included in your path before any locations where you might have the `fly` binary already.
1. Upon invocation, the script checks the command line arguments passed, looking for `-t|--target`, `-c|--concourse-url` and `--ca-cert` flags which are used when connecting to a Concourse for the first time.
1. If the target specified does not already exist in the `~/.flyrc` file, then it is added automatically (including ca-cert if specified)
1. A query is sent to the api of the Concourse target to get the version info, and if this version of the fly binary does not exist in `~/.flyenv/bin/` then it will automatically be downloaded and stored.
1. If the auth-token for a given concourse is in need of renewal, then the script will automatically re-authenticate and store the auth-token in the `~/.flyrc` file.
1. Finally, the entire set of command line arguments passed into the wrapper script are then passed over to the correct version of the `fly` binary, which can then proceed with the requested operation.

## Usage

It's exactly the same as `fly` in every way. Same arguments, everything. It will just never ask you to `fly sync` or authenticate through the browser ever again.

## Development

Pull requests will be happily received and reviewed :-)

If you're looking to implement a different credential store (something other than `pass`) then it should be fairly obvious in the code where it's trying to fetch the credentials currently and pretty straightforward to put into place an alternative. As long as you have some commands that you can use to get your user/password details they should drop right in.

```python
username = subprocess.getoutput(
    'PASSWORD_STORE_DIR=${HOME}/.my_secrets pass ad-username').strip()
password = subprocess.getoutput(
        'PASSWORD_STORE_DIR=${HOME}/.my_secrets pass ad-password').strip()
```

If you find issues/problems, please let us know via Issues on github. We're not promising that we'll fix them as we can't dedicate time to it, but we'd like to know if people find problems anyway.
