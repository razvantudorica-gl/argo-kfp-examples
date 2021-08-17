import kfp

from kfp.dsl import ParallelFor
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
    def get_countries() -> list:
        import time

        time.sleep(2)
        print("Hardcode countries")
        return ["GE", "RO", "IT", "ES", "UK"]

    @task(
        container_image_uri=image_uri,
        cpu_units=2,
        memory_in_gigabytes=1,
        timeout_in_minutes=5,
        secrets=["default"],
        config_maps=["default", "debug"],
    )
    def learn_process(country: str, version: str):
        import time

        print(f"received countries={country}, version: {version}")
        time.sleep(3)

    @task(
        container_image_uri=image_uri,
        cpu_units=1,
        memory_in_gigabytes=1,
        timeout_in_minutes=2,
        secrets=["default"],
        config_maps=["default"],
    )
    def task_save_version(version: str, env: str = "PROD"):
        import time

        time.sleep(2)

        print(f"Saved versions {version} for {env}")

    @kfp.dsl.pipeline()
    def pipeline():

        countries = get_countries()
        with ParallelFor(countries.output) as country:
            learn_result = learn_process(country=country, version="{{ workflow.uid }}")

        task_save_version(version="{{ workflow.uid }}", env="stage").after(learn_result)

    return pipeline
