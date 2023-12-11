FROM python:3.10-bookworm

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

RUN echo "some comment"

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt \
	&& pip uninstall -y JWT PyJWT \
	&& pip install PyJWT==2.8.0

ENTRYPOINT ["python", "Backend/app.py"]