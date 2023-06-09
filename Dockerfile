FROM python:3.9-buster

WORKDIR /scraper





# RUN mkdir tmp
# RUN cd tmp

# RUN apt update
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN apt install -y ./google-chrome-stable_current_amd64.deb



# RUN wget https://chromedriver.storage.googleapis.com/113.0.5672.63/chromedriver_linux64.zip
# RUN unzip chromedriver_linux64.zip
# RUN mv chromedriver /usr/bin/chromedriver


COPY requirements.txt .

COPY credentials.json credentials.json
COPY setup.py setup.py
COPY pyproject.toml pyproject.toml
COPY README.md README.md
COPY src src

ENV SCRAPER_CREDS /scraper/credentials.json


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set the build command
RUN pip install -e .



ENTRYPOINT [ "bash" ]
# CMD ["upwork_scraper", "main"]


# google-chrome --no-sandbox --version  && which google-chrome
