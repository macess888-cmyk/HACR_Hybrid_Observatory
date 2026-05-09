def dependency_observer(state):

    dependencies = {
        "upstream_policy_dependency": state.get("upstream_policy_dependency", False),
        "external_service_dependency": state.get("external_service_dependency", False),
        "human_approval_dependency": state.get("human_approval_dependency", False),
        "queue_dependency": state.get("queue_dependency", False),
        "scheduler_dependency": state.get("scheduler_dependency", False),
        "hidden_dependency": state.get("hidden_dependency", False)
    }

    active_count = 0

    for _, value in dependencies.items():

        if value:
            active_count += 1

    if state.get("hidden_dependency", False):
        status = "SHADOW"

    elif active_count >= 4:
        status = "DENSE_DEPENDENCY"

    elif active_count >= 1:
        status = "DEPENDENT"

    else:
        status = "INDEPENDENT"

    return {
        "status": status,
        "dependencies": dependencies,
        "active_count": active_count
    }