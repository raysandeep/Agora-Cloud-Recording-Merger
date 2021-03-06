
# Agora-Cloud-Recording-Merger
Agora-Recording-Merger helps in merging Cloud Recorded Files generated by Agora Cloud Recording. 

# Prerequisites
 1. Heroku Developer Account / VM
 2. AWS IAM Credentials 
 3. AWS S3 Bucket ( to uplaod merged files )
 4. AWS S3 Bucket containing recorded files
 5. Docker 
# Steps to run
 1. Deploying to Heroku
	  - Head on to your Heroku Developer Account and create a new name
	  - Once done, head on to overview tab and click on configure add-ons. 
	  - Add Postgres and Redis add-ons. 
	  - Now, install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-command-line)
	  - Clone the repo, duplicate the `sample.env` file and rename it to `.env`. 
	  - Fill all your creds in `.env` file and run the following commands
        ```
        heroku login
        heroku container:login
        heroku container:push web
        heroku container:release web
        ```
  2. Deploying through VM
	    - Install docker and docker-compose on the vm.
	    - Duplicate the `sample.env` file and rename it to `.env`. 
	    - Uncomment 11-16 lines from `.env` file and fill all the fields. 
	    - Build the docker image with the following command.
	      
	      ```docker-compose build ```
	    - Run the docker-compose file with the following command. 
	      
	      ```docker-compose up -d ```
	    - Now, let's access into database container and create a database with following command.
	      
	      ```docker exec -it backend bash```
	    - Create a database and run compose up command. 

# Tech Stack
  1. Docker 
  2. Django 
  3. Celery
  4. Postgres
  5. FFMPEG

# API Docs
```
curl --location --request POST 'https://backend.com/api/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "channel_id":""
}'
```
#### Optional fields: 
- merge_mode ( int )
- fps ( int )
- width ( int )
- height ( int )
