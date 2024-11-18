import pandas
import scikitlearn
import ao_log
import requests
import datetime
def data_get(url:str, instrument_key: str, interval:str, to_date: datetime.date, from_date: datetime.date|None = None, ):
    """
    Here's a sample response from the upstox historical candle data API. 
    base url: https://api.upstox.com/v2/historical-candle/:instrument_key/:interval/:to_date/:from_date
    {"status": "success","data": {"candles": [["2023-10-01T00:00:00+05:30",53.1,53.95,51.6,j52.05,235519861,0],["2023-09-01T00:00:00+05:30",50.35,56.85,49.35,52.8,1004998611,0]]}}
    
    """
    log_con = log_con_create()
    
    headers = {"Accept": "application/json"}
    if from_date != None:
        params = {
            "instrument_key": instrument_key,
            "interval": interval,
            "to_date": to_date,
            "from_date": from_date
        }
    else:
        params = {
            "instrument_key": instrument_key,
            "interval": interval,
            "to_date": to_date,
        }
    try: api_response = requests.get(url, params=params) 
    except Exception as e:
        error = f"ERROR: {__name__}.rest_data_get() failed api call to url={url}. | DEBUG: {e}"
        add_err(log_con, error)
    
    if (api_response.status_code != 200) or (api_response.status_code != 201):
        error = f"ERROR: {__name__}.rest_data_get() api call returned a non-200 level http code. | DEBUG: {api_response.text}"

    return api_response, log_con


def main(log_level):
    log_con = log_con_create()
    api_response, log_con_temp= data_get(**data_config)
    log_con_transfer(log_con_temp, log_con)
    if check_error(log_con): 
        error = f"FATAL: Failed to get data from the internet api."
        log_con_dump(log_con)

    return 0
if __name__ == "__main__":
    debug = main(1)
    if debug != 0:
        log(f"ERROR: {__name__}.main() returned non-zero exit code")