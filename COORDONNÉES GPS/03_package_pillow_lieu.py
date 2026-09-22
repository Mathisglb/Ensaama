from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def get_gps_coordinates(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()

    if exif_data is None:
        print("Aucune métadonnée EXIF trouvée.")
        return None

    gps_info = None
    for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, tag_id)
        if tag_name == "GPSInfo":
            gps_info = {GPSTAGS.get(k, k): v for k, v in value.items()}

    if gps_info is None:
        print("Pas de données GPS dans cette photo.")
        return None

    def to_deg(value):
        # value = (d, m, s), chacun étant un IFDRational -> on force le float
        d, m, s = value
        return float(d) + float(m) / 60 + float(s) / 3600

    lat = to_deg(gps_info["GPSLatitude"])
    if gps_info["GPSLatitudeRef"] != "N":
        lat = -lat

    lon = to_deg(gps_info["GPSLongitude"])
    if gps_info["GPSLongitudeRef"] != "E":
        lon = -lon

    return lat, lon, gps_info["GPSLatitudeRef"], gps_info["GPSLongitudeRef"]


def deg_to_dms(deg_abs, ref):
    """Convertit une valeur absolue en degrés décimaux vers une chaîne DMS."""
    d = int(deg_abs)
    m_float = (deg_abs - d) * 60
    m = int(m_float)
    s = (m_float - m) * 60
    return f"{d}° {m}′ {s:.2f}″ {ref}"


chemin_image = "photo.jpg"
result = get_gps_coordinates(chemin_image)

if result:
    latitude, longitude, lat_ref, lon_ref = result

    # Affichage décimal
    print(f"Latitude (décimal) : {latitude}")
    print(f"Longitude (décimal) : {longitude}")

    # Affichage DMS
    print(f"Latitude\t{deg_to_dms(abs(latitude), lat_ref)}")
    print(f"Longitude\t{deg_to_dms(abs(longitude), lon_ref)}")

    print(f"Google Maps : https://www.google.com/maps?q={latitude},{longitude}")