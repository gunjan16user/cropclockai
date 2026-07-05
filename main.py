from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os
import sys
import re

app = FastAPI(title="CropClockAI Web Server")

# Image analysis helper: dynamic metadata extractor representing Google Search Vision
def classify_crop_by_metadata(filename: str) -> dict:
    name = filename.lower()
    # Strip extension
    name = os.path.splitext(name)[0]
    # Replace separators with spaces
    name = re.sub(r'[-_]', ' ', name)
    # Remove numbers
    name = re.sub(r'\d+', '', name)
    
    # Common words to filter out
    words_to_strip = [
        "organic", "fresh", "farm", "photo", "ripe", "decayed", "healthy", 
        "image", "upload", "capture", "crop", "picture", "harvest", "field", 
        "garden", "local", "premium", "quality", "raw", "freshly", "picked"
    ]
    for word in words_to_strip:
        name = re.sub(rf'\b{word}\b', '', name)
    
    # Clean spacing
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Capitalize the remaining crop name
    crop_type = name.title() if name else "Generic Crop"
    
    # Dynamically determine category based on a broad dictionary of common crops
    category = "General Crop"
    classification = f"Species of {crop_type}"
    condition_index = 0.40
    
    lower_crop = crop_type.lower()
    
    # Fruits classification dictionary
    fruits = [
        "apple", "banana", "mango", "orange", "lemon", "lime", "citrus", 
        "grape", "strawberry", "pear", "peach", "plum", "apricot", "cherry", 
        "pineapple", "papaya", "watermelon", "melon", "pomegranate", "fig",
        "guava", "lychee", "kiwi", "avocado", "coconut", "jackfruit", "sweet lime"
    ]
    # Vegetables classification dictionary
    vegetables = [
        "tomato", "potato", "onion", "spinach", "carrot", "garlic", "chili", 
        "pepper", "capsicum", "cabbage", "broccoli", "cauliflower", "lettuce", 
        "cucumber", "eggplant", "aubergine", "okra", "bhindi", "peas", "bean",
        "radish", "turnip", "beetroot", "ginger", "squash", "pumpkin"
    ]
    # Grains classification dictionary
    grains = [
        "wheat", "rice", "paddy", "barley", "oat", "corn", "maize", "millet", 
        "sorghum", "rye", "quinoa", "buckwheat"
    ]
    
    if any(f in lower_crop for f in fruits):
        category = "Fruit"
        classification = f"Fruit Species ({crop_type})"
        if "lime" in lower_crop or "lemon" in lower_crop or "citrus" in lower_crop:
            classification = f"Citrus Fruit ({crop_type})"
    elif any(v in lower_crop for v in vegetables):
        category = "Vegetable"
        classification = f"Vegetable Species ({crop_type})"
    elif any(g in lower_crop for g in grains):
        category = "Grain"
        classification = f"Agricultural Grain ({crop_type})"
        condition_index = 0.10
        
    return {
        "crop_type": crop_type,
        "category": category,
        "classification": classification,
        "condition_index": condition_index
    }

# Serve the Single Page Application assets directly
@app.get("/")
async def get_index():
    return FileResponse("index.html")

@app.get("/app.js")
async def get_js():
    return FileResponse("app.js")

@app.get("/styles.css")
async def get_css():
    return FileResponse("styles.css")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "cropclock-agronomy"}

# Live API endpoints to run the Python ADK Agents and MCP tools in the Cloud Run container!
@app.get("/api/mcp/weather")
async def run_weather_tool(lat: float, lon: float):
    # Dynamically import helper from agents directory
    sys.path.append(os.path.join(os.path.dirname(__file__), ".agents", "skills", "cropclock", "scripts"))
    try:
        from cropclock_agents import tool_fetch_weather_vectors
        result = tool_fetch_weather_vectors("", [lat, lon])
        return {"status": "success", "tool": "fetch_weather_vectors", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/mcp/buyers")
async def run_buyers_tool(lat: float, lon: float, radius: float = 50.0):
    sys.path.append(os.path.join(os.path.dirname(__file__), ".agents", "skills", "cropclock", "scripts"))
    try:
        from mcp_server import tool_query_buyer_directory
        loc_str = f"GPS Coordinates [{lat}, {lon}]"
        result = tool_query_buyer_directory(loc_str, radius)
        return {"status": "success", "tool": "query_buyer_directory", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/classify")
async def classify_image(file: UploadFile = File(...)):
    try:
        result = classify_crop_by_metadata(file.filename)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

