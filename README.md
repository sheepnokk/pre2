
"# prediction-flood-level" 

#how to build docker
docker build --tag pre2 . 


docker run pre2"


docker build -t csv-generator .
docker build -t Scsv-generator .

docker export --output="latest.tar" red_panda

docker run -v ${PWD}:/data ex_scrape


docker run -v $PWD/output:/usr/my/workspace mycontainer app