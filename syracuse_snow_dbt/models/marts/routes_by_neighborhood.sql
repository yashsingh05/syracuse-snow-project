select
    s.objectid,
    s.roadname,
    s.routepriority,
    s.snowroutesegmentid,
    s.servicestatus,
    s.last_serviced_at,
    s.passes,
    n.name as neighborhood_name
from stg_snow_routes s
left join stg_neighborhoods n
    on ST_Intersects(
        ST_GeomFromText(s.geometry_wkt),
        ST_GeomFromText(n.geometry_wkt)
    )
