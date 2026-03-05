from fastapi import HTTPException, status


def validate_category_output(parsed_json):

    errors = []

    required_fields = [
        "primary_category",
        "sub_category",
        "seo_tags",
        "sustainability_filters",
    ]

    # required fields
    for field in required_fields:
        if field not in parsed_json:
            errors.append(f"Missing field: {field}")

    # category validation
    if "primary_category" in parsed_json:
        if (
            not isinstance(parsed_json["primary_category"], str)
            or not parsed_json["primary_category"].strip()
        ):
            errors.append("primary_category must be a valid string")

    if "sub_category" in parsed_json:
        if (
            not isinstance(parsed_json["sub_category"], str)
            or not parsed_json["sub_category"].strip()
        ):
            errors.append("sub_category must be a valid string")

    # seo tags validation
    if "seo_tags" in parsed_json:

        seo_tags = parsed_json["seo_tags"]

        if not isinstance(seo_tags, list) or len(seo_tags) == 0:
            errors.append("seo_tags must be a non-empty list")

        else:
            for tag in seo_tags:
                if not isinstance(tag, str) or not tag.strip():
                    errors.append("seo_tags must contain valid strings")

    # sustainability filters validation
    if "sustainability_filters" in parsed_json:

        filters = parsed_json["sustainability_filters"]

        if not isinstance(filters, list):
            errors.append("sustainability_filters must be a list")

        else:
            for item in filters:
                if not isinstance(item, str) or not item.strip():
                    errors.append("sustainability_filters must contain valid strings")

    # return validation errors
    if errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=errors
        )
