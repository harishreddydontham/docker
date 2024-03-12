From python:3.11
LABEL app1="boto3 with FastAPI"
MAINTAINER author = "dockertesting@gmail.com"
ENV AWS_ACCESS_KEY_ID=SAMPLEKEYID
ENV AWS_SECRET_ACCESS_KEY=SAMPLESECRETKEY
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt \
    python --version
COPY main.py main.py
CMD ["uvicorn", "main:app1", "--host", "0.0.0.0", "--port", "80" ]
