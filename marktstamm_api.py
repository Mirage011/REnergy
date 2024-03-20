import requests
import json

#https://www.marktstammdatenregister.de/MaStR/Einheit/EinheitJson/GetErweiterteOeffentlicheEinheitStromerzeugung?sort=Spalte&page=1&pageSize=10&filter=Betriebs-Status~eq~37
def get_betribs_by_status(status=37, pageSize=5, page=3):

    base_url = "https://www.marktstammdatenregister.de/MaStR/Einheit/EinheitJson/GetErweiterteOeffentlicheEinheitStromerzeugung"
    params = {
        "filter": f"Betriebs-Status~eq~{status}"
        ,"pageSize": pageSize
        ,"page": page
    }
    response = requests.get(
       base_url
       ,params = params 
    )
    print(response.request.path_url)
    return response.json()

## change 
data_response = get_betribs_by_status(status=31, pageSize=7, page=1)["Data"]
print(f"Returned {len(data_response)} elements")
print("AnlagenbetreiberId: ", data_response[0]["AnlagenbetreiberId"])
print("BetriebsStatusId: ", data_response[0]["BetriebsStatusId"])