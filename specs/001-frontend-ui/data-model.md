# Data Model: Computer Parts Pricing Application

## Entities

### ComputerPart
- **Description**: Represents a single computer component with attributes including part name, price information, and source details
- **Fields**:
  - `name` (string): Name of the computer part (e.g., "RTX5070", "64GB-DDR5-RAM")
  - `category` (string): Category/type of the component (e.g., "GPU", "RAM", "CPU")
  - `specifications` (dict): Additional specifications metadata about the part
- **Relationships**: 
  - Connected to multiple PriceRecords through a one-to-many relationship

### PriceRecord
- **Description**: Contains pricing data for a specific part from various sources, including minimum, maximum, and average prices  
- **Fields**:
  - `part_name` (string): Name of the computer part this record relates to
  - `source` (string): Source/provider of the price information (e.g., "amazon_search")
  - `price_value` (float): The actual numeric price value after cleaning and processing 
  - `timestamp` (datetime): When the price data was retrieved
  - `currency` (string): Currency code for the price (default: "GBP")
- **Relationships**:
  - Connected to one ComputerPart through a many-to-one relationship

### UserInput
- **Description**: Collection of computer parts entered by the user for price calculation
- **Fields**:
  - `parts_list` (list of strings): List of part names/queries entered by the user
  - `geo_location` (string): Geographic location setting for price queries (default: "GB")
  - `parse_enabled` (boolean): Whether to parse additional data from sources
  - `timestamp` (datetime): When the input was submitted
- **Relationships**:
  - Connected to one or more ComputerParts through a many-to-many relationship

## Relationships
1. UserInput → ComputerPart: Many-to-many (a user can enter multiple parts, and each part may appear in multiple inputs)
2. ComputerPart → PriceRecord: One-to-many (each computer part has many price records from different sources)

## Validation Rules
- `name` field in ComputerPart must be non-empty string
- `price_value` in PriceRecord must be a positive numeric value
- `parts_list` in UserInput must not be empty and contain valid part names
- All timestamps should be properly formatted datetime objects

## State Transitions 
No explicit state transitions defined for this data model, as the application primarily focuses on processing inputs to generate pricing results rather than maintaining complex states.
