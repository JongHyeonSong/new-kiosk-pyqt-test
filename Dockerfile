FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install pyinstaller

# CMD [ "tail", "-f", "/dev/null" ]
CMD [ "pyinstaller", "--noconfirm", "--onedir", "--console", "--add-data", "./static:static/", "app.py" ]

# pyinstaller --noconfirm --onedir --console --add-data "./static:static/"  "app.py"

# docker build -t mypy .


# docker run --rm -v ${PWD}:/app my-python-app
# docker run -itd -v ${PWD}:/app my-python-app
# docker run -itd --name app2 -v ${PWD}:/app my-python-app2

# docker run --rm -v ${PWD}/dockerFolder:/app/dist mypy


# docker run -itd --name my-p -v .\dockerFolder\:/tmp my-p
# docker run -itd --name my-p -v .\dockerFolder\:/app my-p