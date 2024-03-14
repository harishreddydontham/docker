From python:3.11
LABEL app1="boto3 with FastAPI"
MAINTAINER author = "dockertesting@gmail.com"
ENV AWS_ACCESS_KEY_ID=SAMPLEKEYID
ENV AWS_SECRET_ACCESS_KEY=SAMPLESECRETKEY
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN python --version && apt update && apt install -y unzip
COPY main.py main.py
ADD instruction.info instruction.info
ARG T_VERSION=1.70
ADD https://releases.hashicorp.com/terraform/${T_VERSION}/terraform_${T_VERSION}_linux_amd64.zip terraform.zip
RUN unzip terraform.zip -d /usr/local/bin && terraform --version
EXPOSE 80
# CMD ["uvicorn", "main:app1", "--host", "0.0.0.0", "--port", "80" ]
ENTRYPOINT ["uvicorn", "main:app1", "--host", "0.0.0.0", "--port", "80" ]
