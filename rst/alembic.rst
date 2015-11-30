Create an extension which need a db access
==========================================

Extends the models
------------------

Add your models. You can look at janitoo_dhcp to get an example.

Add an entry_point in setup.py

    entry_points = {
        'janitoo.models': [
            'janitoo_template = janitoo_template.models:extend',
        ],
    },

It's important that the entry_point name match the version-path parameter and the branch label of the alembic command.

Develop your setup :

..code: bash

    python setup.py develop


Initialise alembic
------------------

Update the database section in the config file:

..code: bash

    version_locations = %(here)s/models/janitoo_template


And the bash helper script:

..code: bash

    vi alembic.sh


..code: bash

    #!/bin/bash
    alembic -c janitoo_template.conf -n database $* --version-path=models/janitoo_template


Create a new SQL version management for your project :

..code: bash

    alembic -c janitoo_template.conf init alembic

Create a new labelled branch for your project :

..code: bash
    alembic -c janitoo_template.conf -n database  revision -m "Create janitoo_template branch" --head=base --branch-label=janitoo_template --version-path=models/janitoo_template

Update env.py

..code: bash
    #~ target_metadata = None
    from janitoo_db.base import Base
    target_metadata = Base.metadata


Using jnt_dbman
---------------

jnt_dman allows you to work on an offline database.

Create a database from migration scripts :

..code: bash

    jnt_dbman initdb

This will create the database using the default url : "sqlite:////tmp/janitoo_dbman.sqlite". You can change it using the --url parameter.


Create a database from models :

..code: bash

    jnt_dbman createdb


Drop the database :

..code: bash

    jnt_dbman dropdb


Working with branches
---------------------

Each extension (janitoo included) has its branch :

Show all extension heads :

..code: bash

    jnt_dbman heads


Check full history of your extension :

..code: bash

    jnt_dbman history --revrange=janitoo_template:


Generate the migration script for your extension :

..code: bash

    jnt_dbman generate -m "Initial import" --head=janitoo_template


Clean the script as it can contains updates for others extension.

Using alembic
-------------

You can also use alembic to manage the models. You need to generate a copy of the version_locations to include in your alembic.ini using :

..code: bash

    jnt_dbman version_locations

