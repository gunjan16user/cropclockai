---
name: cropclock
description: CropClock Multiagent System capability skill. Exposes agronomical visual classification, shelf life decay simulations, buyer directory matching, and localized SMS compilers.
---

# CropClock Multiagent Agronomy Skill

This skill registers the CropClock capability with the Antigravity agentic engine.

## Exposed Capabilities (MCP Tools)

The skill registers 5 dynamic tools loaded through the MCP server:

1. **`fetch_weather_vectors`**
   - **Description**: Fetches ambient temperature and humidity for a coordinate pair or location indicator string using real-time Open-Meteo queries.
   - **Arguments**: `{ location_string: str, coordinates: list[float] }`
   - **Returns**: `{ ambient_temperature_c: float, relative_humidity_pct: float }`

2. **`calculate_shelf_life`**
   - **Description**: Evaluates base agronomical preservation curves and applies physiological high-heat penalties (1.5h/°C above 30°C) and storage deficits (28% cut).
   - **Arguments**: `{ crop_type: str, condition_index: float, temp_c: float, humidity_pct: float }`
   - **Returns**: `{ remaining_marketable_hours: int, degradation_rate_curve: str }`

3. **`query_buyer_directory`**
   - **Description**: Maps current location coordinates against active wholesale APMC yards and agri-tech aggregators, dynamically resolved using geocoding directories. Under low shelf life, it automatically restricts transport distance to nearby entities only.
   - **Arguments**: `{ current_location: str, max_radius_km: float }`
   - **Returns**: `{ buyers_list: list }`

4. **`get_market_prices`**
   - **Description**: Retrieves live wholesale spot prices for target buyers and crops.
   - **Arguments**: `{ buyer_id: str, crop_type: str }`
   - **Returns**: `{ wholesale_price_per_unit: float, currency_code: str }`

5. **`log_consented_loss`**
   - **Description**: Telemetry logging tool for crop loss prevention tracking. Evaluates consent status before writing.
   - **Arguments**: `{ crop_type: str, calculated_loss_prevented_kg: float, region_id: str }`
   - **Returns**: `{ logging_status: str }`
