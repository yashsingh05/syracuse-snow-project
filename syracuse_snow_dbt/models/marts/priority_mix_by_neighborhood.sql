select
    neighborhood_name,
    count(*) as total_segments,
    sum(case when routepriority = 'Priority 1' then 1 else 0 end) as priority_1_segments,
    sum(case when routepriority = 'Priority 2' then 1 else 0 end) as priority_2_segments,
    round(
        100.0 * sum(case when routepriority = 'Priority 2' then 1 else 0 end) / count(*),
        1
    ) as pct_priority_2
from routes_by_neighborhood
where neighborhood_name is not null
group by neighborhood_name
order by pct_priority_2 desc
