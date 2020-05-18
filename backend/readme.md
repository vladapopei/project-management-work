# Running the project
* From the `backend` directory, install requirements with `pip install -r requirements.txt`
* Set an environment variable called `DATABASE` to be equal to a postgres url (e.g `docker:docker@localhost:5432/docker`)
* Set an environment variable called `FLASK_APP` to be equal to `helpr`
* Run `flask run` 

# Running Postgres via docker
* Install docker desktop
* from the utils/postgres_db directory, run `docker run --rm -P -p 5432:5432 --name helpr_docker_db eg_postgresql`


