from django.contrib import admin
from django.urls import reverse

APP_ICONS = {
    "authentication": "person",
    "auth": "group",
    "core": "settings",
    "universe": "public",
    "lore": "auto_stories",
    "manufacturer": "factory",
    "component": "memory",
    "vehicle": "rocket_launch",
    "equipment": "shield",
    "economy": "payments",
}


def get_navigation(request):
    """
    Auto-generate Unfold sidebar navigation grouped by app label.
    Introspects admin.site._registry to build collapsible groups.
    """
    app_groups = {}

    for model, model_admin in admin.site._registry.items():
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        verbose = model._meta.verbose_name_plural.title()

        url_name = f"admin:{app_label}_{model_name}_changelist"
        try:
            link = reverse(url_name)
        except Exception:
            continue

        if not model_admin.has_module_permission(request):
            continue

        if app_label not in app_groups:
            app_groups[app_label] = []

        app_groups[app_label].append(
            {
                "title": verbose,
                "icon": APP_ICONS.get(app_label, "folder"),
                "link": link,
            }
        )

    navigation = []
    for app_label, items in app_groups.items():
        items.sort(key=lambda x: x["title"])
        navigation.append(
            {
                "title": app_label.replace("_", " ").title(),
                "separator": True,
                "collapsible": True,
                "items": items,
            }
        )

    return navigation
