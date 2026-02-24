"""Takes JSON files from current kmnr.org about shows and DJs and combines them to create a JSON file of data that is easier to work with for this website/schema."""

import json


DAYS = {
    "Su": "Sunday",
    "Mo": "Monday",
    "Tu": "Tuesday",
    "We": "Wednesday",
    "Th": "Thursday",
    "Fr": "Friday",
    "Sa": "Saturday",
}

F25 = {"term": "Fall", "year": 2025}


def main():
    try:
        with open("f25_shows_w_hosts.json", "r") as file:
            shows_data = json.load(file)

        with open("f25_djs.json", "r") as file:
            djs_data = json.load(file)

    except FileNotFoundError:
        print("Error: The file was not found.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from the file.")
        return

    print(f"There are {len(shows_data)} shows and {len(djs_data)} DJs")

    djs = dict()
    for dj in djs_data:
        djs[dj["id"]] = dj

    shows = []
    for show in shows_data:
        new_show = dict()
        new_show["id"] = show["id"]
        new_show["name"] = show["name"]
        new_show["shortDesc"] = show["short_desc"]
        new_show["day"] = DAYS.get(show["day"])
        new_show["startTime"] = show["start_time"]
        new_show["endTime"] = show["end_time"]
        new_show["semester"] = F25

        host_id = show["host"]
        host = djs.get(host_id)
        new_host = {
            "id": host["id"],
            "djName": host["djName"],
            "userName": "John Doe",
            "profileImg": None,
        }

        new_show["hosts"] = [new_host]

        shows.append(new_show)

    print(f"Reformatted {len(shows)} shows")

    with open("migrated_shows.json", "w") as out_file:
        json.dump(shows, out_file)


if __name__ == "__main__":
    main()
