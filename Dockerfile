# Build
FROM python:2.7
ADD requirements.txt /
ADD getsports.py /
WORKDIR /
RUN pip install -r requirements.txt
CMD ["python", "getsports.py"]
