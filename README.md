# GraphQLnp1


**Disclaimer**:
This project is used to demonstrate and explore the *n+1 problem* regarding database queries when querying dependent tables using GraphQL.
It was specifically created for my talk [Django und GraphQL: Einführung und Fallstricke](https://www.enterpy.de/lecture_compact1.php?id=12613&source=0) at [enterPy 2021](https://www.enterpy.de).
This project does only make sense in connection with this talk.
It is **not** intended as a sensible / professional stand-alone project.

I use a database filled via Django migrations. For the current purpose, I did not bother with creating a proper DB volume to make changes persistent.


This project is based on

- https://tutorial.djangogirls.org/de/django_installation/
- https://github.com/DjangoGirls/tutorial
- https://tutorial-extensions.djangogirls.org/en
- https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04

and extended with GraphQL API.


## Initial setup

In project dir:

```bash
# create venv
python -m venv .venv

# activate venv
. .venv/bin/activate
# Win10 (GitBash): . .venv/Scripts/activate

# install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt
```


## Start-Up (after Initial setup)

Project should then be reachable via

- http://localhost:8000/admin
- http://localhost:8000/graphql

### With fresh container

```bash
./start_all.sh -a
```

#### Activate DB logging

Press `Ctrl-C` to stop Django.

Save original config via `docker cp djangodbX:/var/lib/postgresql/data/postgresql.conf postgresql.conf.org`.

Copy prepared file back via `docker cp postgresql.conf djangodbX:/var/lib/postgresql/data/`.

Then in container (via `docker exec -it djangodb bash`) set owner and restart Postgresql:

```bash
chown postgres:postgres /var/lib/postgresql/data/postgresql.conf
su postgres
pg_ctl restart
```

Restart container via `docker start djangodbX`.
Database logging is active now.

I use `5439` as PostgreSQL port, as I need the default port for an independent instance. See also `mysite/settings.py`.


### With prepared container

```bash
./start_all.sh
```


## Observe PostgreSQL-Logging

```bash
docker exec -it djangodbX bash
# WIN10:  winpty docker exec -it djangodbX bash
> su postgres
> ls -al /var/lib/postgresql/data/log/
# choose appropriate version of log file
> tail -f /var/lib/postgresql/data/log/postgresql-*.log
```
