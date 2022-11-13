FROM amazon/aws-lambda-python:3.9.2022.11.11.19

COPY ./src/* /home/
RUN yum install -y zip

RUN cd /home/; \
    pip install -r requirements.txt --target ./package; \
    cd package;	\
    zip -r ../deployment-package.zip .; \
    cd ..; \
    zip -g deployment-package.zip index.py; \
    zip -g deployment-package.zip aws_s3_wrapper.py; \
    zip -g deployment-package.zip file.py

