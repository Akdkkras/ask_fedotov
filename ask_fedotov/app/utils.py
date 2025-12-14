from .models import Tag


def parse_tags(tags_str):
    """
    Converts a string of tags separated by commas into a list of Tag objects.
    """
    tag_names = [t.strip() for t in tags_str.split(",") if t.strip()]
    if not tag_names:
        return []

    existing_tags = Tag.objects.filter(name__in=tag_names)
    existing_names = set(tag.name for tag in existing_tags)

    new_names = [name for name in tag_names if name not in existing_names]
    new_tags = [Tag(name=name) for name in new_names]

    if new_tags:
        Tag.objects.bulk_create(new_tags)

    all_tags = list(existing_tags) + new_tags
    return all_tags
