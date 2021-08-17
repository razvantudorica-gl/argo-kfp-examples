import kfp
from kfp.components import InputPath, OutputPath
from kfp_mlp.decorators import task


def build_training_pipeline(
    image_uri: str,
):
    @task(
        container_image_uri=image_uri,
        cpu_units=1,
        memory_in_gigabytes=1,
        timeout_in_minutes=2,
        secrets=["default"],
        config_maps=["default", "debug"],
    )
    def get_countries(output_countries_path: OutputPath()):
        import json
        import time

        time.sleep(2)
        print("Hardcode countries")

        with open(output_countries_path, "w") as outfile:
            json.dump(["GE", "RO", "IT", "ES", "UK"], outfile)

    @task(
        container_image_uri=image_uri,
        cpu_units=1,
        memory_in_gigabytes=1,
        timeout_in_minutes=5,
        secrets=["default"],
        config_maps=["default"],
    )
    def task_dummy(input_file_path: InputPath(), obj_dummy: dict):
        import json

        print("in task dummy")
        print(input_file_path)
        print(obj_dummy)
        with open(input_file_path, "r") as f:
            countries = json.load(f)

        print("we've got countries: ", countries)

    @kfp.dsl.pipeline()
    def pipeline():
        countries_res = get_countries()
        countries_dummy = {"test2": 222}
        task_dummy(countries_res.outputs["output_countries"], countries_dummy)

    return pipeline
