import requests


def get_data():
    json_data = requests.get("https://www.sofascore.com/tournament/1462/13415/standings/tables/json")

    data = json_data.json()
    standings = data['standingsTables'][0]
    print(standings)
    info = standings['name']
    print(len(info))
    rows = standings['tableRows']
    print(len(rows))
    print(rows)
    print(info)
    pass


if __name__ == '__main__':
    get_data()