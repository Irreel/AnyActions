


def getVehicleDetailsByRegistrationNumber(, data):
    """Get vehicle details by registration number"""
    import requests
    url = f"https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"
    
    
    
    
    
    
    
    params = {
        
        
        
        
        
        
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

