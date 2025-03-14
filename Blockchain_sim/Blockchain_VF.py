# app.py (Complete 8-Stage Version)
from flask import Flask, render_template, jsonify
from datetime import datetime
import hashlib

app = Flask(__name__)

class CanIdentity:
    def __init__(self):
        self.blocks = {
            "CAN-2024-EU-9A8B7C": {
                "stages": {
                    "raw_material": {
                        "visible_to": ["mining_engineer", "sustainability_auditor"],
                        "data": {
                            "material_id": "AL-2024-EU-001",
                            "mine_location": "Vaud, Switzerland",
                            "extraction_date": "2024-03-15",
                            "carbon_footprint": "15.2 kg CO2e",
                            "recycled_content": "72%"
                        }
                    },
                    "smelting": {
                        "visible_to": ["plant_manager", "quality_controller"],
                        "data": {
                            "smelter_id": "SM-EU-AL-0456",
                            "energy_mix": "82% Renewable",
                            "output_purity": "99.89%",
                            "batch_temperature": "720°C"
                        }
                    },
                    "manufacturing": {
                        "visible_to": ["production_manager", "quality_controller"],
                        "data": {
                            "factory": "FAC-EU-CAN-789",
                            "production_line": "Line 5",
                            "coating_type": "Epoxy-Free Polymer",
                            "thickness": "0.21mm",
                            "units_per_minute": 420
                        }
                    },
                    "filling": {
                        "visible_to": ["beverage_producer", "quality_controller"],
                        "data": {
                            "product": "Sparkling Water",
                            "fill_date": datetime.utcnow().date().isoformat(),
                            "batch_id": "BATCH-2024-SW-789",
                            "expiry_date": "2025-03-15"
                        }
                    },
                    "distribution": {
                        "visible_to": ["logistics_manager", "retailer"],
                        "data": {
                            "shipping_method": "Refrigerated Truck",
                            "departure": "2024-03-20T08:00:00Z",
                            "destination": "Brussels Distribution Hub",
                            "temperature_log": "2-4°C maintained"
                        }
                    },
                    "retail": {
                        "visible_to": ["retailer", "consumer"],
                        "data": {
                            "store_id": "BE-BRU-ALDI-045",
                            "shelf_date": "2024-03-22",
                            "price": "€0.85",
                            "promotion": "Buy 2, Get 1 Free"
                        }
                    },
                    "collection": {
                        "visible_to": ["recycling_tech", "municipal_worker"],
                        "data": {
                            "collection_date": "2024-04-15",
                            "sorting_facility": "RecycleHub #45",
                            "contamination_level": "0.2%",
                            "collection_method": "Curbside Pickup"
                        }
                    },
                    "reprocessing": {
                        "visible_to": ["recycling_tech", "sustainability_auditor"],
                        "data": {
                            "reprocessor_id": "RECYCLE-EU-789",
                            "melting_temp": "660°C",
                            "recovery_rate": "98.7%",
                            "new_product": "Bicycle Frame AL-045"
                        }
                    }
                },
                "blockchain_hash": self.generate_hash("CAN-2024-EU-9A8B7C")
            }
        }

    def generate_hash(self, can_id):
        return hashlib.sha256(can_id.encode()).hexdigest()

can_db = CanIdentity()

ROLES = {
    "mining_engineer": {"level": 1, "department": "raw_materials"},
    "plant_manager": {"level": 2, "department": "processing"},
    "production_manager": {"level": 3, "department": "manufacturing"},
    "beverage_producer": {"level": 4, "department": "production"},
    "logistics_manager": {"level": 5, "department": "distribution"},
    "retailer": {"level": 6, "department": "sales"},
    "recycling_tech": {"level": 7, "department": "sustainability"},
    "sustainability_auditor": {"level": 10, "department": "compliance"},
    "quality_controller": {"level": 8, "department": "quality_assurance"},
    "consumer": {"level": 0, "department": "end_user"},
    "municipal_worker": {"level": 9, "department": "waste_management"}
}

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/can/<can_id>/<role>')
def get_can_data(can_id, role):
    if can_id not in can_db.blocks:
        return jsonify({"error": "Can not found"}), 404
    
    if role not in ROLES:
        return jsonify({"error": "Invalid role"}), 400

    filtered_data = {
        "metadata": {
            "can_id": can_id,
            "current_owner": "HydroCan Beverages EU",
            "blockchain_verification": can_db.blocks[can_id]["blockchain_hash"]
        },
        "stages": {}
    }

    for stage, details in can_db.blocks[can_id]["stages"].items():
        if role in details["visible_to"] or ROLES[role]["level"] >= 9:
            filtered_data["stages"][stage] = details["data"]

    return jsonify(filtered_data)

if __name__ == '__main__':
    app.run(debug=True)
