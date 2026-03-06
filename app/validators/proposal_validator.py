from fastapi import HTTPException, status


def validate_proposal_output(parsed_json, client_budget):
    errors = []
    required_fields = ["product_mix", "budget_allocation", "impact_summary"]
    for field in required_fields:
        if field not in parsed_json:
            errors.append(f"Missing field: {field}")

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
                if "unit_price" not in item:
                    errors.append(f"Missing unit_price for: {item.get('product','?')}")
                elif (
                    not isinstance(item["unit_price"], (int, float))
                    or item["unit_price"] <= 0
                ):
                    errors.append("unit_price must be a positive number")
                if "total_cost" not in item:
                    errors.append(f"Missing total_cost for: {item.get('product','?')}")
                elif (
                    not isinstance(item["total_cost"], (int, float))
                    or item["total_cost"] <= 0
                ):
                    errors.append("total_cost must be a positive number")

    if "budget_allocation" in parsed_json:
        budget = parsed_json["budget_allocation"]
        required_budget_fields = ["products", "logistics", "buffer"]
        for field in required_budget_fields:
            if field not in budget:
                errors.append(f"Missing budget field: {field}")
            elif not isinstance(budget[field], (int, float)) or budget[field] < 0:
                errors.append(f"{field} must be a positive number")
        if all(
            field in budget and isinstance(budget[field], (int, float))
            for field in required_budget_fields
        ):
            total = sum(budget[f] for f in required_budget_fields)
            if total > client_budget:
                errors.append(
                    f"Proposal total ({total}) exceeds client budget ({client_budget})"
                )

    if "impact_summary" in parsed_json:
        if (
            not isinstance(parsed_json["impact_summary"], str)
            or len(parsed_json["impact_summary"].strip()) < 10
        ):
            errors.append("Impact summary must be meaningful text")

    if errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=errors
        )
