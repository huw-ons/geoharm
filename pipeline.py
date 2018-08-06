import logger
import geocode
import mapping
import boundarycode
import aggregate
import merger

if __name__ == "__main__":
    log = logger.get_logger("pipeline.py")

    to_run_lsoa = {
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
            },
            "aggregate": {
                "RUN": True,
                "input": "libraries_boundaries",
                "boundary": "infuse_lsoa_lyr_2011"
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
            },
            "aggregate": {
                "RUN": True,
                "input": "practices_boundaries",
                "boundary": "infuse_lsoa_lyr_2011"
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
            },
            "aggregate": {
                "RUN": True,
                "input": "worship_boundaries",
                "boundary": "infuse_lsoa_lyr_2011"
            }
        },
    }

    to_run_msoa = {
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
                "boundary_input": "infuse_msoa_lyr_2011_clipped",
                "map_output": "Y"
            },
            "aggregate": {
                "RUN": True,
                "input": "libraries_boundaries",
                "boundary": "infuse_msoa_lyr_2011_clipped"
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
                "boundary_input": "infuse_msoa_lyr_2011_clipped",
                "map_output": "Y"
            },
            "aggregate": {
                "RUN": True,
                "input": "practices_boundaries",
                "boundary": "infuse_msoa_lyr_2011_clipped"
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
                "boundary_input": "infuse_msoa_lyr_2011_clipped",
                "map_output": "Y"
            },
            "aggregate": {
                "RUN": True,
                "input": "worship_boundaries",
                "boundary": "infuse_msoa_lyr_2011_clipped"
            }
        },
    }

    to_run_la = {
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
                "boundary_input": "infuse_dist_lyr_2011_clipped",
                "map_output": "Y"
            },
            "aggregate": {
                "RUN": True,
                "input": "libraries_boundaries",
                "boundary": "infuse_dist_lyr_2011_clipped"
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
                "boundary_input": "infuse_dist_lyr_2011_clipped",
                "map_output": "Y"
            },
            "aggregate": {
                "RUN": True,
                "input": "practices_boundaries",
                "boundary": "infuse_dist_lyr_2011_clipped"
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
                "boundary_input": "infuse_dist_lyr_2011_clipped",
                "map_output": "Y"
            },
            "aggregate": {
                "RUN": True,
                "input": "worship_boundaries",
                "boundary": "infuse_dist_lyr_2011_clipped"
            }
        },
    }

    runnables = [to_run_lsoa, to_run_msoa, to_run_la]

    log.info("{} boundary levels to be run\n\n".format(len(runnables)))

    i = 0

    for to_run in runnables:
        i = i + 1
        log.info("Boundary #{}".format(i))

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

            if value["aggregate"]["RUN"] is True:
                aggregate.run(value["aggregate"]["input"], value["aggregate"]["boundary"])

            else:
                log.info("Skipping aggregating...")

            log.info("Completed {}\n".format(key))

        merger.run(list(to_run.keys()), to_run[list(to_run.keys())[0]]["aggregate"]["boundary"])

        log.info("Boundary #{} completed\n\n".format(i))