First, find the container that runs your MongoDB and ssh into it:
```bash
sudo docker exec -it <container name> /bin/bash
```

Then, find the collection you want to export:
```bash
mongo
show dbs
use <database>
show collections
exit
```
Then, run mongoexport command in the shell (not in mongo):
```bash
mongoexport -d <database-name> -c <collection-name> -q "{ 'bbox_id': 'NY1' }" --out ny1.json
```

Then, on your local machine, copy the file from inside the docker container to your current folder:
```bash
docker cp <mongodb docker container name>:/ny1.json .
```
Don't forget the dot from the end.

Clean the docker from json file (while ssh in container):
```bash
rm ny1.json
```