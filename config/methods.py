from config.regions import regions

def is_valid_country(country: str) -> bool:
    if country in regions:
        return True
    else:
        return False
    
def is_valid_region(country: str, region: str) -> bool:
    if country in regions:
        if region in regions[country]:
            return True
    return False