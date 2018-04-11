set mapred.job.queue.name = data;
set mapreduce.map.memory.mb=4096;
set mapreduce.reduce.memory.mb=4096;
set mapreduce.reduce.java.opts=-Xmx4096m -XX:+UseG1GC;

select
    facet,
    if(facet in ("ens_fromid"), channel_name, interest),
    count(distinct user_id), cast(sum(value) as bigint)
from
(select
    users.user_id as user_id, facet, interest, value
from
    (select
        distinct user_id
    from
        temp.dim_group_portrait_user
    where
        p_type = '${PARTITION}' and
        p_user = '${USER}') users
inner join
    (select
        user_id, facet, interest, value
    from
        dw.fact_merge_user_profile
    where
        p_day = '${DAY}' and
        p_type = 'Client' and
        facet in ("ens_gender", "ens_age", "lbs_area", "lbs_tier", "lbs_province", "lbs_city", "ens_ct", "ens_sct", "ens_fromid", "cs_keyword")
    union all
    select
        user_id, 'os' as facet, lower(os) as interest, 1 as value
    from
        dw.fact_merge_user_profile
    where
        p_day = '${DAY}' and
        p_type = 'Client' and
        facet in ("ens_gender", "ens_age", "lbs_area", "lbs_tier", "lbs_province", "lbs_city", "ens_ct", "ens_sct", "ens_fromid", "cs_keyword")
        ) profile
on
    users.user_id = profile.user_id) dims
left join
    (select from_id, channel_name from olap.dict_channel) channels
on
    dims.interest = channels.from_id
group by
    facet,
    if(facet in ("ens_fromid"), channel_name, interest)
;
