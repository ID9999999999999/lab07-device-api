from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

devices = []

class Device(BaseModel):
    name: str
    energy_usage: int
    status: str
    location: str

@app.get("/")
def home():
    return {"message": "Smart Building Device API"}

@app.get("/devices")
def get_devices(status: str = None):
    if status:
        return [d for d in devices if d["status"] == status]
    return devices

@app.post("/devices")
def add_device(device: Device):
    new_device = device.dict()
    new_device["id"] = len(devices) + 1
    devices.append(new_device)
    return new_device

@app.get("/devices/{device_id}")
def get_device(device_id: int):
    for device in devices:
        if device["id"] == device_id:
            return device
    return {"error": "Device not found"}

@app.delete("/devices/{device_id}")
def delete_device(device_id: int):
    for device in devices:
        if device["id"] == device_id:
            devices.remove(device)
            return {"message": "Device deleted"}
    return {"error": "Device not found"}
@app.get("/energy/total")
def total_energy():
    total = sum(device["energy_usage"] for device in devices)
    return {"total_energy_usage": total}
