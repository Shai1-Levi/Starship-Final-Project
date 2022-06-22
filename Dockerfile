FROM python:3
ADD ./ /
RUN python3 -m pip install requests
RUN python3 -m pip install flask
RUN python3 -m pip install pymongo
RUN python3 -m pip install hvac
RUN python3 -m pip install python_terraform
RUN python3 -m pip install flask_cors
RUN python3 -m pip install paramiko
RUN python3 -m pip install docker
EXPOSE 5000
ENV FLASK_APP=server.py
ENV FLASK_ENV=development
CMD ["python3", "-m", "flask", "run"]
# ENTRYPOINT ["python3"]
# CMD ["server.py"]