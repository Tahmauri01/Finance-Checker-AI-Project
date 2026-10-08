{
    "name": "load_transactions",
    "description": (
        "Read the csv file and puts each line into a list as a transaction"
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "csv_path": {
                "type": "string",
                "description": "Directory path/file name to the csv file with the transactions listed",
            },
        },
        "required": {
            ["csv_path"]
        }
    }
},
{
    "name": "spending_by_category",
    "description": (),
    "input_schema": {
        "type": "object",
        "properties": {
            "month": {
                "type": "string",
                "description": "The month in a YYYY-MM format. EX: 2026-10"
            },
        },
        "required": {
            ["month"]
        }
    }
},
{
    "name": "compare_months",
    "description": (),
    "input_schema": {
        "type": "object",
        "properties": {

        }
    }
},
{
    "name": "monthly_total",
    "description": (),
    "input_schema": {
        "type": "object",
        "properties": {

        }
    }
},
{
    "name": "least_spending_month",
    "description": (),
    "input_schema": {
        "type": "object",
        "properties": {

        }
    }
},
{
    "name": "highest_spending_month",
    "description": (),
    "input_schema": {
        "type": "object",
        "properties": {

        }
    }
},
{
    "name": "largest_seen",
    "description": (),
    "input_schema": {
        "type": "object",
        "properties": {

        }
    }
},
{
    "name": "recuring_charges",
    "description": (),
    "input_schema": {
        "type": "object",
        "properties": {

        }
    }
},
{
    "name": "find_uncategorized",
    "description": (),
    "input_schema": {
        "type": "object",
        "properties": {

        }
    }
},
{
    "name": "categorize",
    "description": (),
    "input_schema": {
        "type": "object",
        "properties": {

        }
    }
},