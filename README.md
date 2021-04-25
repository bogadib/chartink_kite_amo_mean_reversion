# Chartink Vishal Mehta Mean Reversion Scanner

This python script gets the stocks scanned by Mean Reversion scanner from Vishal Mehta. Once the stocks are available, it places AMO (After Market Order) in Zerodha Trading account using `kiteconnect` APIs.

The scanner can be located on chartink [https://chartink.com/screener/vishal-mehta-mean-reversion](https://chartink.com/screener/vishal-mehta-mean-reversion)

If available stocks are more than 10 then the stocks are sorted according to latest close price _ascending_ and only 10 orders are placed.



## How to use this repository

### Get the code

* Download the repository as zip
* Unzip / extract it in a folder preferably on `D:\trading` Avoid extracting on Desktop
 

### Installation

* Install Python 3.9.4 latest version as of today (25th April 2021)
* It can work on python 3.6 and above but it is not tested

### Virtual Environment Creation

* `python -m pip install virtualenv` on Windows or `python3 -m pip install --user virtualenv` on Linux 
* Go to the folder `D:\trading` and then create virtualenv as `venv` using command as `python -m virtualenv venv` on Windows or `python3 -m virtualenv -p py3 venv` on Linux
* Activate the virtual environment using `.\venv\Scripts\activate` on Windows or `source ./venv/bin/activate` on Linux/Mac. 
* Upgrade packages using command `python -m pip install -U pip wheel setuptools`


* `pip install .\Twisted-21.2.0-py3-none-any.whl` (MANDATORY on Windows, to install kiteconnect successfully.)
* `pip install .\TA_Lib-0.4.19-cp39-cp39-win_amd64.whl` (OPTIONAL on Windows)
* `pip install -r requirements.txt` (NOTE : There is issue while installing pandas on python 3.6.9 downgrade pandas version to 1.1.5)


## Important

* Before running the script, it is very important to generate the `enctoken.txt` file which is used in `config.py` file
* There are 2 ways to do this
    1. Copy Paste the enctoken from Zerodha Web Session using Chrome DevTools, check images in useful snapshots
    2. Another way to do this is to run the `login_and_generate_enctoken.py` script, this must be done once. 
       May have to run again if you invalidate the session.
       Run this again if you face any issues.
       This step will invalidate your web session if you have logged in through browser.


### Running the Script

* Before running the actual script `chartink_kite.py` you must create .env file same folder
* Copy the .env.example file or rename it to create a new .env file in the same folder
* Change the values for USERNAME, PASSWORD and PIN with your own credentials
* Finally you can run the script using `python chartink.py` or `python3 chartink.py`

## Note

* Some lines are commented since this code is not tested in Live Market
* Stop Loss for the Strategy is not implemented in the script, **3%** Stop Loss recommended by Vishal Mehta, people have posted that **4%** works better but some people keep Stop Loss based on their own Risk e.g. **2%** to **2.5%**
* Similarly, Target or Profit must be kept accordingly to your own Risk Management. Vishal Mehta recommends **6%** while some keep it at **4.5%** 
* Also, some people exit when the overall MTM / PnL reaches approximately **5%** or **6%** of invested capital.
* More images will be added in future. Please check existing images.
* Coding is still in progress, for any suggestions please open discussions [here](https://github.com/algo2t/chartink_kite_amo_mean_reversion/discussions/1#discussion-3336072).


### Useful snapshots

* Cloning repository, creating virutalenv and installing packages
  
  ![2021-04-25 05_01_48-WSL-Ubuntu](https://user-images.githubusercontent.com/73125182/115976343-aeb37b00-a58a-11eb-964f-c547cc329aac.png)

* Activating Virtual environment venv
  
  ![image](https://user-images.githubusercontent.com/73125182/115976649-aad52800-a58d-11eb-95cb-e919bc7850d0.png)

* Installing all requirements from `requirements.txt` using pip
  
  ![image](https://user-images.githubusercontent.com/73125182/115976685-fee00c80-a58d-11eb-93eb-92c55cbab47a.png)
  
  ![image](https://user-images.githubusercontent.com/73125182/115976708-57afa500-a58e-11eb-853a-2b3bbd8d0763.png)

* Below images there is an error which occurred because the session was expired. New enctoken was added to `enctoken.txt` file
  
  ![image](https://user-images.githubusercontent.com/73125182/115976802-4adf8100-a58f-11eb-8d26-0477e9083c9f.png)

* Getting the enctoken from the kite dashboard using Chrome DevTool. Copy paste it to enctoken.txt
  This will help to keep both web session running and script execution will not invalidate web session

  ![image](https://user-images.githubusercontent.com/73125182/115994306-15b94a00-a5f4-11eb-972e-41e9f1ad1a0f.png)


* Kite dashboard orders page before placing AMO orders.
 
 ![image](https://user-images.githubusercontent.com/73125182/115976365-f0442600-a58a-11eb-8e6f-19e2bd29a773.png)

* Executing script and checking output in console

  ![image](https://user-images.githubusercontent.com/73125182/115976385-2f727700-a58b-11eb-948c-83546fc1a2dd.png)

  ![image](https://user-images.githubusercontent.com/73125182/115976391-42854700-a58b-11eb-96a1-37ae39dcc1ab.png)

* Finally checking the orders on the kite dashboard

  ![image](https://user-images.githubusercontent.com/73125182/115976373-110c7b80-a58b-11eb-9f25-fadd2f7c5f15.png)
  


