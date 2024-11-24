


def CompanyAnnouncement(id):
    """Retrieves announcement data"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/announcement/{id}"
    
    
    
    url = url.format(id=id)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanyDeepsearchISIN(data):
    """Retrieves a list of stock exchange listings"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/deepsearch/isin"
    
    params = {
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanyDeepsearchLEI(number, page):
    """Retrieves a list of companies"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/deepsearch/lei/{number}"
    
    
    
    url = url.format(number=number)
    
    
    
    
    
    params = {
        
        
        
        
        
        "page": page,
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanyDeepsearchName(country, name):
    """Retrieves a list of companies from the official business register"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/deepsearch/name/{country}/{name}"
    
    
    
    url = url.format(country=country)
    
    
    
    url = url.format(name=name)
    
    
    
    params = {
        
        
        
        
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanyDeepsearchNumber(country, number):
    """Retrieves a list of companies from the official business register"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/deepsearch/number/{country}/{number}"
    
    
    
    url = url.format(country=country)
    
    
    
    url = url.format(number=number)
    
    
    
    params = {
        
        
        
        
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanyMonitorChangeTypesList():
    """Get available ChangeTypes"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/monitoring/changeTypes"
    
    params = {
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanyMonitorList():
    """Retrieves a list of registered monitors"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/monitoring/list"
    
    params = {
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanyMonitorId(id):
    """Get monitor status for specific company id"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/monitoring/list/{id}"
    
    
    
    url = url.format(id=id)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanyMonitorRegister(id, data):
    """Register a Company for monitoring"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/monitoring/register/{id}"
    
    
    
    url = url.format(id=id)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanyMonitorUnregister(id):
    """Deactivates an active notification"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/monitoring/unregister/{id}"
    
    
    
    url = url.format(id=id)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = None
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanyNotificationList():
    """Retrieves a list of registered notifications"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/notification/list"
    
    params = {
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanyNotificationId(id):
    """Retrieves a list of registered notifications"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/notification/list/{id}"
    
    
    
    url = url.format(id=id)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanyNotificationRegister(id, data):
    """Creates a new notification"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/notification/register/{id}"
    
    
    
    url = url.format(id=id)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanyNotificationUnregister(id):
    """Unregister a company from Monitoring"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/notification/unregister/{id}"
    
    
    
    url = url.format(id=id)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = None
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanySearchName(country, name, limit):
    """Retrieves a list of companies from the KYC API company index"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/search/name/{country}/{name}"
    
    
    
    url = url.format(country=country)
    
    
    
    url = url.format(name=name)
    
    
    
    
    
    params = {
        
        
        
        
        
        
        
        "limit": limit,
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanySearchNumber(country, number, limit):
    """Retrieves a list of companies from the KYC API company index"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/search/number/{country}/{number}"
    
    
    
    url = url.format(country=country)
    
    
    
    url = url.format(number=number)
    
    
    
    
    
    params = {
        
        
        
        
        
        
        
        "limit": limit,
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanyAlternativeSearch(country, data):
    """Retrieves a list of companies from the KYC API company index"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/search/{country}"
    
    
    
    url = url.format(country=country)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanyIdAnnouncements(id, limit, offset, data):
    """Retrieves company announcements"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/{id}/announcements"
    
    
    
    url = url.format(id=id)
    
    
    
    
    
    
    
    
    
    params = {
        
        
        
        
        
        "limit": limit,
        
        
        
        "offset": offset,
        
        
        
        "data": data,
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanyIdSuper(id, country, lang):
    """Retrieves structured data extracted from a company document"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/{id}/super/{country}"
    
    
    
    url = url.format(id=id)
    
    
    
    url = url.format(country=country)
    
    
    
    
    
    params = {
        
        
        
        
        
        
        
        "lang": lang,
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def CompanyIdDataset(id, check_stock_listing, dataset, lang):
    """Retrieves company details"""
    import requests
    url = f"https://api.kompany.com//api/v1/company/{id}/{dataset}"
    
    
    
    url = url.format(id=id)
    
    
    
    
    
    url = url.format(dataset=dataset)
    
    
    
    
    
    params = {
        
        
        
        
        
        "check_stock_listing": check_stock_listing,
        
        
        
        
        
        "lang": lang,
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def EinVerificationBasic(ein):
    """Verifies an EIN number"""
    import requests
    url = f"https://api.kompany.com//api/v1/ein-verification/basic-check"
    
    
    
    
    
    params = {
        
        
        
        "ein": ein,
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def EinVerificationComprehensive(ein):
    """Verifies EIN number and retrieves company data"""
    import requests
    url = f"https://api.kompany.com//api/v1/ein-verification/comprehensive-check"
    
    
    
    
    
    params = {
        
        
        
        "ein": ein,
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def EinVerificationLookup(name, state, zip, tight):
    """Retrieves a list of EIN numbers"""
    import requests
    url = f"https://api.kompany.com//api/v1/ein-verification/lookup"
    
    
    
    
    
    
    
    
    
    
    
    params = {
        
        
        
        "name": name,
        
        
        
        "state": state,
        
        
        
        "zip": zip,
        
        
        
        "tight": tight,
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def IbanBasic(data):
    """Checks validity of an IBAN number"""
    import requests
    url = f"https://api.kompany.com//api/v1/iban-verification/check-iban"
    
    params = {
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def IbanComprehensive(data):
    """Checks validity of an IBAN number"""
    import requests
    url = f"https://api.kompany.com//api/v1/iban-verification/comprehensive-check-iban"
    
    params = {
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def NifBasic(country, data):
    """Verifies a NIF number"""
    import requests
    url = f"https://api.kompany.com//api/v1/nif-verification/basic-check/{country}"
    
    
    
    url = url.format(country=country)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def NifComprehensive(country, data):
    """Verifies a NIF number and retrieves company data"""
    import requests
    url = f"https://api.kompany.com//api/v1/nif-verification/comprehensive-check/{country}"
    
    
    
    url = url.format(country=country)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def PepMonitorList():
    """Retrieves a list of monitor entries"""
    import requests
    url = f"https://api.kompany.com//api/v1/pepsanction/monitor/list"
    
    params = {
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def PepMonitorUnregister(id):
    """Deactive a pep sanction monitor"""
    import requests
    url = f"https://api.kompany.com//api/v1/pepsanction/monitor/unregister/{id}"
    
    
    
    url = url.format(id=id)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = None
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def PepMonitorUpdate(id, data):
    """Update details of active Pep Sanction monitor"""
    import requests
    url = f"https://api.kompany.com//api/v1/pepsanction/monitor/update/{id}"
    
    
    
    url = url.format(id=id)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def PepOrder(type, search, data):
    """Orders a new Pep Sanction Check Report"""
    import requests
    url = f"https://api.kompany.com//api/v1/pepsanction/order/{type}/{search}"
    
    
    
    url = url.format(type=type)
    
    
    
    url = url.format(search=search)
    
    
    
    params = {
        
        
        
        
        
        
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def PepRetrieve(id):
    """Returns a json or pdf report"""
    import requests
    url = f"https://api.kompany.com//api/v1/pepsanction/retrieve/{id}"
    
    
    
    
    
    url = url.format(id=id)
    
    
    
    params = {
        
        
        
        
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def ProductAvailability(sku, subjectId):
    """Retrieves a document availability result"""
    import requests
    url = f"https://api.kompany.com//api/v1/product/availability/{sku}/{subjectId}"
    
    
    
    url = url.format(sku=sku)
    
    
    
    url = url.format(subjectId=subjectId)
    
    
    
    params = {
        
        
        
        
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def ProductCatalog(country):
    """Returns a catalog of products"""
    import requests
    url = f"https://api.kompany.com//api/v1/product/catalog/{country}"
    
    
    
    url = url.format(country=country)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def ProductNotifier(notifierId):
    """Returns metadata for a notifier"""
    import requests
    url = f"https://api.kompany.com//api/v1/product/notifier/{notifierId}"
    
    
    
    url = url.format(notifierId=notifierId)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def ProductNotifierCreate(orderId, type, uri):
    """Creates a notifier for an order"""
    import requests
    url = f"https://api.kompany.com//api/v1/product/notifier/{orderId}/{type}/{uri}"
    
    
    
    url = url.format(orderId=orderId)
    
    
    
    url = url.format(type=type)
    
    
    
    url = url.format(uri=uri)
    
    
    
    params = {
        
        
        
        
        
        
        
        
        
    }
    
    data = None
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def ProductOrderConcierge(data):
    """Places a concierge order"""
    import requests
    url = f"https://api.kompany.com//api/v1/product/order/concierge"
    
    params = {
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def ProductOrderUbo(data):
    """Places a UBO order"""
    import requests
    url = f"https://api.kompany.com//api/v1/product/order/ubo"
    
    params = {
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def ProductOrderWithOption(sku, option, subjectId):
    """Places a product order"""
    import requests
    url = f"https://api.kompany.com//api/v1/product/order/{sku}/{option}/{subjectId}"
    
    
    
    url = url.format(sku=sku)
    
    
    
    url = url.format(option=option)
    
    
    
    url = url.format(subjectId=subjectId)
    
    
    
    params = {
        
        
        
        
        
        
        
        
        
    }
    
    data = None
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def ProductOrder(sku, subjectId):
    """Places a product order"""
    import requests
    url = f"https://api.kompany.com//api/v1/product/order/{sku}/{subjectId}"
    
    
    
    url = url.format(sku=sku)
    
    
    
    url = url.format(subjectId=subjectId)
    
    
    
    params = {
        
        
        
        
        
        
        
    }
    
    data = None
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def ProductSearch(subjectId):
    """Returns a list of products"""
    import requests
    url = f"https://api.kompany.com//api/v1/product/search/{subjectId}"
    
    
    
    url = url.format(subjectId=subjectId)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def ProductStatus(orderId):
    """Returns metadata for a order"""
    import requests
    url = f"https://api.kompany.com//api/v1/product/status/{orderId}"
    
    
    
    url = url.format(orderId=orderId)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def ProductUpdateAction(action, orderId, data):
    """Updates metadata of an order"""
    import requests
    url = f"https://api.kompany.com//api/v1/product/update/{action}/{orderId}"
    
    
    
    url = url.format(action=action)
    
    
    
    url = url.format(orderId=orderId)
    
    
    
    params = {
        
        
        
        
        
        
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def ProductRetrieve(orderId):
    """Retrieves the result of an order"""
    import requests
    url = f"https://api.kompany.com//api/v1/product/{orderId}"
    
    
    
    url = url.format(orderId=orderId)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def SystemCountries():
    """Returns a list of countries"""
    import requests
    url = f"https://api.kompany.com//api/v1/system/countries"
    
    params = {
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def HealthCheck():
    """Returns the health information for the official business registers based on usage."""
    import requests
    url = f"https://api.kompany.com//api/v1/system/health"
    
    params = {
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def SystemPricelist():
    """Returns a list of products with prices"""
    import requests
    url = f"https://api.kompany.com//api/v1/system/pricelist"
    
    params = {
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def TinVerificationBasicCheck(tin, name):
    """Verifies a TIN number"""
    import requests
    url = f"https://api.kompany.com//api/v1/tin-verification/basic-check"
    
    
    
    
    
    
    
    params = {
        
        
        
        "tin": tin,
        
        
        
        "name": name,
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def TinVerificationComprehensiveCheck(tin, name, threshold):
    """EIN Name Lookup with TIN number and retrieves company data"""
    import requests
    url = f"https://api.kompany.com//api/v1/tin-verification/comprehensive-check"
    
    
    
    
    
    
    
    
    
    params = {
        
        
        
        "tin": tin,
        
        
        
        "name": name,
        
        
        
        "threshold": threshold,
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def TinVerificationNameLookup(tin):
    """EIN Name Lookup with TIN number"""
    import requests
    url = f"https://api.kompany.com//api/v1/tin-verification/name-lookup"
    
    
    
    
    
    params = {
        
        
        
        "tin": tin,
        
        
        
    }
    
    data = None
    
    response = requests.get(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def VatBasic(country, data):
    """Returns a verification result"""
    import requests
    url = f"https://api.kompany.com//api/v1/vat-verification/basic-check/{country}"
    
    
    
    url = url.format(country=country)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def VatComprehensive(country, data):
    """Returns a verification result and company data"""
    import requests
    url = f"https://api.kompany.com//api/v1/vat-verification/comprehensive-check/{country}"
    
    
    
    url = url.format(country=country)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def VatLevelTwo(country, data):
    """Returns a level two verification result"""
    import requests
    url = f"https://api.kompany.com//api/v1/vat-verification/leveltwo-check/{country}"
    
    
    
    url = url.format(country=country)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def VatLookup(country, data):
    """Returns a list of vat numbers with additional data"""
    import requests
    url = f"https://api.kompany.com//api/v1/vat-verification/lookup/{country}"
    
    
    
    url = url.format(country=country)
    
    
    
    params = {
        
        
        
        
        
    }
    
    data = data
    
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

