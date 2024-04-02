ckanext-ytp-comments
====================

CKAN extension for adding comments to datasets. 

Anyone with an account can comment any public datasets. Users with modification access can delete comments from the dataset.

Some of the code is taken from [ckanext-comments](https://github.com/rossjones/ckanext-comments)


## Requirements

If your extension works across different versions you can add the following table:

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | not tested    |
| 2.7             | not tested    |
| 2.8             | not tested    |
| 2.9             | not tested    |
| 2.10.X          | yes           |
| 2.11.X          | yes           |


## Installation

To install ckanext-ytp-comments:

1. Activate your CKAN virtual environment, for example:

    ```shell
    . /usr/lib/ckan/default/bin/activate
    ```

2. Clone the source and install it on the virtualenv

    ```shell
    pip install git+https://github.com/csse-uoft/ckanext-ytp-comments#egg=ckanext-ytp-comments
    ```

3. Add `ckanext-ytp-comments` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Init DB
     ```shell
     # Use your own path to the ckan.ini
     ckan -c /etc/ckan/default/ckan.ini ytp initdb
     ```

6. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     ```shell
     sudo supervisorctl reload
     ```
