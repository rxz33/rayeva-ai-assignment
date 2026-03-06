from fastapi import HTTPException, status


def validate_impact_output(parsed_json):
    errors = []

    required_fields = ["order_id", "plastic_saved_kg", "carbon_avoided_kg", "local_sourcing_summary", "impact_statement"]
    for field in required_fields:
        if field not in parsed_json:
            errors.append(f"Missing field: {field}")

    for field in ["plastic_saved_kg", "carbon_avoided_kg"]:
        if field in parsed_json:
            if not isinstance(parsed_json[field], (int, float)) or parsed_json[field] < 0:
                errors.append(f"{field} must be a non-negative number")

    for field in ["local_sourcing_summary", "impact_statement"]:
        if field in parsed_json:
            if not isinstance(parsed_json[field], str) or len(parsed_json[field].strip()) < 10:
                errors.append(f"{field} must be meaningful text")

    if errors:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=errors)