cp threads-main.py __main__.py
rm native-app-audit-trail.zip
zip -r native-app-audit-trail.zip __main__.py marketdata.py portfoliodata.py marginBalance.py data/ virtualenv/bin/activate_this.py virtualenv/lib/python3.5/site-packages/yfinance virtualenv/lib/python3.5/site-packages/certifi virtualenv/lib/python3.5/site-packages/chardet virtualenv/lib/python3.5/site-packages/multitasking 

cp mpk-main.py __main__.py
rm mpk-app-audit-trail.zip
zip -r mpk-app-audit-trail.zip __main__.py marketdata.py portfoliodata.py marginBalance.py data/ virtualenv/bin/activate_this.py virtualenv/lib/python3.5/site-packages/yfinance virtualenv/lib/python3.5/site-packages/certifi virtualenv/lib/python3.5/site-packages/chardet virtualenv/lib/python3.5/site-packages/multitasking virtualenv/lib/python3.5/site-packages/mpkmemalloc.cpython-35m-x86_64-linux-gnu.so

cp batching-main.py __main__.py
rm batch-app-audit-trail.zip
zip -r batch-app-audit-trail.zip __main__.py marketdata.py portfoliodata.py marginBalance.py data/ virtualenv/bin/activate_this.py virtualenv/lib/python3.5/site-packages/yfinance virtualenv/lib/python3.5/site-packages/certifi virtualenv/lib/python3.5/site-packages/chardet virtualenv/lib/python3.5/site-packages/multitasking virtualenv/lib/python3.5/site-packages/mpkmemalloc.cpython-35m-x86_64-linux-gnu.so

cp native-batching-main.py __main__.py
rm nativebatch-app-audit-trail.zip
zip -r nativebatch-app-audit-trail.zip __main__.py marketdata.py portfoliodata.py marginBalance.py data/ virtualenv/bin/activate_this.py virtualenv/lib/python3.5/site-packages/yfinance virtualenv/lib/python3.5/site-packages/certifi virtualenv/lib/python3.5/site-packages/chardet virtualenv/lib/python3.5/site-packages/multitasking 
