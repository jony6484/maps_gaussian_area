FROM python:3.9.12-slim-bullseye

WORKDIR /gaussian_gui

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY ./src ./src
COPY ./input ./input

ENV PYTHONPATH "${PYTHONPATH}:/gaussian_gui"
# ENV API_IP=${API_IP}
EXPOSE 8501

ENTRYPOINT ["streamlit","run"]
CMD ["./src/gaussians_streamlit_app.py"]
# CMD ["streamlit", "run", "./src/gui_app.py", 'localhost']