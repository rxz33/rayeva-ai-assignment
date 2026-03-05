from fastapi import HTTPException, status

VALID_CATEGORIES = {
    "personal_care",
    "kitchen",
    "office_supplies",
    "packaging",
    "home_products",
}


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

    # primary category — must be from predefined list
    if "primary_category" in parsed_json:
        val = parsed_json["primary_category"]
        if not isinstance(val, str) or not val.strip():
            errors.append("primary_category must be a valid string")
        elif val not in VALID_CATEGORIES:
            errors.append(
                f"primary_category '{val}' is not valid. Must be one of: {', '.join(sorted(VALID_CATEGORIES))}"
            )

    # sub category
    if "sub_category" in parsed_json:
        if (
            not isinstance(parsed_json["sub_category"], str)
            or not parsed_json["sub_category"].strip()
        ):
            errors.append("sub_category must be a valid string")

    # seo tags — must be between 5 and 10
    if "seo_tags" in parsed_json:
        seo_tags = parsed_json["seo_tags"]
        if not isinstance(seo_tags, list) or len(seo_tags) == 0:
            errors.append("seo_tags must be a non-empty list")
        elif len(seo_tags) < 5 or len(seo_tags) > 10:
            errors.append(
                f"seo_tags must contain between 5 and 10 tags, got {len(seo_tags)}"
            )
        else:
            for tag in seo_tags:
                if not isinstance(tag, str) or not tag.strip():
                    errors.append("seo_tags must contain valid strings")

    # sustainability filters
    if "sustainability_filters" in parsed_json:
        filters = parsed_json["sustainability_filters"]
        if not isinstance(filters, list):
            errors.append("sustainability_filters must be a list")
        else:
            for item in filters:
                if not isinstance(item, str) or not item.strip():
                    errors.append("sustainability_filters must contain valid strings")

    if errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=errors
        )
