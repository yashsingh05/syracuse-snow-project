select
    c.id,
    c.summary,
    c.address,
    c.created_at,
    c.lat,
    c.lng,
    n.name as neighborhood_name
from stg_cityline_requests c
left join stg_neighborhoods n
    on ST_Within(
        ST_Transform(ST_Point(c.lat, c.lng), 'EPSG:4326', 'EPSG:3857'),
        ST_GeomFromText(n.geometry_wkt)
    )
