# VisualQuant
A reactive web applications to visualize results produced by the
[LEAN](https://github.com/QuantConnect/Lean) engine developed by QuanntConncect, build with [Streamlit](https://streamlit.io/).

## What is Visual Quant

Visual Quant is a local webapp written in python with streamlit.
It allows you to easily run trading algorithms from the browser and
get the results in nice looking visual charts. 

Everything runs localy and the LEAN engine is opensource so you don't need any account at quanntconnect.

The application also features tools to import and download data
from diffrent sources, as the quanntconnect backtesting data can
not be downloaded itself.

## How to use

- Install the LEAN engine and Docker to run it
- Clone this repo
- From the root directory of this repo run `streamlit run src/main.py`
- Configure the path to your engine in Visual Quant