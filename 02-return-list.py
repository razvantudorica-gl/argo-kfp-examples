import kfp
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
    def task_get_countries() -> list:
        import time

        time.sleep(2)
        print("Hardcode countries")
        return ["GE", "RO", "IT", "ES", "UK"]

    @task(
        container_image_uri=image_uri,
        cpu_units=1,
        memory_in_gigabytes=1,
        timeout_in_minutes=5,
        secrets=["default"],
        config_maps=["default"],
    )
    def task_dummy(something: list):
        print("in task dummy, something:")
        print(something)

    @kfp.dsl.pipeline()
    def pipeline():
        my_other_precious = task_get_countries()
        task_dummy(my_other_precious.output)

    return pipeline
