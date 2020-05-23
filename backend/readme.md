# Running the project
* From the `backend` directory, install requirements with `pip install -r requirements.txt`
* Set an environment variable called `DATABASE` to be equal to a postgres url (e.g `docker:docker@localhost:5432/docker`)
* Set an environment variable called `FLASK_APP` to be equal to `helpr`
* Run `flask run` 

# Running Postgres via docker
* Install docker desktop
* from the utils/postgres_db directory, run `docker run --rm -P -p 5432:5432 --name helpr_docker_db eg_postgresql`
* You probably want to run migrations. To do this:
    * you need to make sure you have the FLASK_APP environment variable set
     * from `backend/` run the command `flask db upgrade`
     * This should apply the migrations stored in the migrations directory


# Tests are currently not really setup
* Our project is relatively similar to this from the Flask docs though, should be easy enough to addapt. 
    * https://flask.palletsprojects.com/en/1.1.x/tutorial/tests/

# Authentication
* The authentication is based around Miguel Grinberg's REST-Auth example, using the up to date code from his example:
    * https://github.com/miguelgrinberg/REST-auth/blob/2904b70ea95885bc523e472e58e934925f1ab1eb/api.py