import logger
import geocode
import mapping
import boundarycode


if __name__ == "__main__":
    log = logger.get_logger("pipeline.py")

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

        "worship": {
            "geocode": {
                "RUN": False,
                "input": "",
                "column": "",
                "columns": ""
            },
            "mapping": {
                "RUN": True,
                "input": "worship_geo",
                "name": "ADDRESS"
            },
            "boundarycode": {
                "RUN": True,
                "data_input": "worship_geo",
                "boundary_input": "infuse_lsoa_lyr_2011",
                "map_output": "Y"
            }
        },

        "community": {
            "geocode": {
                "RUN": False,
                "input": "",
                "column": "",
                "columns": ""
            },
            "mapping": {
                "RUN": True,
                "input": "community_geo",
                "name": "ADDRESS"
            },
            "boundarycode": {
                "RUN": True,
                "data_input": "community_geo",
                "boundary_input": "infuse_lsoa_lyr_2011",
                "map_output": "Y"
            }
        },

        # "pubs": {
        #     "geocode": {
        #         "RUN": False,
        #         "input": "",
        #         "column": "",
        #         "columns": ""
        #     },
        #     "mapping": {
        #         "RUN": True,
        #         "input": "pubs_geo",
        #         "name": ""
        #     },
        #     "boundarycode": {
        #         "RUN": True,
        #         "data_input": "pubs_geo",
        #         "boundary_input": "infuse_lsoa_lyr_2011",
        #         "map_output": "Y"
        #     }
        # },
    }

    for key, value in to_run.items():
        log.info("Processing {}...".format(key))

        if value["geocode"]["RUN"] is True:
            geocode.run()

        else:
            log.info("Skipping geocoding...")

        if value["mapping"]["RUN"] is True:
            mapping.run(value["mapping"]["input"], value["mapping"]["name"])

        else:
            log.info("Skipping mapping...")

        if value["boundarycode"]["RUN"] is True:
            boundarycode.run(value["boundarycode"]["data_input"], value["boundarycode"]["boundary_input"], value["boundarycode"]["map_output"])

        else:
            log.info("Skipping boundary coding...")

        log.info("Completed {}\n".format(key))