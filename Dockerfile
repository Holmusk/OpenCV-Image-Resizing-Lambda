FROM lambci/lambda:build-python3.8

# Install our dependencies
RUN yum -y install libXext libSM libXrender