# financial-data-crawler
This contains the code that automatically download financial statement of a stock

Before running the code, follow the steps

1. Download and install the latest Google Chrome release

  $ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

  $ sudo dpkg -i --force-depends google-chrome-stable_current_amd64.deb

2. Download and install the latest amd64 chromedriver release

  $ LATEST=$(wget -q -O - http://chromedriver.storage.googleapis.com/LATEST_RELEASE)

  $ wget http://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip

  $ unzip chromedriver_linux64.zip && sudo ln -s $PWD/chromedriver /usr/local/bin/chromedriver

3. Install selenium

  $  pip install selenium
