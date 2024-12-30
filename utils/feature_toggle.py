def feature_toggle(feature_name: str, enabled: bool = True) -> callable:
    def decorator(func):
        def wrapper(*args, **kwargs):
            if enabled:
                return func(*args, **kwargs)
            else:
                print(f"Feature '{feature_name}' is disabled.")
        return wrapper
    return decorator

@feature_toggle("Cool Feature", True)
def run_cool_feature():
    print("Cool Feature is running!")


@feature_toggle("Experimental Feature", False)
def run_experimental_feature():
    print("Experimental Feature is running!")


run_cool_feature()

run_experimental_feature()
