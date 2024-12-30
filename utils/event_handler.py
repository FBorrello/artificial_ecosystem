def event_handler_factory(event_name: str) -> callable:
    counter = 0
    def event_handler(*args, **kwargs):
        nonlocal counter
        counter += 1
        print(f"Event triggered: {event_name} ({counter} {'time' if counter == 1 else 'times'})")

    return event_handler

click_handler = event_handler_factory("Click Event")
scroll_handler = event_handler_factory("Scroll Event")

click_handler()
scroll_handler()
click_handler()
scroll_handler()
scroll_handler()
scroll_handler()
scroll_handler()
click_handler()