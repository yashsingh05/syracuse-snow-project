select
    id,
    summary,
    rating,
    address,
    category,
    strptime(created_at_local, '%m/%d/%Y - %I:%M%p') as created_at,
    strptime(acknowledged_at_local, '%m/%d/%Y - %I:%M%p') as acknowledged_at,
    strptime(closed_at_local, '%m/%d/%Y - %I:%M%p') as closed_at,
    minutes_to_acknowledge,
    sla_in_hours,
    report_source,
    lat,
    lng
from raw_cityline_requests
