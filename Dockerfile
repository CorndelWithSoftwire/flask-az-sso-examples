FROM python:3.10

ENV POETRY_HOME=/poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH=/poetry/bin:${PATH}

WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN poetry install

COPY src/ /code/src
ENTRYPOINT [ "poetry", "run", "flask", "run", "--host", "0.0.0.0"]