select
    snapshot_file,
    cast(polled_at_utc as timestamp) as polled_at,
    objectid,
    roadname,
    routepriority,
    snowroutesegmentid,
    servicestatus,
    to_timestamp(lastserviced / 1000) as last_serviced_at,
    passes,
    eventid,
    geometry_wkt
from raw_snow_routes
