
Update the database section in the config file:

..code: bash

version_locations = %(here)s/models/janitoo_template %(here)s/alembic/versions

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

Add an entry_point in setup.py

    entry_points = {
        'janitoo.models': [
            'janitoo_template = janitoo_template.models:extend',
        ],
    },

It's important that the entry_point name match the version-path parameter  and the branch label of the alembic command.
