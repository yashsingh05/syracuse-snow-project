with route_summary as (
    select
        neighborhood_name,
        count(*) as total_segments,
        sum(case when routepriority = 'Priority 1' then 1 else 0 end) as priority_1_segments,
        sum(case when routepriority = 'Priority 2' then 1 else 0 end) as priority_2_segments,
        round(100.0 * sum(case when routepriority = 'Priority 2' then 1 else 0 end) / count(*), 1) as pct_priority_2
    from routes_by_neighborhood
    where neighborhood_name is not null
    group by neighborhood_name
),
complaint_summary as (
    select
        neighborhood_name,
        count(*) as total_complaints
    from complaints_by_neighborhood
    where neighborhood_name is not null
    group by neighborhood_name
)
select
    r.neighborhood_name,
    r.total_segments,
    r.priority_1_segments,
    r.priority_2_segments,
    r.pct_priority_2,
    coalesce(c.total_complaints, 0) as total_complaints,
    round(coalesce(c.total_complaints, 0) * 1.0 / r.total_segments, 3) as complaints_per_segment
from route_summary r
left join complaint_summary c
    on r.neighborhood_name = c.neighborhood_name
order by r.pct_priority_2 desc
