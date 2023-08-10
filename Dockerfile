FROM osgeo/gdal:ubuntu-small-latest



RUN apt-get update && apt-get -y install python3-pip --fix-missing

WORKDIR /pre2

RUN pip install --no-cache-di --upgrade /code/requirements.txt

COPY app/test.py ./

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app/test.py /app/test.py
RUN pip install geopandas


COPY . .

# CMD ["python3", "./app/test.py"]

CMD ["uvivorn", "app.main:ppp"]