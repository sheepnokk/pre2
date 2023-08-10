
# Installation
### prediction-flood-level

### Don't forget to add tif file in the folder "point_tif2" before run it.

* How to build using docker-compose
  ```bash
  docker-compose build
  ```

* How to run using docker-compose
  ```bash
  docker-compose up
  ```

### if got error like "The requested image's platform (linux/amd64) does not match the detected host platform"
please add this line in yaml service
```bash
  platform: linux/amd64
```

