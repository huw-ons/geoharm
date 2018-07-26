import geocode
import mapping
import boundarycode

if __name__ == "__main__":
    to_run = {
        "libraries": {
            "geocode": {
                "RUN": False,
                "input": "",
                "column": "",
                "columns": ""
            },
            "mapping": {
                "RUN": True,
                "input": "libraries_geo",
                "name": "ADDRESS"
            },
            "boundarycode": {
                "RUN": True,
                "data_input": "libraries_geo",
                "boundary_input": "infuse_lsoa_lyr_2011",
                "map_output": "Y"
            }
        },

        "practices": {
            "geocode": {
                "RUN": False,
                "input": "",
                "column": "",
                "columns": ""
            },
            "mapping": {
                "RUN": True,
                "input": "practices_geo",
                "name": "ADDRESS"
            },
            "boundarycode": {
                "RUN": True,
                "data_input": "practices_geo",
                "boundary_input": "infuse_lsoa_lyr_2011",
                "map_output": "Y"
            }
        },
    }

    for key, value in to_run.items():
        print("Processing {}...".format(key))
        print("="*30)

        if value["geocode"]["RUN"] is True:
            print("\nRunning geocoding...")
            geocode.run()

        else:
            print("\nSkipping geocoding...")

        if value["mapping"]["RUN"] is True:
            print("\nRunning mapping...")
            mapping.run(value["mapping"]["input"], value["mapping"]["name"])

        else:
            print("\nSkipping mapping...")

        if value["boundarycode"]["RUN"] is True:
            print("\nRunning boundary coding...")
            boundarycode.run(value["boundarycode"]["data_input"], value["boundarycode"]["boundary_input"], value["boundarycode"]["map_output"])

        else:
            print("\nSkipping boundary coding...")

        print("\nCompleted {}\n".format(key))