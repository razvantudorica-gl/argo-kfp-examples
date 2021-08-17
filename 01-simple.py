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
    def task_to_get_something() -> int:
        import time

        time.sleep(2)
        print("task_to_get_something")
        return 999

    @task(
        container_image_uri=image_uri,
        cpu_units=1,
        memory_in_gigabytes=1,
        timeout_in_minutes=5,
        secrets=["default"],
        config_maps=["default"],
    )
    def task_dummy(just_something: int):
        print("in task dummy. just_something: ")
        print(just_something)

    @kfp.dsl.pipeline()
    def pipeline():
        my_precious = task_to_get_something()
        task_dummy(my_precious.output)

    return pipeline
