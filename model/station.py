class Station:
    
    def __init__(self, data):
        self.id = data.get("id", None)
        self.name = data.get("name", None)
        self.latitude = data.get("latitude", None)
        self.longitude = data.get("longitude", None)
        self.elevation = data.get("elevation", None)
        self.type = data.get("type", None)
        license_data = data.get("license", {})
        self.license = {
            "license": license_data.get("license", None),
            "url": license_data.get("url", None),
            "source": license_data.get("source", None),
            "metadonnees": license_data.get("metadonnees", None)
        }

    def getId(self):
        return self.id

    def __str__(self):
        return f"Station_id={self.id} \n name={self.name} \n latitude={self.latitude} \n longitude={self.longitude} \n elevation={self.elevation} \n type={self.type} \n license={self.license})"
