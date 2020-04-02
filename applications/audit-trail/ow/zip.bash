cp portfoliodata.py __main__.py
rm portfoliodata.zip
zip -r portfoliodata.zip __main__.py data/ 

cp marketdata.py __main__.py
rm marketdata.zip
zip -r marketdata.zip __main__.py virtualenv/bin/activate_this.py virtualenv/lib/python3.5/site-packages/certifi virtualenv/lib/python3.5/site-packages/chardet virtualenv/lib/python3.5/site-packages/yfinance virtualenv/lib/python3.5/site-packages/multitasking 
