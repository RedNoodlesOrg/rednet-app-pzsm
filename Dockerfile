ARG PYTHON_BASE=3.12-slim
FROM python:$PYTHON_BASE AS builder
RUN pip install -U pdm
ENV PDM_CHECK_UPDATE=false
COPY pyproject.toml pdm.lock /usr/src/app/
COPY src/ /usr/src/app/src
WORKDIR /usr/src/app
RUN pdm install --check --prod --no-editable
FROM python:$PYTHON_BASE
COPY --from=builder /usr/src/app/.venv/ /usr/src/app/.venv
ENV PATH="/usr/src/app/.venv/bin:$PATH"
ENV PYTHONPATH=$PYTHONPATH:/usr/src/app/src/.
COPY src /usr/src/app/src

EXPOSE 80

CMD ["waitress-serve", "--host", "0.0.0.0", "--port" , "80", "--call", "pzsm_app:create_app"]
