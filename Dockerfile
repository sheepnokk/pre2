FROM osgeo/gdal:ubuntu-small-latest

RUN apt-get update && apt-get -y install python3-pip --fix-missing

WORKDIR /work-flood-level

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "./app/test.py"]