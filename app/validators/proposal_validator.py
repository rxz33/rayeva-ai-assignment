from fastapi import HTTPException, status


def validate_proposal_output(parsed_json, client_budget):

    errors = []

    # required fields
    required_fields = ["product_mix", "budget_allocation", "impact_summary"]

    for field in required_fields:
        if field not in parsed_json:
            errors.append(f"Missing field: {field}")

    # product mix validation
    if "product_mix" in parsed_json:

        product_mix = parsed_json["product_mix"]

        if not isinstance(product_mix, list) or len(product_mix) == 0:
            errors.append("product_mix must be a non-empty list")

        else:
            for item in product_mix:

                if "product" not in item or "quantity" not in item:
                    errors.append("Each product must contain product and quantity")
                    continue

                if not isinstance(item["product"], str) or not item["product"].strip():
                    errors.append("Product name must be a valid string")

                if not isinstance(item["quantity"], int) or item["quantity"] <= 0:
                    errors.append("Quantity must be a positive integer")

    # budget validation
    if "budget_allocation" in parsed_json:

        budget = parsed_json["budget_allocation"]

        required_budget_fields = ["products", "logistics", "buffer"]

        for field in required_budget_fields:
            if field not in budget:
                errors.append(f"Missing budget field: {field}")
            else:
                if not isinstance(budget[field], (int, float)) or budget[field] < 0:
                    errors.append(f"{field} must be a positive number")

        if all(f in budget for f in required_budget_fields):
            total_budget = budget["products"] + budget["logistics"] + budget["buffer"]

            if total_budget > client_budget:
                errors.append("Generated proposal exceeds client budget")

    # impact summary validation
    if "impact_summary" in parsed_json:

        impact_summary = parsed_json["impact_summary"]

        if not isinstance(impact_summary, str) or len(impact_summary.strip()) < 10:
            errors.append("Impact summary must be meaningful text")

    if errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=errors
        )
