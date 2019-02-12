## pysportstracker

## author: Lennart Takanen, Johanna Haara, Nicholas Kukka

## modified: 25.1.2019

Short brief:

    service type = microservice

    File named by getsports.py script provides a sportstracker data of your friends. Results are provided in mapped configuration and
    Currently it uses API token, which have been inspected from sports-tracker website. It is not our token, and could end working as anyday (if changed).

    Easy going local development can be:
        running python getsports.py

    result should be like this:
    [
        {
            "duration": 80,
            "account": "Jsmith",
            "endtime": "2019-01-17 18:16:06",
            "fullname": "John Smith",
            "starttime": "2019-01-17 16:56:06"
        },
        {
            "duration": 47,
            "account": "playerx",
            "endtime": "2017-02-12 15:55:07",
            "fullname": "John Doe",
            "starttime": "2017-02-12 15:08:07"
        }
    ]

Developing local docker test:

    docker-compose -f docker-compose.yml up

Production:

Building image:

    cd docker
    ./build.sh
    cd ..

And Deploy to swarm:

    docker stack deploy --with-registry-auth -c docker-compose-prod.yml pysportstracker
